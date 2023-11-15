import os
import argparse
from sf_translate.services.translator import DeepLTranslator
from sf_translate.services.editor import ComponentEditor, DataEditor, LabelEditor
from sf_translate.constant import SALESFORCE_SUPPORTED_LANGUAGES, SUPPOTED_TRANSLATORS


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "type",
        type=str,
        default="data",
        choices=["component", "data", "label"],
        help="Type of XLIFF file you would like to translate",
    )
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Path to XLIFF file to translate"
    )
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="Path to XLIFF file to output"
    )
    parser.add_argument(
        "-tl",
        "--target_lang",
        type=str,
        choices=SALESFORCE_SUPPORTED_LANGUAGES,
        help="Language of the target text for data translation",
    )
    parser.add_argument(
        "-sl",
        "--source_lang",
        type=str,
        choices=SALESFORCE_SUPPORTED_LANGUAGES,
        help="Language of the source text for data translation",
    )
    parser.add_argument(
        "-t",
        "--translator",
        type=str,
        default="deepl",
        choices=SUPPOTED_TRANSLATORS,
        help="Translator to use",
    )
    parser.add_argument("-k", "--key", type=str, help="Translator API key for DeepL")
    return parser.parse_args()


def _get_editor(option, translator):
    if option.type == "component":
        return ComponentEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
        )
    elif option.type == "data":
        if not option.target_lang or not option.source_lang:
            raise ValueError(
                "Target and source languages are required for data translation"
            )
        return DataEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
            option.target_lang,
            option.source_lang,
        )
    elif option.type == "label":
        if not option.target_lang:
            raise ValueError(
                "Target and source languages are required for data translation"
            )
        return LabelEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
            option.target_lang,
            option.source_lang
        )
    else:
        raise NotImplementedError("Data translation is not yet implemented")


def _get_translator(option):
    if option.translator == "deepl":
        if not option.key:
            raise ValueError("DeepL API key is required")
        return DeepLTranslator(option.key)
    else:
        raise NotImplementedError("Translator is not yet implemented")


def main():
    option = _get_args()
    translator = _get_translator(option)
    editor = _get_editor(option, translator)
    editor.translate()


if __name__ == "__main__":
    main()
