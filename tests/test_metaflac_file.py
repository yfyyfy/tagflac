import filecmp
from os import path
from unittest import TestCase

from tagflac import metaflac_file, read_yaml
from tests.util import assert_test_files_identity, copy_flac_to_test_directory, copy_to_test_directory, file_in_test_directory

class TestMetaflacFile(TestCase):

    def _test_metaflac_file(self, testdir, *, convert=False):
        tag_yaml = 'tags.yml'
        convert_yaml = 'convert.yml'
        dirname = testdir
        copy_to_test_directory(dirname)
        flacfiles = copy_flac_to_test_directory(dirname, [1])
        flacfile = flacfiles[0]

        tag_list = read_yaml(file_in_test_directory(dirname, tag_yaml))
        if convert:
            convert_dict = read_yaml(file_in_test_directory(file_in_test_directory(dirname, convert_yaml)))
            metaflac_file(file_in_test_directory(dirname, flacfile), tag_list, convert_dict)
        else:
            metaflac_file(file_in_test_directory(dirname, flacfile), tag_list)
        self.assertTrue(filecmp.cmp(file_in_test_directory(dirname, flacfile), file_in_test_directory(dirname, flacfile + '.expected'), shallow=False))
        assert_test_files_identity(self, dirname, [tag_yaml, *([convert_yaml] if convert else []), flacfile + '.expected'])

    def test_metaflac_file(self):
        self._test_metaflac_file('metaflac_file')

    def test_metaflac_file_convert(self):
        self._test_metaflac_file('metaflac_file_convert', convert=True)
