import filecmp
from os import path
import subprocess
from sys import executable
from unittest import TestCase

from tagflac import metaflac_dir, read_yaml
from tests.util import assert_test_files_identity, copy_flac_to_test_directory, copy_to_test_directory, file_in_test_directory

class TestMain(TestCase):

    def test_main_file(self):
        dirname = 'main_file'
        copy_to_test_directory(dirname)
        copy_flac_to_test_directory(dirname, [1])

        python = executable
        completed_process = subprocess.run([python, 'tagflac.py', '--tags', file_in_test_directory(dirname, 'tags.yml'), file_in_test_directory(dirname, '01.flac')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertTrue(filecmp.cmp(file_in_test_directory(dirname, '01.flac'), file_in_test_directory(dirname, '01.flac.expected'), shallow=False))
        assert_test_files_identity(self, dirname, ['tags.yml', '01.flac.expected'])

    def test_main_dir(self):
        dirname = 'main_dir'
        copy_to_test_directory(dirname)
        copy_flac_to_test_directory(dirname, [1])

        python = executable
        completed_process = subprocess.run([python, 'tagflac.py', '--tags', file_in_test_directory(dirname, 'tags.yml'), file_in_test_directory(dirname)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertTrue(filecmp.cmp(file_in_test_directory(dirname, '01.flac'), file_in_test_directory(dirname, '01.flac.expected'), shallow=False))
        assert_test_files_identity(self, dirname, ['tags.yml', '01.flac.expected'])
