"""
Disease detection module with a SAFETY LAYER + AUTO-DETECT CROP support.

CRITICAL: MobileNetV3Large has built-in preprocessing/rescaling. Do NOT
divide pixel values by 255 here — the model was trained on raw 0-255
pixel values (Keras applies scaling internally). Dividing by 255 before
inference breaks the input signal and causes near-constant, image-independent
predictions (the exact "same result for every photo" bug).
"""
import tensorflow as tf
from PIL import Image
import io
import os
import numpy as np

from remedies import get_remedy, RETAKE_TIPS, CONFIDENCE_THRESHOLD, get_friendly_name
import glob
BACKEND_DIR = os.path.dirname(__file__)  
STATIC_REF_DIR = os.path.join(BACKEND_DIR, "static", "reference_images")

def _get_reference_image_url(raw_class_name: str):
    matches = glob.glob(os.path.join(STATIC_REF_DIR, f"{raw_class_name}.*"))
    if not matches:
        return None
    filename = os.path.basename(matches[0])
    return f"/static/reference_images/{filename}"
BACKEND_DIR = os.path.dirname(__file__)

MODEL_CANDIDATES = [
    os.path.join(BACKEND_DIR, "crop_disease_model_v2.tflite"),
    os.path.join(BACKEND_DIR, "crop_disease_model.tflite"),
]
CLASS_NAMES_PATH = os.path.join(BACKEND_DIR, "class_names.txt")

# Values the frontend can send that mean "don't restrict by crop —
# search across all 38 classes and let the model pick the best match."
AUTO_DETECT_VALUES = {"", "auto", "auto-detect", "unknown"}

_interpreter = None
_class_names = []
_active_model_name = None


def _load_model():
    global _interpreter, _class_names, _active_model_name
    if _interpreter is not None:
        return
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, "r") as f:
            _class_names = [line.strip() for line in f if line.strip()]
    for path in MODEL_CANDIDATES:
        if os.path.exists(path):
            import tensorflow as tf
            _interpreter = tf.lite.Interpreter(model_path=path)
            _interpreter.allocate_tensors()
            _active_model_name = os.path.basename(path)
            print(f"[detection.py] Loaded model: {_active_model_name}")
            break
    if _interpreter is None:
        print("[detection.py] No .tflite model found — using fallback heuristic.")


def _format_disease_name(raw_name: str):
    parts = raw_name.split("___")
    crop = parts[0].replace("_", " ").strip()
    disease = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Unknown"
    return crop, disease


def classify_leaf_image(image_bytes: bytes, crop_type: str, growth_stage: str = None):
    _load_model()
    if _interpreter is not None and _class_names:
        return _classify_with_model(image_bytes, crop_type)
    else:
        return _classify_with_heuristic(image_bytes, crop_type)


def _classify_with_model(image_bytes: bytes, crop_type: str):
    input_details = _interpreter.get_input_details()
    output_details = _interpreter.get_output_details()

    img_size = input_details[0]["shape"][1:3]
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(tuple(img_size))

    # CRITICAL FIX: keep raw 0-255 pixel values — do NOT divide by 255.
    # MobileNetV3Large's internal Rescaling layer handles normalization.
    arr = np.array(img, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)

    _interpreter.set_tensor(input_details[0]["index"], arr)
    _interpreter.invoke()
    output = _interpreter.get_tensor(output_details[0]["index"])[0]

    # Debug log — remove/comment out once confirmed working.
    print(f"[detection.py] raw output range: min={output.min():.4f} max={output.max():.4f}")

    # --- AUTO-DETECT CROP support ---
    # crop_key == "" / "auto" / etc. -> skip crop filtering entirely and
    # search across ALL classes for the best match (auto-detect mode).
    crop_key = (crop_type or "").lower().strip()
    is_auto = crop_key in AUTO_DETECT_VALUES

    if is_auto:
        matching_indices = []
    else:
        matching_indices = [
            i for i, name in enumerate(_class_names)
            if name.split("___")[0].lower().replace("_", " ").startswith(crop_key)
        ]
    pool = matching_indices if matching_indices else list(range(len(_class_names)))

    if matching_indices:
        top_idx = max(matching_indices, key=lambda i: output[i])
    else:
        top_idx = int(np.argmax(output))

    confidence = float(output[top_idx])
    raw_name = _class_names[top_idx] if top_idx < len(_class_names) else "Unknown"
    crop, disease = _format_disease_name(raw_name)
    is_healthy = "healthy" in disease.lower()

    # What to show as "crop" in the response: if the user picked a
    # specific crop, echo that back; if auto-detect, use the crop the
    # model itself identified from the leaf (e.g. "Tomato").
    display_crop = crop if is_auto else crop_type

    top3_idx = sorted(pool, key=lambda i: output[i], reverse=True)[:3]
    candidates = []
    for idx in top3_idx:
        _, c_disease = _format_disease_name(_class_names[idx])
        if "healthy" in c_disease.lower():
            continue
        remedy_entry = get_remedy(c_disease)
        candidates.append({
            "disease": c_disease,
            "disease_display": {lang: get_friendly_name(c_disease, lang) for lang in ["en", "hi", "mr"]},
            "confidence": round(float(output[idx]), 2),
            "reference_image": _get_reference_image_url(_class_names[idx]),
        })

    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "needs_retake": True,
            "disease": None,
            "disease_display": None,
            "confidence": round(confidence, 2),
            "crop": display_crop,
            "is_healthy": None,
            "explanation": f"Model confidence ({round(confidence*100)}%) is below the safety threshold ({int(CONFIDENCE_THRESHOLD*100)}%).",
            "retake_tips": RETAKE_TIPS,
            "remedy": None,
            "referral": None,
            "candidates": candidates,
        }

    remedy = None if is_healthy else get_remedy(disease)
    explanation = (
        f"MobileNetV3 model ({_active_model_name}) predicts '{disease}' on {crop} "
        f"with {round(confidence*100)}% confidence."
    )

    return {
        "needs_retake": False,
        "disease": "Healthy" if is_healthy else disease,
        "disease_display": {lang: get_friendly_name(disease, lang) for lang in ["en", "hi", "mr"]} if not is_healthy else None,
        "confidence": round(confidence, 2),
        "crop": display_crop,
        "is_healthy": is_healthy,
        "explanation": explanation,
        "retake_tips": None,
        "remedy": remedy,
        "referral": None if is_healthy else remedy.get("referral"),
        "candidates": candidates,
    }


DISEASE_LIBRARY = {
    "tomato": ["Early Blight", "Late Blight", "Leaf Mold", "Healthy"],
    "potato": ["Early Blight", "Late Blight", "Healthy"],
    "corn": ["Common Rust", "Northern Leaf Blight", "Gray Leaf Spot", "Healthy"],
    "apple": ["Apple Scab", "Black Rot", "Cedar Apple Rust", "Healthy"],
    "grape": ["Black Rot", "Esca", "Leaf Blight", "Healthy"],
    "pepper": ["Bacterial Spot", "Healthy"],
    "wheat": ["Leaf Rust", "Powdery Mildew", "Healthy"],
    "rice": ["Bacterial Blight", "Blast", "Brown Spot", "Healthy"],
    "cotton": ["Bacterial Blight", "Leaf Curl Virus", "Healthy"],
}


def _classify_with_heuristic(image_bytes: bytes, crop_type: str):
    crop_key = (crop_type or "").lower().strip()
    # If auto-detect was requested but we only have the fallback
    # heuristic (no .tflite model available), we can't actually guess
    # the crop from pixels alone — default to the tomato library as a
    # reasonable generic guess for a leaf photo.
    if crop_key in AUTO_DETECT_VALUES:
        crop_key = "tomato"
    possible_diseases = DISEASE_LIBRARY.get(crop_key, DISEASE_LIBRARY["tomato"])
    display_crop = crop_type if crop_type and crop_type.lower().strip() not in AUTO_DETECT_VALUES else crop_key.title()

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((128, 128))
    pixels = list(img.getdata())
    total = len(pixels)
    green_dominant = sum(1 for r, g, b in pixels if g > r and g > b and g > 90)
    brown_yellow = sum(1 for r, g, b in pixels if r > 100 and g > 60 and b < 90 and r > b)
    green_ratio = green_dominant / total
    stress_ratio = brown_yellow / total

    if green_ratio > 0.75 and stress_ratio < 0.1:
        return {
            "needs_retake": False, "disease": "Healthy", "disease_display": None,
            "confidence": round(min(0.99, 0.80 + green_ratio * 0.2), 2),
            "crop": display_crop, "is_healthy": True,
            "explanation": f"[Fallback heuristic] Leaf area is {round(green_ratio*100)}% green.",
            "retake_tips": None, "remedy": None, "referral": None, "candidates": [],
        }
    else:
        candidates_list = [d for d in possible_diseases if d != "Healthy"]
        idx = min(int(stress_ratio * len(candidates_list)) % max(len(candidates_list), 1), len(candidates_list) - 1)
        disease = candidates_list[idx] if candidates_list else "Unknown"
        remedy = get_remedy(disease)
        return {
            "needs_retake": False, "disease": disease,
            "disease_display": {lang: get_friendly_name(disease, lang) for lang in ["en", "hi", "mr"]},
            "confidence": round(min(0.97, 0.55 + stress_ratio * 2), 2),
            "crop": display_crop, "is_healthy": False,
            "explanation": f"[Fallback heuristic] Pattern consistent with {disease}.",
            "retake_tips": None, "remedy": remedy, "referral": remedy.get("referral"), "candidates": [],
        }