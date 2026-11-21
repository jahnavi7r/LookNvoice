"""
Telugu-only language data for LookNvoice (AAC gaze interface).
Every sentence is written in full, in Subject-Object-Verb (SOV) order.
"""


def _item(item_id, label, sentence):
    return {"id": item_id, "label": label, "sentence": sentence}


TELUGU = {
    "code": "te",
    "name": "తెలుగు",
    "english_name": "Telugu",
    "locale": "te-IN",
    "voice_keywords": ["telugu", "te-in", "te_in"],
    "ui": {
        "back": "వెనుకకు",
        "next": "తదుపరి",
        "recalibrate": "RE-CALIBRATE",
        "recal_message": "రీ-కాలిబ్రేషన్ మొదలైంది... స్క్రీన్ మధ్యలో చూడండి",
    },
    "menu": [
        {"id": "me", "label": "నాకు", "type": "subject"},
        {"id": "food", "label": "ఆహారం", "type": "category", "items": [
            _item("dal", "పప్పు", "నాకు పప్పు కావాలి"),
            _item("roti", "రొట్టె", "నాకు రొట్టె కావాలి"),
            _item("rice", "అన్నం", "నాకు అన్నం కావాలి"),
            _item("curry", "కూర", "నాకు కూర కావాలి"),
            _item("snack", "అల్పాహారం", "నాకు అల్పాహారం కావాలి"),
            _item("biscuit", "బిస్కెట్", "నాకు బిస్కెట్ కావాలి"),
            _item("tiffin", "టిఫిన్", "నాకు టిఫిన్ కావాలి"),
            _item("something_else", "ఇంకేదైనా", "నాకు ఇంకేదైనా కావాలి"),
        ]},
        {"id": "water", "label": "నీళ్లు", "type": "sentence",
         "sentence": "నాకు నీళ్లు కావాలి"},
        {"id": "go", "label": "వెళ్లాలి", "type": "category", "items": [
            _item("room", "గదిలోకి", "నేను గదిలోకి వెళ్లాలి"),
            _item("washroom", "బాత్రూంకి", "నేను బాత్రూంకి వెళ్లాలి"),
            _item("bed", "మంచం మీదకి", "నేను మంచం మీదకి వెళ్లాలి"),
            _item("home", "ఇంటికి", "నేను ఇంటికి వెళ్లాలి"),
            _item("outside", "బయటకి", "నేను బయటకి వెళ్లాలి"),
            _item("hospital", "ఆసుపత్రికి", "నేను ఆసుపత్రికి వెళ్లాలి"),
            _item("garden", "తోటలోకి", "నేను తోటలోకి వెళ్లాలి"),
        ]},
        {"id": "pain", "label": "నొప్పి", "type": "category", "items": [
            _item("head", "తలలో", "నాకు తలలో నొప్పిగా ఉంది"),
            _item("stomach", "కడుపులో", "నాకు కడుపులో నొప్పిగా ఉంది"),
            _item("chest", "ఛాతీలో", "నాకు ఛాతీలో నొప్పిగా ఉంది"),
            _item("hand", "చేతిలో", "నాకు చేతిలో నొప్పిగా ఉంది"),
            _item("legs", "కాళ్లలో", "నాకు కాళ్లలో నొప్పిగా ఉంది"),
            _item("back", "వీపులో", "నాకు వీపులో నొప్పిగా ఉంది"),
            _item("somewhere", "ఎక్కడో", "నాకు నొప్పిగా ఉంది"),
        ]},
        {"id": "help", "label": "సహాయం", "type": "sentence",
         "sentence": "నాకు సహాయం కావాలి"},
        {"id": "yes", "label": "అవును", "type": "sentence", "sentence": "అవును"},
        {"id": "no", "label": "కాదు", "type": "sentence", "sentence": "కాదు"},
    ],
}

LANGUAGES = {"te": TELUGU}
LANGUAGE_ORDER = ["te"]


def find_entry(entries, entry_id):
    """Return the dict in `entries` whose id matches, or None."""
    for entry in entries:
        if entry["id"] == entry_id:
            return entry
    return None