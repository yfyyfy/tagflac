import filecmp
from os import path
from unittest import TestCase

from tagflac import metaflac_file, read_yaml
from tests.util import assert_test_files_identity, copy_to_test_directory, create_test_directory, file_in_test_directory

class TestMetaflacFile(TestCase):

    def _test_metaflac_file(self, testdir, yaml, *, convert=False):
        dirname = testdir
        create_test_directory(dirname)
        copy_to_test_directory(dirname, [yaml, 'convert.yml', '01.flac', '01.flac.expected'])

        tag_list = read_yaml(file_in_test_directory(dirname, yaml))
        convert_dict = read_yaml(file_in_test_directory(file_in_test_directory(dirname, 'convert.yml')))
        if convert:
            metaflac_file(file_in_test_directory(dirname, '01.flac'), tag_list, convert_dict)
        else:
            metaflac_file(file_in_test_directory(dirname, '01.flac'), tag_list)
        self.assertTrue(filecmp.cmp(file_in_test_directory(dirname, '01.flac'), file_in_test_directory(dirname, '01.flac.expected'), shallow=False))
        assert_test_files_identity(self, dirname, [yaml, 'convert.yml', '01.flac.expected'])

    def test_metaflac_file(self):
        self._test_metaflac_file('metaflac_file', 'tag_file.yml')

    def test_metaflac_file(self):
        self._test_metaflac_file('metaflac_file_convert', 'tag_file_for_convert.yml', convert=True)
