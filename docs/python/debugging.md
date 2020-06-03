# Debugging


I saw [this great talk](https://www.youtube.com/watch?v=5AYIe-3cD-s) by [Nina Zakharenko](https://www.nnja.io/) ([handout](https://nina.to/pycon2020)), I learned most tips on this page from that talk.

## pdb

Python Debugger (pdb) is easy to use, simply put `breakpoint()` in your `.py` file and run it (python >= 3.7).
[Florian Preinstorfer](https://github.com/nblock/pdb-cheatsheet) made a great cheatsheet for what to do once you're inside the debugger.

![](./img/pdb-cheatsheet.png)

If you want to enter the regular python REPL from the debug mode type `interact`.

## ipdb

The vanilla python debugger is good, but it misses some basic features such as tab completion.
Luckily there is [ipdb](https://github.com/gotcha/ipdb) which is a (near) drop-in replacement.

To set it up:

1. In your python environment: install ipdb `python -m pip install ipdb`
2. In your shell's rc file: set python breakpoint to ipdb  `export PYTHONBREAKPOINT = ipdb.set_trace`
3. In your root folder: Create a `.pdbrc` with this content (credits to [Nina Zahrenko](https://www.nnja.io/post/2020/pycon2020-goodbye-print-hello-debugger/)):

```
# Install IPython: python3 -m pip install ipython

import IPython
from traitlets.config import get_config

cfg = get_config()
cfg.InteractiveShellEmbed.colors = "Linux"  # syntax highlighting
cfg.InteractiveShellEmbed.confirm_exit = False

alias interacti IPython.embed(config=cfg)  # I replaced `interacti` with `ii` 
```

## In Jupyter Notebooks

In jupyter notebooks you can start the debugger as above, but you can also use the `%debug` magic.
It works like this:

1. Get an error in a cell
2. Run `%debug` in another cell to start the debugger the error point of last run cell
