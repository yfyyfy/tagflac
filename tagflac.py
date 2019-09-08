from glob import glob
from logging import basicConfig, getLogger, DEBUG
from os import path
import re
import roman
from string import Formatter
import subprocess
import yaml

basicConfig(level=DEBUG)

logger = getLogger(__name__)

class TagFormatter(Formatter):
    def getarg(self, spec, specname, argstr):
        matchOB = re.match(r'^' + re.escape(specname) + r':(.*)$', spec)
        if not matchOB:
            raise Exception(f'Spec \'{specname}\' must be given argument(s), e.g., \'post:{argstr}\'')
        return matchOB.group(1)

    def replace_if_not_none(self, format_str, value, *, default=None):
        if value is None:
            return default
        return format_str.format(value=value)

    def format_field(self, value, format_spec):
        separator = ';'
        for spec in format_spec.split(separator):
            if spec == 'roman':
                try:
                    value = roman.toRoman(value)
                except:
                    continue
            elif spec == 'squo':
                value = self.replace_if_not_none('\'{value}\'', value)
            elif spec == 'dquo':
                value = self.replace_if_not_none('"{value}"', value)
            elif spec == 'paren':
                value = self.replace_if_not_none('({value})', value)
            elif spec == 'optional':
                value = self.replace_if_not_none(' {value}', value, default='')
            elif spec.startswith('post'):
                suffix = self.getarg(spec, 'post', 'SUFFIX_STR')
                value = self.replace_if_not_none(f'{{value}}{suffix}', value)
            elif spec.startswith('pre'):
                prefix = self.getarg(spec, 'pre', 'PREFIX_STR')
                value = self.replace_if_not_none(f'{prefix}{{value}}', value)
            else:
                value = super().format_field(value, spec)
        return value

def construct_tags(tag_list, convert_dict=None):
    fmt = TagFormatter()
    if convert_dict is None:
        return tag_list

    ret = {}
    for key, format_str in convert_dict.items():
        complemented_tag_list = {}
        for parsed in fmt.parse(format_str):
            literal_text, field_name, format_spec, conversion = parsed
            complemented_tag_list.update({field_name: None})
        complemented_tag_list.update(tag_list)
        ret.update({key: fmt.format(format_str, **complemented_tag_list)})

    return ret

def read_yaml(filepath):
    with open(filepath) as f:
        return yaml.safe_load(f)
    raise Exception(f'Read yaml file failed: {filepath}')

def metaflac_file(filepath, tags, convert_dict=None):
    # Run
    set_tags = [f'--set-tag={k}={v}' for k, v in sorted(construct_tags(tags, convert_dict).items())]
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

def metaflac_dir(dirpath, tag_list, convert_dict=None):
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
        metaflac_file(flacfile, tags, convert_dict)


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
        '--convert',
        type=argparse.FileType('r'),
        help='tag conversion file (from yaml to flac) in yaml format'
    )
    parser.add_argument(
        'target',
        metavar='target',
        type=str,
        help='flac file to edit tags or directory contaianing flac files'
    )

    args = parser.parse_args()

    tag_list = yaml.safe_load(args.tags)
    if args.convert:
        convert_dict = yaml.safe_load(args.convert)
    else:
        convert_dict = None
    target = args.target

    if path.isdir(target):
        metaflac_dir(target, tag_list, convert_dict)
        pass
    elif path.isfile(target):
        metaflac_file(target, tag_list, convert_dict)
    else:
        raise Exception(f'Target file or directory {target} was not found')

if __name__ == '__main__':
    main()
