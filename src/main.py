#
#  CLI Snarf
#  CLI Web-CAT snarfer for people who use VIM.
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

import os
import re
import json
import requests
import argparse
import zipfile
from getpass import getpass

CONFIG_PATH = os.path.expanduser("~/.config/clisnarf.json")
TMP = os.path.expanduser("~/.clisnarf.zip")


def remove_xml_comments(text):
    while "<!--" in text:
        start = text.find("<!--")
        end = text.find("-->")
        text = text[:start] + text[end+3:]

    return text


def read_config():
    data = {}
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)

    if "snarfpath" not in data:
        data["snarfpath"] = input("Snarf root URL: ").strip("/")
    if "username" not in data:
        data["username"] = input("Username: ")
    if "password" not in data:
        data["password"] = getpass("Password: ")

    return data

def write_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


def get_regex(snarfpath):
    pattern = "https{0,1}://"
    pattern += snarfpath.replace(".", "\\.").split("://")[1]
    pattern += "/.*\\.zip"
    return re.compile(pattern)

def read_pkgs(url, hidden):
    r = requests.get(os.path.join(url, "snarf.xml"))

    text = r.text
    l = len(text)
    if not hidden:
        text = remove_xml_comments(text)

    url_pat = "https{0,1}://"
    url_pat += url.replace(".", "\\.").split("://")[1]
    url_pat += "/.*\\.zip"

    return get_regex(url).findall(text)

def list_pkgs(pkgs):
    if len(pkgs) == 0:
        print("No packages found.")
        return

    for i, path in enumerate(pkgs):
        name = os.path.basename(path).replace(".zip", "")
        print(f"{i}: {name}")


def snarf(pkgs, pkg):
    if pkg is None:
        pkg = input("Package to snarf: ")

    try:
        if pkg.isdigit():
            path = pkgs[int(pkg)]
        else:
            path = [p for p in pkgs if p.endswith(f"/{pkg}.zip")][0]
    except IndexError:
        print("Invalid package.")
        return
    name = path.split("/")[-1].replace(".zip", "")

    r = requests.get(path)
    if r.status_code != 200:
        print("Request failed.")
        return

    with open(TMP, "wb") as f:
        f.write(r.content)

    if os.path.isdir(name):
        if input(f"{name} already exists. Overwrite? [y/N] ").lower() != "y":
            return

    with zipfile.ZipFile(TMP, "r") as f:
        f.extractall(name)
    os.remove(TMP)

    print(f"{name} snarfed.")


def main(args):
    parser = argparse.ArgumentParser(description="CLI Snarf")
    parser.add_argument("mode", nargs="?", choices={"ls", "config", "snarf", "submit"}, default="ls")
    parser.add_argument("pkg", nargs="?", help="Package name or index.")
    parser.add_argument("submit", nargs="?", help="Path to your work to submit.")
    parser.add_argument("--hidden", action="store_true", help="Allow hidden packages.")
    args = parser.parse_args(args)

    config = read_config()
    pkgs = read_pkgs(config["snarfpath"], args.hidden)

    if args.mode == "ls":
        list_pkgs(pkgs)

    elif args.mode == "config":
        os.system(f"vim {CONFIG_PATH}")

    elif args.mode == "snarf":
        snarf(pkgs, args.pkg)

    write_config(config)
