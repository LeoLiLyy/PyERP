import json


def load_translations(language):
    with open(f'translations/{language}.json', 'r') as f:
        translations = json.load(f)
    return translations
