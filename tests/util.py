import filecmp
from os import makedirs, path
from shutil import copyfile, copytree, rmtree
import subprocess

def file_in_test_directory(dirname, filename=None):
    dirpath = path.dirname(__file__)
    test_directory = path.join(dirpath, 'testdir', dirname)
    if filename is None:
        return test_directory
    else:
        return path.join(test_directory, filename)

def generate_expected_flac_file(dirname, indices):
    copy_flac_to_test_directory(dirname, indices, ext='.expected')

    dirpath = path.dirname(__file__)
    base_flac = path.join(dirpath, 'data', 'base.flac')
    test_directory = path.join(dirpath, 'testdir', dirname)
    for index in indices:
        txt = file_in_test_directory(dirname, f'{index:02}.expected.txt')
        p = subprocess.run(['metaflac', '--import-tags-from', txt, file_in_test_directory(dirname, f'{index:02}.flac.expected')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(p.stderr.decode('utf-8'))

def copy_flac_to_test_directory(dirname, indices, *, ext=''):
    # Assume that destination directory exists.
    dirpath = path.dirname(__file__)
    base_flac = path.join(dirpath, 'data', 'base.flac')
    test_directory = path.join(dirpath, 'testdir', dirname)
    for index in indices:
        copyfile(base_flac, path.join(test_directory, f'{index:02}.flac{ext}'))

    return [f'{index:02}.flac{ext}' for index in indices]

def copy_to_test_directory(dirname):
    dirpath = path.dirname(__file__)
    data_directory = path.join(dirpath, 'data', dirname)
    test_directory = path.join(dirpath, 'testdir', dirname)

    rmtree(test_directory, ignore_errors=True)
    copytree(data_directory, file_in_test_directory(dirname))

def assert_test_files_identity(this, dirname, filenames):
    dirpath = path.dirname(__file__)
    data_directory = path.join(dirpath, 'data', dirname)

    for filename in filenames:
        if filename is None:
            continue
        this.assertTrue(filecmp.cmp(path.join(data_directory, filename), file_in_test_directory(dirname, filename), shallow=False))
