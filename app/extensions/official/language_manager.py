import json
import os


def load_translations(language_code):
    filename = f'{language_code}.json'
    filepath = os.path.join('translations', filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"Language file '{filepath}' not found.")


class LanguageManager:
    def __init__(self, language_code):
        self.translations = load_translations(language_code)

    def translate(self, key):
        return self.translations.get(key, key)


# Helper function for easier use in templates
def _(key):
    return language_manager.translate(key)
