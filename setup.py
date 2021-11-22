#
#  CLI Web-CAT
#  CLI Web-CAT interface.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

with open("requirements.txt", "r") as file:
    requirements = file.read().strip().split("\n")

setuptools.setup(
    name="cliwebcat",
    version="0.0.1",
    author="Patrick Huang",
    author_email="phuang1024@gmail.com",
    description="CLI Web-CAT interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phuang1024/cliwebcat",
    py_modules=["webcat"],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points={"console_scripts": ["webcat = webcat.main:main"]},
)
