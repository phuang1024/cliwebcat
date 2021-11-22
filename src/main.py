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

import sys
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

def get_pkg(pkgs, identifier):
    if identifier is None:
        print("Specify package in CLI argument.")
        sys.exit(1)

    try:
        if identifier.isdigit():
            pkg = pkgs[int(identifier)]
        else:
            pkg = [p for p in pkgs if p["url"].endswith(f"/{identifier}.zip")][0]

    except IndexError:
        print(f"Invalid package \"{identifier}\".")
        sys.exit(1)

    return pkg

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


def parse_pkg(text, url):
    url_pat = "https{0,1}://"
    url_pat += url.replace(".", "\\.").split("://")[1]
    url_pat += "/.*?\\.zip"
    snarf_url = re.compile(url_pat).findall(text)[0]

    name = re.compile("name=\".*?\"").findall(text)[0].replace("name=", "").replace("\"", "")
    category = re.compile("category=\".*?\"").findall(text)[0].replace("category=", "").replace("\"", "")
    desc = re.compile("<description>.*?</description>").findall(text)[0].replace("<description>", "").replace("</description>", "")

    return {
        "name": name,
        "category": category,
        "desc": desc,
        "url": snarf_url,
    }

def read_pkgs(url, hidden):
    r = requests.get(os.path.join(url, "snarf.xml"))

    text = r.text
    if not hidden:
        text = remove_xml_comments(text)

    pkgs = []

    start = re.compile("<package")
    end = re.compile("</package>")
    for s, e in zip(start.finditer(text), end.finditer(text)):
        try:
            pkgs.append(parse_pkg(text[s.start(0):e.start(0)], url))
        except IndexError:
            pass

    return pkgs


def list_pkgs(pkgs):
    if len(pkgs) == 0:
        print("No packages found.")
        return

    longest = max([len(p["name"]) for p in pkgs]) + 3
    for i, pkg in enumerate(pkgs):
        name = pkg["name"]
        desc = pkg["desc"]

        sys.stdout.write(str(i)+":")
        sys.stdout.write(" " * (6-len(str(i))))
        sys.stdout.write(name)
        sys.stdout.write(" " * (longest - len(name)))
        sys.stdout.write(desc)
        sys.stdout.write("\n")

    sys.stdout.flush()

def info(pkgs, identifier):
    pkg = get_pkg(pkgs, identifier)

    print("Package " + pkg["name"])
    print("  * Name: " + pkg["name"])
    print("  * Category: " + pkg["category"])
    print("  * Description: " + pkg["desc"])
    print("  * URL: " + pkg["url"])

def snarf(pkgs, identifier):
    pkg = get_pkg(pkgs, identifier)

    r = requests.get(pkg["url"])
    if r.status_code != 200:
        print("Request failed.")
        return

    with open(TMP, "wb") as f:
        f.write(r.content)

    name = pkg["name"]
    if os.path.isdir(name):
        if input(f"{name} already exists. Overwrite? [y/N] ").lower() != "y":
            return

    with zipfile.ZipFile(TMP, "r") as f:
        f.extractall(name)
    os.remove(TMP)

    print(f"{name} snarfed.")

def submit(pkgs, identifier, submission, config):
    pkg = get_pkg(pkgs, identifier)


def main(args):
    parser = argparse.ArgumentParser(description="CLI Snarf")
    parser.add_argument("mode", nargs="?", choices={"ls", "config", "info", "snarf", "submit"}, default="ls")
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

    elif args.mode == "info":
        info(pkgs, args.pkg)

    elif args.mode == "snarf":
        snarf(pkgs, args.pkg)

    elif args.mode == "submit":
        submit(pkgs, args.pkg, args.submit, config)

    write_config(config)
