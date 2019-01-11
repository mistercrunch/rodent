# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
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

import io
import os

from setuptools import find_packages, setup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

version_string = "0.1.0"

setup(
    name="rodent",
    description="A CLI utility to manage license headers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version_string,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=["rodent/bin/rodent"],
    install_requires=["gitpython", "click"],
    author="Maxime Beauchemin",
    author_email="maximebeauchemin@gmail.com",
    url="https://github.com/mistercrunch/rodent",
    download_url=(
        "https://github.com" "/mistercrunch/rodent/tarball/" + version_string
    ),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
    ],
    license="Apache License 2.0",
)
