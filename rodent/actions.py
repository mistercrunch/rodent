import os
import git

from rodent.licenses import LICENSE_MAP

EXT_MAP = {
    'js': 'javascript',
    'jsx': 'javascript',
    'py': 'python',
}
LICENSE_WRAPPER = {
    'python': lambda s: '"""\n{}\n"""'.format(s),
    'javascript': lambda s: '/*\n{}\n*/'.format(s),
}


def get_commented_license(license, language):
    license_text = LICENSE_MAP[license]
    license_mutator = LICENSE_WRAPPER[language]
    return license_mutator(license_text)


def get_extension(filename):
    splitted = filename.split('.')
    return splitted[-1] if len(splitted) > 1 else ''


def files_in_scope(folder='./', extentions=None):
    file_list = []
    if not extentions:
        extentions = EXT_MAP.keys()


    repo_files = git.cmd.Git().ls_files().split()
    for filename in repo_files:
        ext = get_extension(filename)
        if not extentions or ext in extentions:
            yield filename


def list_files(folder='./', extentions=None):
    for s in files_in_scope(folder, extentions):
        print(s)


def apply(filepath, license_text):
    file_content = read_file(filepath)
    if not check_license(file_content, license_text):
        print('APPLY TO: ' + filepath)
    else:
        print('SKIPPING: ' + filepath)


def check_license(file_content, license_text):
    commented_license_text = get_commented_license(license, language)
    return commented_license_text in file_content


def read_file(filepath):
    with open(os.path.join(dir_name, filename), 'r') as f:
        file_content = f.read()
