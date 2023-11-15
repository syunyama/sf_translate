# Salesforce Translator

This tool is used to translate file for 3 types below.
1. [Export Data Translation Files](https://help.salesforce.com/s/articleView?id=sf.workbench_export_data.htm&type=5) (data)
1. [Localize Store Labels](https://help.salesforce.com/s/articleView?id=sf.comm_translate_store_labels_manually.htm&type=5) (component) 
1. Translate metadata file from [CustomLabels](https://developer.salesforce.com/docs/atlas.en-us.244.0.api_meta.meta/api_meta/meta_customlabels.htm) to [Translations](https://developer.salesforce.com/docs/atlas.en-us.244.0.api_meta.meta/api_meta/meta_translations.htm) (label)

## Supported Translator
- [DeepL](https://www.deepl.com/translator)

## Utilize
### Make command in local
```sh
python3 setup.py develop
```

### Uninstall command from local
```sh
python3 setup.py develop -u
```

### Make library in local
```sh
pip3 install -e .
```

### Uninstall library from local
```sh
pip3 uninstall sf_translate
```

## Commands

### Command for data type
```sh
python3 command.py data -i sample/data/Source_Product2_sample.xlf -o sample/data/RESULT_Source_Product2_sample.xlf -tl en_US -sl ja -k {deepl key}
```
OR if you like installed command
```sh
sf_translate data -i sample/data/Source_Product2_sample.xlf -o sample/data/RESULT_Source_Product2_sample.xlf -tl en_US -sl ja -k {deepl key}
```

### Command for component type
```sh
python3 command.py component -i sample/component/components_ja_en-US_sample.xlf -o sample/component/RESULT_components_ja_en-US_sample.xlf -k {deepl key}
```
OR if you like installed command
```sh
sf_translate component -i sample/component/components_ja_en-US_sample.xlf -o sample/component/RESULT_components_ja_en-US_sample.xlf -k {deepl key}
```

### Command for label type
```sh
python3 command.py label -i sample/label/CustomLabels.labels-meta.xml -o sample/label/ja.translation-meta.xml -tl ja -k {deepl key}
```
OR if you like installed command
```sh
sf_translate label -i sample/label/CustomLabels.labels-meta.xml -o sample/label/ja.translation-meta.xml -tl ja -k {deepl key}
```

## Use as Python library
```python
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

```

## Roadmap (Hopefully)
- Translating `Translations` meta data to another language.
- Supporting Googole translator.

## Notes
- Some non pure string value like JSON or HTML and so on can not be translated properly.




