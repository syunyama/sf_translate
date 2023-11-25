import os
import argparse
from sf_translate.services.translator import DeepLTranslator, GoogleTranslator
from sf_translate.services.editor import (
    ComponentXMLEditor,
    DataXMLEditor,
    LabelXMLEditor,
    LabelConvertXMLEditor,
    StandardValueXMLEditor,
    StandardValueConvertXMLEditor,
    TranslationConvertXMLEditor,
    PropertyEditor,
)
from sf_translate.constants import (
    SALESFORCE_SUPPORTED_LANGUAGES,
    SUPPOTED_TRANSLATORS,
    TRANSLATE_TYPE,
)


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "type",
        type=str,
        default="xml:data",
        choices=TRANSLATE_TYPE,
        help="Type of file you would like to translate",
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
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        required=True,
        help="Translator API key for DeepL or Google",
    )
    parser.add_argument(
        "-m", "--max_workers", type=str, help="Max workers for concurrent translation"
    )
    return parser.parse_args()


def _get_editor(option, translator):
    if option.type == "xml:component":
        return ComponentXMLEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
            max_workers=option.max_workers,
        )
    elif option.type == "xml:data":
        if not option.target_lang or not option.source_lang:
            raise ValueError(
                "Target and source languages are required for data translation"
            )
        return DataXMLEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
            option.target_lang,
            option.source_lang,
            max_workers=option.max_workers,
        )
    elif option.type == "xml:label":
        if not option.target_lang:
            raise ValueError(
                "Target and source languages are required for data translation"
            )
        return LabelXMLEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
            option.target_lang,
            source_lang=option.source_lang,
            max_workers=option.max_workers,
        )
    elif option.type == "xml:label_convert":
        if not option.target_lang:
            raise ValueError(
                "Target and source languages are required for data translation"
            )
        return LabelConvertXMLEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
            option.target_lang,
            source_lang=option.source_lang,
            max_workers=option.max_workers,
        )
    elif option.type == "xml:standard_value":
        if not option.target_lang:
            raise ValueError(
                "Target and source languages are required for data translation"
            )
        return StandardValueXMLEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
            option.target_lang,
            source_lang=option.source_lang,
            max_workers=option.max_workers,
        )
    elif option.type == "xml:standard_value_convert":
        if not option.target_lang:
            raise ValueError(
                "Target and source languages are required for data translation"
            )
        return StandardValueConvertXMLEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
            option.target_lang,
            source_lang=option.source_lang,
            max_workers=option.max_workers,
        )
    elif option.type == "xml:translation_convert":
        if not option.target_lang:
            raise ValueError(
                "Target and source languages are required for data translation"
            )
        return TranslationConvertXMLEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
            option.target_lang,
            source_lang=option.source_lang,
            max_workers=option.max_workers,
        )
    elif option.type == "property:basic":
        if not option.target_lang:
            raise ValueError(
                "Target and source languages are required for data translation"
            )
        return PropertyEditor(
            translator,
            os.path.abspath(option.input),
            os.path.abspath(option.output),
            option.target_lang,
            source_lang=option.source_lang,
            max_workers=option.max_workers,
        )
    else:
        raise NotImplementedError("Data translation is not yet implemented")


def _get_translator(option):
    if option.translator == "deepl":
        if not option.key:
            raise ValueError("DeepL API key is required")
        return DeepLTranslator(option.key)
    elif option.translator == "google":
        if not option.key:
            raise ValueError("Google API key is required")
        return GoogleTranslator(option.key)
    else:
        raise NotImplementedError("Translator is not yet implemented")


def main():
    option = _get_args()
    translator = _get_translator(option)
    editor = _get_editor(option, translator)
    editor.translate()


if __name__ == "__main__":
    main()
