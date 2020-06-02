# Jupyter Restart and Run All

I like being sure that my notebooks work well when run from start to finish.
To that end I use this shortcut:

```
{
  "shortcuts": [
    {
      "command": "runmenu:restart-and-run-all",
      "keys": [
        "Ctrl Alt R"
      ],
      "selector": "[data-jp-code-runner]",
      "title": "Restart Kernel and Run All",
      "category": "Run Menu"
    },
    {
      "command": "notebook:change-cell-to-raw",
      "keys": [
        "R"
      ],
      "disabled": true,
      "selector": ".jp-Notebook:focus"
    }
  ]
}
```

You can add it to your jupyter lab setup by going to `Settings > Advanced Settings Editor > Keyboard Shortcuts` and pasting this into the `User Preferences` pane.
