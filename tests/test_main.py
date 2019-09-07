import filecmp
from os import path
import subprocess
from sys import executable
from unittest import TestCase

from tagflac import metaflac_dir, read_yaml
from util import assert_test_files_identity, copy_to_test_directory, create_test_directory, file_in_test_directory

class TestMain(TestCase):

    def test_main_file(self):
        dirname = 'main'
        create_test_directory(dirname)
        copy_to_test_directory(dirname, ['tag_file.yml', '01.flac', '01.flac.expected'])

        python = executable
        completed_process = subprocess.run([python, 'tagflac.py', '--tags', file_in_test_directory(dirname, 'tag_file.yml'), file_in_test_directory(dirname, '01.flac')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertTrue(filecmp.cmp(file_in_test_directory(dirname, '01.flac'), file_in_test_directory(dirname, '01.flac.expected'), shallow=False))
        assert_test_files_identity(self, dirname, ['tag_file.yml', '01.flac.expected'])

    def test_main_dir(self):
        dirname = 'main'
        create_test_directory(dirname)
        copy_to_test_directory(dirname, ['tag_dir_1.yml', '01.flac', '01.flac.expected'])

        python = executable
        completed_process = subprocess.run([python, 'tagflac.py', '--tags', file_in_test_directory(dirname, 'tag_dir_1.yml'), file_in_test_directory(dirname)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertTrue(filecmp.cmp(file_in_test_directory(dirname, '01.flac'), file_in_test_directory(dirname, '01.flac.expected'), shallow=False))
        assert_test_files_identity(self, dirname, ['tag_dir_1.yml', '01.flac.expected'])
