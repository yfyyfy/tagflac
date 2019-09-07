from glob import glob
from logging import basicConfig, getLogger, DEBUG
from os import path
import re
import subprocess
import yaml

basicConfig(level=DEBUG)

logger = getLogger(__name__)

def read_yaml(filepath):
    with open(filepath) as f:
        return yaml.safe_load(f)
    raise Exception(f'Read yaml file failed: {filepath}')

def metaflac_file(filepath, tags):
    # Run
    set_tags = [f'--set-tag={k}={v}' for k, v in sorted(tags.items())]
    completed_process = subprocess.run(['metaflac', '--remove-all-tags', *set_tags, filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Output log
    returncode = completed_process.returncode
    stderr = completed_process.stderr
    stdout = completed_process.stdout
    if returncode != 0:
        logger.error(f'metaflac failed with code {returncode}')
        logger.error(f'metaflac finished with the message below:')
        if stderr:
            for line in stderr.decode('utf-8').split('\n'):
                logger.error(f'> {line}')
    if stdout:
        logger.info(f'metaflac finished with the message below:')
        for line in stdout.decode('utf-8').split('\n'):
            logger.error(f'> {line}')
    if returncode == 0 and not stdout:
        logger.info(f'metaflac succeeded with no output')

def tags_for_file(tag_list, fileindex):
    tags = {}
    files_in_dict = tag_list.get('files')
    if files_in_dict is None:
        raise Exception('Key \'files\' was not found')
    for record in files_in_dict:
        fileindex_in_dict = record.get('fileindex')
        tags_in_dict = record.get('tags')
        if fileindex_in_dict is None:
            if tags_in_dict is None:
                tags_in_dict = record
            fileindex_in_dict = tags_in_dict.get('tracknumber')
            if fileindex_in_dict is None:
                fileindex_in_dict = 'all'
            else:
                fileindex_in_dict = [fileindex_in_dict]
        if fileindex_in_dict == 'all' or fileindex in fileindex_in_dict:
            tags.update(tags_in_dict)
    return tags

def metaflac_dir(dirpath, tag_list):
    regex = re.compile(r'\d+')
    for flacfile in glob(f'{dirpath}/*.flac'):
        # Get and check fileindex
        fileindex = path.splitext(path.basename(flacfile))[0]
        if not regex.match(fileindex):
            logger.error(f'Unexpected filename: {flacfile}')
            continue
        fileindex = int(fileindex)

        # Collect tags for fileindex
        tags = tags_for_file(tag_list, fileindex)
        if len(tags) == 0:
            logger.error(f'No entry was found for {flacfile}')
            continue

        # Run metaflac
        metaflac_file(flacfile, tags)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(
        '--tags',
        type=argparse.FileType('r'),
        required=True,
        help='tag file in yaml format'
    )
    parser.add_argument(
        'target',
        metavar='target',
        type=str,
        help='flac file to edit tags or directory contaianing flac files'
    )

    args = parser.parse_args()

    tag_list = yaml.safe_load(args.tags)
    target = args.target

    if path.isdir(target):
        metaflac_dir(target, tag_list)
        pass
    elif path.isfile(target):
        metaflac_file(target, tag_list)
    else:
        raise Exception(f'Target file or directory {target} was not found')

if __name__ == '__main__':
    main()
