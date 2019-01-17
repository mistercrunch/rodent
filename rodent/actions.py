# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import os
import re
import sys

import click

import git

from rodent.licenses import LICENSE_MAP


def js_wrapper(s, filepath):
    lines = []
    lines.append("/**")
    lines += [" * " + line if line else " *" for line in s.split("\n")]
    lines.append(" */")
    return "\n".join(lines)


def py_wrapper(s, filepath):
    lines = []
    lines += ["# " + line if line else "#" for line in s.split("\n")]
    return "\n".join(lines)


def html_wrapper(s, filepath):
    jinja_regex = os.environ.get("RODENT_JINJA_REGEX")
    lines = []
    if jinja_regex and re.match(jinja_regex, filepath):
        lines += ["  " + line if line else "" for line in s.split("\n")]
        return "{#\n" + "\n".join(lines) + "\n#}"
    lines += ["  " + line if line else "" for line in s.split("\n")]
    return "<!--\n" + "\n".join(lines) + "\n-->"


EXT_MAP = {
    "js": "javascript",
    "css": "css",
    "jsx": "javascript",
    "py": "python",
    "html": "html",
}
LICENSE_WRAPPER = {
    "python": py_wrapper,
    "javascript": js_wrapper,
    "css": js_wrapper,
    "html": html_wrapper,
}
SPECIAL_FIRST_LINES = ["#!", "# -*-", "from __future__ "]


def get_commented_license(license_type, language, filename):
    license_text = LICENSE_MAP[license_type]
    license_type_mutator = LICENSE_WRAPPER[language]
    return license_type_mutator(license_text, filename)


def get_extension(filename):
    splitted = filename.split(".")
    return splitted[-1] if len(splitted) > 1 else ""


def files_in_scope(file_regex=None):
    repo_files = git.cmd.Git().ls_files().split()
    if not file_regex:
        return repo_files
    return [s for s in repo_files if re.match(file_regex, s)]


def list_files(file_regex=None):
    for filename in files_in_scope(file_regex):
        print(filename)


def apply(file_regex=None, license_type="asf"):
    for filename in files_in_scope(file_regex):
        apply_to_file(filename, license_type)
    click.echo(click.style("All done! 🍰", fg="white"))


def check(file_regex=None, license_type="asf"):
    failed = []
    for filepath in files_in_scope(file_regex):
        file_content = read_file(filepath)
        language = get_language(filepath)
        if language and not check_license(file_content, language, license_type, filepath):
            failed.append(filepath)
    if failed:
        click.echo(click.style("Check failed", fg="red"))
        for s in failed:
            click.echo(click.style("* " + s, fg="red"))
        sys.exit(1)
    else:
        click.echo(click.style("Check passed!", fg="green"))


def get_language(filename):
    ext = get_extension(filename)
    return EXT_MAP.get(ext)


def squeeze_in_license(file_content, commented_license_text):
    """Skips shebang and adds license content"""
    license_applied = False
    newfile_lines = []
    for line in file_content.split("\n"):
        if not license_applied:
            is_special_line = any(line.startswith(s) for s in SPECIAL_FIRST_LINES)
            if not is_special_line:
                newfile_lines.append(commented_license_text)
                license_applied = True
        newfile_lines.append(line)
    return "\n".join(newfile_lines)


def apply_to_file(filepath, license_type="asf"):
    file_content = read_file(filepath)
    language = get_language(filepath)
    if (
            language and
            file_content and not
            check_license(file_content, language, license_type, filepath)
    ):
        commented_license_text = get_commented_license(license_type, language, filepath)
        click.echo(click.style("[adding license] - " + filepath, fg="green"))
        with open(filepath, "w") as f:
            new_content = squeeze_in_license(file_content, commented_license_text)
            f.write(new_content)
    else:
        click.echo(click.style("[skipping] - " + filepath, fg="red"))


def check_license(file_content, language, license_type="asf", filepath=None):
    commented_license_text = get_commented_license(license_type, language, filepath)
    if not file_content:
        return True
    return commented_license_text in file_content


def read_file(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception:
        pass
