import filecmp
from os import makedirs, path
from shutil import copyfile, rmtree

def create_test_directory(dirname):
    dirpath = path.dirname(__file__)
    test_directory = path.join(dirpath, 'testdir', dirname)

    rmtree(test_directory, ignore_errors=True)
    makedirs(test_directory, exist_ok=True)

def file_in_test_directory(dirname, filename=None):
    dirpath = path.dirname(__file__)
    test_directory = path.join(dirpath, 'testdir', dirname)
    if filename is None:
        return test_directory
    else:
        return path.join(test_directory, filename)

def copy_to_test_directory(dirname, filenames):
    dirpath = path.dirname(__file__)
    data_directory = path.join(dirpath, 'data')

    for filename in filenames:
        if filename is None:
            continue
        copyfile(path.join(data_directory, filename), file_in_test_directory(dirname, filename))

def assert_test_files_identity(this, dirname, filenames):
    dirpath = path.dirname(__file__)
    data_directory = path.join(dirpath, 'data')

    for filename in filenames:
        if filename is None:
            continue
        this.assertTrue(filecmp.cmp(path.join(data_directory, filename), file_in_test_directory(dirname, filename), shallow=False))
