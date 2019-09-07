import filecmp
from os import path
from unittest import TestCase

from tagflac import metaflac_file, read_yaml
from util import assert_test_files_identity, copy_to_test_directory, create_test_directory, file_in_test_directory

class TestMetaflacFile(TestCase):

    def test_metaflac_file(self):
        dirname = 'metaflac_file'
        create_test_directory(dirname)
        copy_to_test_directory(dirname, ['tag_file.yml', '01.flac', '01.flac.expected'])

        tag_list = read_yaml(file_in_test_directory(dirname, 'tag_file.yml'))
        metaflac_file(file_in_test_directory(dirname, '01.flac'), tag_list)
        self.assertTrue(filecmp.cmp(file_in_test_directory(dirname, '01.flac'), file_in_test_directory(dirname, '01.flac.expected'), shallow=False))
        assert_test_files_identity(self, dirname, ['tag_file.yml', '01.flac.expected'])
