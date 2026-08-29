"""
Remedy database + safety-layer messaging for Kisan Raksha Network.
"""

REMEDY_DB = {
    "early blight": {
        "severity": "Moderate",
        "reference_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Alternaria_solani_lesion.jpg/320px-Alternaria_solani_lesion.jpg",
        "description": {
            "en": "Fungal disease causing dark concentric-ring spots on lower leaves, spreading upward.",
            "hi": "यह एक फफूंद रोग है जो निचली पत्तियों पर काले घेरेदार धब्बे बनाता है और ऊपर फैलता है।",
            "mr": "हा एक बुरशीजन्य रोग आहे ज्यामुळे खालच्या पानांवर काळे वर्तुळाकार डाग पडतात आणि वर पसरतात.",
        },
        "chemical_remedy": {
            "en": "Spray Mancozeb (2g per liter water) or Chlorothalonil every 7 to 10 days.",
            "hi": "मैंकोज़ेब (2 ग्राम प्रति लीटर पानी) या क्लोरोथैलोनिल का हर 7 से 10 दिन में छिड़काव करें।",
            "mr": "मॅन्कोझेब (2 ग्रॅम प्रति लिटर पाणी) किंवा क्लोरोथॅलोनिलची दर 7 ते 10 दिवसांनी फवारणी करा.",
        },
        "organic_remedy": {
            "en": "Neem oil spray, 5ml per liter, every 5 days. Remove and destroy infected lower leaves.",
            "hi": "नीम तेल का छिड़काव, 5 मिली प्रति लीटर, हर 5 दिन में करें। संक्रमित निचली पत्तियों को हटा दें।",
            "mr": "कडुनिंब तेल फवारणी, 5 मिली प्रति लिटर, दर 5 दिवसांनी करा. संक्रमित खालची पाने काढून टाका.",
        },
        "steps": [
            {"icon": "cut", "title": {"en": "Remove infected leaves", "hi": "संक्रमित पत्तियाँ हटाएँ", "mr": "संक्रमित पाने काढा"},
             "detail": {"en": "Cut off and destroy affected lower leaves to stop spread.", "hi": "फैलाव रोकने के लिए प्रभावित निचली पत्तियों को काटकर नष्ट करें।", "mr": "प्रसार थांबवण्यासाठी प्रभावित खालची पाने कापून नष्ट करा."}},
            {"icon": "spray", "title": {"en": "Apply spray", "hi": "छिड़काव करें", "mr": "फवारणी करा"},
             "detail": {"en": "Spray chemical or organic remedy evenly on all leaves, including undersides.", "hi": "सभी पत्तियों पर, नीचे की तरफ भी, समान रूप से छिड़काव करें।", "mr": "सर्व पानांवर, खालच्या बाजूनेही, समान फवारणी करा."}},
            {"icon": "water", "title": {"en": "Avoid overhead watering", "hi": "ऊपर से पानी देने से बचें", "mr": "वरून पाणी देणे टाळा"},
             "detail": {"en": "Water at the base of the plant to keep leaves dry.", "hi": "पत्तियों को सूखा रखने के लिए पौधे की जड़ में पानी दें।", "mr": "पाने कोरडी ठेवण्यासाठी झाडाच्या मुळाशी पाणी द्या."}},
            {"icon": "monitor", "title": {"en": "Re-check in 7 days", "hi": "7 दिन में फिर से जाँचें", "mr": "7 दिवसांनी पुन्हा तपासा"},
             "detail": {"en": "If spots continue spreading, repeat the spray and consult local Krishi Kendra.", "hi": "यदि धब्बे फैलते रहें, तो छिड़काव दोहराएँ और स्थानीय कृषि केंद्र से सलाह लें।", "mr": "डाग पसरत राहिल्यास, फवारणी पुन्हा करा आणि स्थानिक कृषी केंद्राचा सल्ला घ्या."}},
        ],
    },
    "late blight": {
        "severity": "High",
        "reference_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Phytophthora_infestans_on_tomato_leaf.jpg/320px-Phytophthora_infestans_on_tomato_leaf.jpg",
        "description": {
            "en": "Fast spreading fungal disease causing water soaked dark patches. Can destroy a field within days.",
            "hi": "तेजी से फैलने वाला फफूंद रोग जो पानी से भीगे काले धब्बे बनाता है। कुछ दिनों में पूरा खेत बर्बाद कर सकता है।",
            "mr": "वेगाने पसरणारा बुरशीजन्य रोग ज्यामुळे पाणी शोषलेले काळे डाग पडतात. काही दिवसांत संपूर्ण शेत नष्ट करू शकतो.",
        },
        "chemical_remedy": {
            "en": "Spray Metalaxyl plus Mancozeb combination immediately. Repeat every 5 to 7 days.",
            "hi": "तुरंत मेटालैक्सिल और मैंकोज़ेब का मिश्रण छिड़कें। हर 5 से 7 दिन में दोहराएँ।",
            "mr": "त्वरित मेटालॅक्सिल आणि मॅन्कोझेब मिश्रण फवारा. दर 5 ते 7 दिवसांनी पुन्हा करा.",
        },
        "organic_remedy": {
            "en": "Copper based fungicide spray. Improve field drainage immediately.",
            "hi": "कॉपर आधारित फफूंदनाशक का छिड़काव करें। तुरंत खेत की जल निकासी सुधारें।",
            "mr": "कॉपर आधारित बुरशीनाशक फवारा. त्वरित शेताचा निचरा सुधारा.",
        },
        "steps": [
            {"icon": "isolate", "title": {"en": "Act within 24 hours", "hi": "24 घंटे के भीतर कार्रवाई करें", "mr": "24 तासांत कृती करा"},
             "detail": {"en": "Late blight spreads fast. Do not wait, spray today.", "hi": "यह रोग तेजी से फैलता है। इंतज़ार न करें, आज ही छिड़काव करें।", "mr": "हा रोग वेगाने पसरतो. थांबू नका, आजच फवारणी करा."}},
            {"icon": "cut", "title": {"en": "Remove severely infected plants", "hi": "गंभीर रूप से संक्रमित पौधे हटाएँ", "mr": "गंभीर संक्रमित रोपे काढा"},
             "detail": {"en": "Uproot and burn or bury badly affected plants away from the field.", "hi": "गंभीर रूप से प्रभावित पौधों को उखाड़ें और खेत से दूर जलाएँ या दबाएँ।", "mr": "गंभीर प्रभावित रोपे उपटून शेतापासून दूर जाळा किंवा पुरा."}},
            {"icon": "spray", "title": {"en": "Spray full field", "hi": "पूरे खेत में छिड़काव करें", "mr": "संपूर्ण शेतात फवारणी करा"},
             "detail": {"en": "Treat the entire field, not just visibly affected plants.", "hi": "केवल दिखने वाले प्रभावित पौधों को नहीं, पूरे खेत का उपचार करें।", "mr": "फक्त दिसणाऱ्या प्रभावित रोपांनाच नाही, संपूर्ण शेताला उपचार द्या."}},
            {"icon": "monitor", "title": {"en": "Check daily for 1 week", "hi": "1 सप्ताह तक रोज़ जाँचें", "mr": "1 आठवडा दररोज तपासा"},
             "detail": {"en": "This disease can return quickly. Daily monitoring is critical.", "hi": "यह रोग जल्दी वापस आ सकता है। रोज़ाना निगरानी ज़रूरी है।", "mr": "हा रोग लवकर परत येऊ शकतो. दररोज तपासणी महत्त्वाची आहे."}},
        ],
        "referral": {
            "en": "This disease spreads fast and can destroy your field. Please show this photo to your nearest Krishi Kendra within 2 days.",
            "hi": "यह रोग तेज़ी से फैलता है और पूरा खेत बर्बाद कर सकता है। कृपया यह फोटो 2 दिन के भीतर अपने नज़दीकी कृषि केंद्र को दिखाएँ।",
            "mr": "हा रोग वेगाने पसरतो आणि संपूर्ण शेत नष्ट करू शकतो. कृपया हा फोटो 2 दिवसांत तुमच्या जवळच्या कृषी केंद्राला दाखवा.",
        },
    },
    "healthy": {
        "severity": "None",
        "reference_image": None,
        "description": {
            "en": "No disease detected. Leaf appears healthy.",
            "hi": "कोई रोग नहीं मिला। पत्ती स्वस्थ दिखाई देती है।",
            "mr": "कोणताही रोग आढळला नाही. पान निरोगी दिसत आहे.",
        },
        "chemical_remedy": {"en": "Not needed.", "hi": "आवश्यकता नहीं।", "mr": "गरज नाही."},
        "organic_remedy": {"en": "Continue routine care and monitoring.", "hi": "नियमित देखभाल और निगरानी जारी रखें।", "mr": "नियमित काळजी आणि तपासणी सुरू ठेवा."},
        "steps": [
            {"icon": "monitor", "title": {"en": "Keep monitoring weekly", "hi": "साप्ताहिक निगरानी जारी रखें", "mr": "साप्ताहिक तपासणी सुरू ठेवा"},
             "detail": {"en": "Check plants weekly for early signs of stress or disease.", "hi": "तनाव या रोग के शुरुआती लक्षणों के लिए साप्ताहिक जाँच करें।", "mr": "ताण किंवा रोगाच्या सुरुवातीच्या लक्षणांसाठी साप्ताहिक तपासणी करा."}},
        ],
    },
    "_default": {
        "severity": "Unknown",
        "reference_image": None,
        "description": {
            "en": "Disease detected. Please consult your local Krishi Kendra for specific treatment.",
            "hi": "रोग का पता चला है। सही उपचार के लिए अपने स्थानीय कृषि केंद्र से सलाह लें।",
            "mr": "रोग आढळला आहे. योग्य उपचारासाठी तुमच्या स्थानिक कृषी केंद्राचा सल्ला घ्या.",
        },
        "chemical_remedy": {"en": "Consult a local agriculture officer for the correct chemical treatment.", "hi": "सही रासायनिक उपचार के लिए स्थानीय कृषि अधिकारी से सलाह लें।", "mr": "योग्य रासायनिक उपचारासाठी स्थानिक कृषी अधिकाऱ्याचा सल्ला घ्या."},
        "organic_remedy": {"en": "Remove visibly affected leaves and improve air circulation around the plant.", "hi": "दिखने वाली प्रभावित पत्तियों को हटाएँ और पौधे के आसपास हवा का संचार बढ़ाएँ।", "mr": "दिसणारी प्रभावित पाने काढा आणि झाडाभोवती हवा खेळती ठेवा."},
        "steps": [
            {"icon": "cut", "title": {"en": "Remove affected leaves", "hi": "प्रभावित पत्तियाँ हटाएँ", "mr": "प्रभावित पाने काढा"},
             "detail": {"en": "Reduce spread by removing visibly diseased leaves.", "hi": "दिखने वाली रोगग्रस्त पत्तियों को हटाकर फैलाव कम करें।", "mr": "दिसणारी रोगग्रस्त पाने काढून प्रसार कमी करा."}},
            {"icon": "monitor", "title": {"en": "Consult local expert", "hi": "स्थानीय विशेषज्ञ से सलाह लें", "mr": "स्थानिक तज्ञांचा सल्ला घ्या"},
             "detail": {"en": "Show this photo to your Krishi Kendra for exact treatment.", "hi": "सटीक उपचार के लिए यह फोटो अपने कृषि केंद्र को दिखाएँ।", "mr": "अचूक उपचारासाठी हा फोटो तुमच्या कृषी केंद्राला दाखवा."}},
        ],
    },
}

RETAKE_TIPS = {
    "en": "The model is not confident enough to give a safe diagnosis. Please retake the photo. Use good daylight, focus on a single leaf, avoid blur, and use a plain background.",
    "hi": "मॉडल को सुरक्षित निदान देने के लिए पर्याप्त विश्वास नहीं है। कृपया फोटो फिर से लें। अच्छी रोशनी में, एक पत्ती पर फोकस करें, धुंधलापन न हो, और सादी पृष्ठभूमि का उपयोग करें।",
    "mr": "मॉडेलला सुरक्षित निदान देण्याइतका आत्मविश्वास नाही. कृपया फोटो पुन्हा घ्या. चांगल्या उजेडात, एका पानावर फोकस करा, अस्पष्ट नसावे, आणि साधी पार्श्वभूमी वापरा.",
}

CONFIDENCE_THRESHOLD = 0.65


def get_remedy(disease_name: str):
    key = (disease_name or "").strip().lower()
    for db_key, entry in REMEDY_DB.items():
        if db_key != "_default" and db_key in key:
            return entry
    return REMEDY_DB["_default"]