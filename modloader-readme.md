# wows-modloader

The World of Warships modloader manages loading python mod packages.

* Automatic loading of mods in the packages directory
* Custom "import" functionality because World of Warships broke pythons import
* Logging of errors and mod related messages to a mods.log

# Installation

* copy modloader.pyc into {game-install-path}/res_mods/{game-version}/scripts/client/mods
* create the directory {game-install-path}/res_mods/{game-version}/scripts/client/mods/packages

# Use

Modloader loads any installed mod from the packages folder ({game-install-path}/res_mods/{game-version}/scripts/client/mods/packages).
Each package has to be a directory inside the packages directory with an __init__.py file in it, for instance 
{game-install-path}/res_mods/{game-version}/scripts/client/mods/packages/mymod/__init__.py .

Import errors are logged into the file {game-install-path}/res_mods/{game-version}/scripts/client/mods/mods.log.

Each module in your mod can make use of two new builtin commands.

The require function loads another module from within your mod. Example:

```python
somemodule = require('somemodule')
```

The function modlog replaces pythons print and writes to <game-install-path>/res_mods/<game-version>/scripts/client/mods/mods.log:

```
modlog('here', 123)
```

# Mods using this loader

* [repl](https://github.com/pyalot/wows-python-repl)
