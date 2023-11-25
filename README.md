# Salesforce Translate

This tool is used to translate file for 3 types below.
1. [Export Data Translation Files](https://help.salesforce.com/s/articleView?id=sf.workbench_export_data.htm&type=5) (xml:data)
1. [Localize Store Labels](https://help.salesforce.com/s/articleView?id=sf.comm_translate_store_labels_manually.htm&type=5) (xml:component) 
1. Translate metadata file from [CustomLabels](https://developer.salesforce.com/docs/atlas.en-us.244.0.api_meta.meta/api_meta/meta_customlabels.htm) to [Translations](https://developer.salesforce.com/docs/atlas.en-us.244.0.api_meta.meta/api_meta/meta_translations.htm) (xml:label)
1. Translate [Translations](https://developer.salesforce.com/docs/atlas.en-us.244.0.api_meta.meta/api_meta/meta_translations.htm) files to another language (xml:label_convert)
1. Translate metadata file from [StandardValueSet](https://developer.salesforce.com/docs/atlas.en-us.244.0.api_meta.meta/api_meta/meta_standardvalueset.htm) to [StandardValueSetTranslation](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_standardvaluesettranslation.htm) (xml:standard_value)
1. Translate property file like [SFRA template localization](https://developer.salesforce.com/docs/commerce/b2c-commerce/guide/b2c-localization.html'#using-one-template-set-to-localize) (property:basic)

## Supported Translator
- [DeepL](https://www.deepl.com/translator)
    - Get API Key following [this instruction](https://support.deepl.com/hc/en-us/articles/360020695820-Authentication-Key)
- [Google Cloud](https://cloud.google.com/translate/docs/reference/rest/v2/translate)
    -  Get API Key following [this instruction](https://cloud.google.com/docs/authentication/api-keys?hl=ja#create)

## Install dependencies
```
pip3 install -r requirements.txt
```

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

## Basic usage
```
python3 command.py {arguments}
```
OR if you already utilized as command
```
sf_translate {arguments}
```

## Commands
### For data type
```sh
sf_translate xml:data -i sample/data/Source_Product2_sample.xlf -o sample/result/RESULT_Source_Product2_sample.xlf -tl en_US -sl ja -k {api key}
```

### For component type
```sh
sf_translate xml:component -i sample/component/components_ja_en-US_sample.xlf -o sample/result/RESULT_components_ja_en-US_sample.xlf -k {api key}
```

### For label type
```sh
sf_translate xml:label -i sample/label/CustomLabels.labels-meta.xml -o sample/result/ja.translation-meta.xml -tl ja -k {api key}
```

### For label convert type
```sh
sf_translate xml:label_convert -i sample/label_convert/ja.translation-meta.xml -o sample/result/ko.translation-meta.xml -tl ko -k {api key}
```

### For standard value
```sh
sf_translate xml:standard_value -i sample/standardValue/LeadSource.standardValueSet-meta.xml -o sample/result/LeadSource-ko.standardValueSetTranslation-meta.xml -tl ko -k {api key}
```

### For property type
```sh
sf_translate property:basic -i sample/property/account.properties -o sample/result/address_ja_JP.properties -tl ja -k {api key}
```

## Use as Python library
```python
import os
from sf_translate.services.translator import DeepLTranslator, GoogleTranslator
from sf_translate.services.editor import LabelXMLEditor


def main():
    translator = DeepLTranslator("Your DeepL API Key")
    # OR
    # translator = GoogleTranslator("Your Google Cloud API Key")
    editor = LabelXMLEditor(
        translator = translator,
        input_path = os.path.abspath("sample/label/CustomLabels.labels-meta.xml"),
        output_path = os.path.abspath("sample/label/ja.translation-meta.xml"),
        target_lang = "ja",
        source_lang="en_US",
    )
    editor.translate()


if __name__ == "__main__":
    main()

```

## Notes
- Some non pure string value like JSON, HTML and so on can not be translated properly.




