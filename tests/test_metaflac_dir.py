import filecmp
from os import path
from unittest import TestCase

from tagflac import metaflac_dir, read_yaml
from tests.util import assert_test_files_identity, copy_flac_to_test_directory, copy_to_test_directory, file_in_test_directory, generate_expected_flac_file

class TestMetaflacDir(TestCase):

    def _test_metaflac_dir(self, testdir, indices, *, convert=False):
        tag_yaml = 'tags.yml'
        convert_yaml = 'convert.yml'
        expected_suffix = 'expected'
        dirname = testdir
        copy_to_test_directory(dirname)
        generate_expected_flac_file(dirname, indices)
        flacfiles = copy_flac_to_test_directory(dirname, indices)

        tag_list = read_yaml(file_in_test_directory(dirname, tag_yaml))
        if convert:
            convert_dict = read_yaml(file_in_test_directory(file_in_test_directory(dirname, convert_yaml)))
            metaflac_dir(file_in_test_directory(dirname), tag_list, convert_dict)
        else:
            metaflac_dir(file_in_test_directory(dirname), tag_list)
        for flacfile in flacfiles:
            self.assertTrue(filecmp.cmp(file_in_test_directory(dirname, flacfile), file_in_test_directory(dirname, f'{flacfile}.{expected_suffix}'), shallow=False))
        assert_test_files_identity(self, dirname, [tag_yaml, *([convert_yaml] if convert else [])])

    def test_metaflac_dir1(self):
        self._test_metaflac_dir('metaflac_dir1', [1])

    def test_metaflac_dir2(self):
        self._test_metaflac_dir('metaflac_dir2', [1])

    def test_metaflac_dir3(self):
        self._test_metaflac_dir('metaflac_dir3', [1])

    def test_metaflac_dir1_convert(self):
        self._test_metaflac_dir('metaflac_dir1_convert', [1], convert=True)

    def test_metaflac_real_world01(self):
        self._test_metaflac_dir('metaflac_real_world01', range(1, 9), convert=True)

    def test_metaflac_real_world02(self):
        self._test_metaflac_dir('metaflac_real_world02', range(1, 25), convert=True)

    def test_metaflac_real_world03_simple(self):
        self._test_metaflac_dir('metaflac_real_world03_simple', range(1, 40), convert=True)
