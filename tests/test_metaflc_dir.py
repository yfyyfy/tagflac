import filecmp
from os import path
from unittest import TestCase

from tagflac import metaflac_dir, read_yaml
from util import assert_test_files_identity, copy_to_test_directory, create_test_directory, file_in_test_directory

class TestMetaflacDir(TestCase):

    def _test_metaflac_dir(self, testdir, flacfiles, tag_yaml, expected_suffix, *, convert_yaml=None):
        dirname = testdir
        create_test_directory(dirname)
        copy_to_test_directory(dirname, [tag_yaml, convert_yaml, *flacfiles, *[f'{flacfile}.{expected_suffix}' for flacfile in flacfiles]])

        dirpath = path.dirname(__file__)
        tag_list = read_yaml(file_in_test_directory(dirname, tag_yaml))
        if convert_yaml is not None:
            convert_dict = read_yaml(file_in_test_directory(file_in_test_directory(dirname, convert_yaml)))
            metaflac_dir(file_in_test_directory(dirname), tag_list, convert_dict)
        else:
            metaflac_dir(file_in_test_directory(dirname), tag_list)
        for flacfile in flacfiles:
            self.assertTrue(filecmp.cmp(file_in_test_directory(dirname, flacfile), file_in_test_directory(dirname, f'{flacfile}.{expected_suffix}'), shallow=False))
        assert_test_files_identity(self, dirname, [tag_yaml, convert_yaml, *[f'{flacfile}.{expected_suffix}' for flacfile in flacfiles]])

    def test_metaflac_dir1(self):
        self._test_metaflac_dir('metaflac_dir1', ['01.flac'], 'tag_dir_1.yml', 'expected')

    def test_metaflac_dir2(self):
        self._test_metaflac_dir('metaflac_dir2', ['01.flac'], 'tag_dir_2.yml', 'expected')

    def test_metaflac_dir3(self):
        self._test_metaflac_dir('metaflac_dir3', ['01.flac'], 'tag_dir_3.yml', 'expected')

    def test_metaflac_dir1_convert(self):
        self._test_metaflac_dir('metaflac_dir1_convert', ['01.flac'], 'tag_dir_1_for_convert.yml', 'expected', convert_yaml='convert.yml')

    def test_metaflac_complete(self):
        self._test_metaflac_dir('metaflac_complete', ['{num:02d}.flac'.format(num=num) for num in range(1, 9)], 'complete.yml', 'expected.complete', convert_yaml='convert_complete.yml')
