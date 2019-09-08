import filecmp
from os import path
from unittest import TestCase

from tagflac import metaflac_dir, read_yaml
from util import assert_test_files_identity, copy_to_test_directory, create_test_directory, file_in_test_directory

class TestMetaflacDir(TestCase):

    def _test_metaflac_dir(self, testdir, yaml, *, convert=False):
        dirname = testdir
        create_test_directory(dirname)
        copy_to_test_directory(dirname, [yaml, 'convert.yml', '01.flac', '01.flac.expected'])

        dirpath = path.dirname(__file__)
        tag_list = read_yaml(file_in_test_directory(dirname, yaml))
        convert_dict = read_yaml(file_in_test_directory(file_in_test_directory(dirname, 'convert.yml')))
        if convert:
            metaflac_dir(file_in_test_directory(dirname), tag_list, convert_dict)
        else:
            metaflac_dir(file_in_test_directory(dirname), tag_list)
        self.assertTrue(filecmp.cmp(file_in_test_directory(dirname, '01.flac'), file_in_test_directory(dirname, '01.flac.expected'), shallow=False))
        assert_test_files_identity(self, dirname, [yaml, 'convert.yml', '01.flac.expected'])

    def test_metaflac_dir1(self):
        self._test_metaflac_dir('metaflac_dir1', 'tag_dir_1.yml')

    def test_metaflac_dir2(self):
        self._test_metaflac_dir('metaflac_dir2', 'tag_dir_2.yml')

    def test_metaflac_dir3(self):
        self._test_metaflac_dir('metaflac_dir3', 'tag_dir_3.yml')

    def test_metaflac_dir1_convert(self):
        self._test_metaflac_dir('metaflac_dir1_convert', 'tag_dir_1_for_convert.yml', convert=True)
