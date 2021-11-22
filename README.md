# CLI Web-CAT

CLI Web-CAT interface.

## Installation

``` bash
git clone https://github.com/phuang1024/cliwebcat
cd cliwebcat
python setup.py bdist_wheel sdist
cd dist
pip install *.whl

webcat --help
```

## Usage

``` bash
# List packages
webcat
webcat ls

# Show hidden packages
webcat --hidden
webcat ls --hidden

# Show package info
webcat info 12345        # index
webcat into JMCh12_AsDf  # name

# Edit configuration file with VIM
webcat config

# Snarf package
webcat snarf 12345
webcat snarf JMCh12_AsDf

# Submit (not implemneted yet)
webcat submit /path/to/folder

```
