import os
from sf_translate.services.translator import DeepLTranslator
from sf_translate.services.editor import LabelEditor


def main():
    translator = DeepLTranslator("Your DeepL API Key")
    editor = LabelEditor(
        translator = translator,
        xml_input_path = os.path.abspath("sample/label/CustomLabels.labels-meta.xml"),
        xml_output_path = os.path.abspath("sample/label/ja.translation-meta.xml"),
        target_lang = "ja",
        source_lang="en_US",
    )
    editor.translate()


if __name__ == "__main__":
    main()
