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

## Configuration

When you run `webcat` the first time, it will interactively ask you for configuration.

* Snarf root URL: Root path e.g. `http://example.com/apcssnarf`
* Username: Your WebCAT username.
* Password: Stored in plaintext.

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
webcat submit 12345 /path/to/folder
webcat submit JMCh12_AsDf /path/to/folder

```
