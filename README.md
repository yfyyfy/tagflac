# tagflac
metaflac wrapper

## Usage
``` sh
python3 -m venv env
env/bin/python tagflac.py --tags TAGS_YAML_FILE FLAC_FILE
env/bin/python tagflac.py --tags TAGS_YAML_FILE --convert CONVERT_CONFIG_YAML_FILE FLAC_FILE
env/bin/python tagflac.py --tags TAGS_YAML_FILE --convert CONVERT_CONFIG_YAML_FILE DIR_CONTAINING_FLAC_FILES
env/bin/python -m unittest discover tests  # Run all tests
env/bin/python -m unittest tests.test_main # Run a specific test, e.g., test_main
```

If CONVERT_CONFIG_YAML_FILE is specified, the properties defined in TAGS_YAML_FILE are converted according to the expression specified in CONVERT_CONFIG_YAML_FILE.
Otherwise, all properties in TAGS_YAML_FILE are directly set as tags for flac file(s).

See [tests/data](tests/data) for examples of yaml files

### Create a dummy flac file
``` sh
printf aa > input.raw
sox -t raw -r 44100 -b 16 -c 1 -L -e signed-integer input.raw output.wav
flac output.wav
rm input.raw output.wav
```
