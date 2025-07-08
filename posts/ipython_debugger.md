---
title: "IPython debugger"
author: "Rens Dimmendaal"
date: "2025-06-18"
tags: ["Data Science", "AI", "Chatbots", "NLP", "Debugging"]
draft: true
---

Shell sage is an amazing tool that lets you chat with an LLM inside your terminal.
It automatically loads in your shell history into the context window so the LLM knows what you've been doing.
Combine with with Ipython and you've got an interactive python environment to pair in with the LLM.
Add ipdb and you've got an AI enabled debugger.

## 1. Install ipdb and ipython

```bash
pip install ipdb ipython shell-sage
```

## 2. Setup the debugger defaults

```bash
# fpath: ~/.pdbrc
import IPython
from traitlets.config import get_config

cfg = get_config()

# enable syntax highlighting
cfg.InteractiveShellEmbed.colors = "Linux"
cfg.InteractiveShellEmbed.confirm_exit = False

alias ii IPython.embed(config=cfg)
```

## 3. Use it with `breakpoint()`

You can use the `breakpoint()` function to set a breakpoint in your code.

Sample python script:

```python
# fpath: main.py
a = "Hello, world!"
breakpoint()
print(a)
```

Run the script:
```bash
python main.py
```

You'll see the debugger start and stop at the breakpoint.

Youll be in ipdb which already has some nice features:

- syntax highlighting
- auto-completion

## 5. Jump into a fully fledged IPython shell from the debugger

You can use the `ii` command to jump into a fully fledged IPython shell.
...and you can even jump back into ipdb with ctr+D or by typing `exit`.

## 6. Run ipdb without breakpoint

You can run ipdb without breakpoint by using the `ipdb` command.

```bash
ipdb main.py
```

