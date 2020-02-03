# VSCode

## Complex autoformatting

I like use multiple packages for autoformatting:

* [docformatter](https://pypi.org/project/docformatter/) to autoformat docstrings
* [isort](https://pypi.org/project/isort/) to automatically sort and group imports
* [black](https://pypi.org/project/black/) to format all other things

I also like to use [flake8](https://pypi.org/project/flake8/) to check if everything is formatted the right way.

Running all these commands in sequence gets tiring so in vscode I automated that using the [Command Runner](https://marketplace.visualstudio.com/items?itemName=edonet.vscode-command-runner&ssr=false#qna) plugin.

I specify the command in my vscode settings as follows:

settings.json

```javascript
{
"command-runner.commands": {
  "docstring formatter": "conda activate ${workspaceFolderBasename} && docformatter --in-place --wrap-descriptions 88 --wrap-summaries 88 --blank ${file} && isort ${file} && black ${file} && flake8 ${file}",
  }
}
```

Note: I always name my conda environment the same as the workspace Folder Basename.

tox.ini:

```text
[flake8]
# Recommend matching the black line length (default 88),
# rather than using the flake8 default of 79:
max-line-length = 88
extend-ignore =
    # See https://github.com/PyCQA/pycodestyle/issues/373
    E203,
exclude = .tox
# If you need to ignore some error codes in the whole source code
# you can write them here
# ignore = D107
show-source = true
enable-extensions=G
docstring-convention=google
import-order-style=google
# Specify your custom package for isort.
# application-import-names = yourpackage
```

## Restart and Rerun Python Interactive

When I run things interactively I like to make sure my kernel is clean. I use the vscode [multi command](https://marketplace.visualstudio.com/items?itemName=ryuta46.multi-command) extension to chain together the restart kernel, remove all cells, and the run file interactive in sequence.

settings.json

```javascript
{
    "multiCommand.commands": [
        {
            "command": "multiCommand,interactiveRestartaAndRun",
            "sequence": [
                "python.datascience.restartkernel",
                "python.datascience.removeallcells",
                "python.datascience.runFileInteractive",
            ]
        },
        ]
}
```

Since I use it a lot I've bound it to cmd+R:

keybindings.json

```javascript
[
    {
        "key": "cmd+r",
        "command": "multiCommand,interactiveRestartaAndRun",
        "when": "editorLangId == 'python'"
    }
]
```

