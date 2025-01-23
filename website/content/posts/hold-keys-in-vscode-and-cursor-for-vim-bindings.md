+++
author = "Rens Dimmendaal"
title = "TIL: Fix Key Repeat in VSCode/Cursor on macOS for Vim bindings"
date = "2025-01-23"
+++

By default, macOS shows accent options (é,è,ê) when holding keys - great for typing.
But it's problematic in apps like VSCode and Cursor where you may have enabled Vim bindings.
Then you want key repeat, like holding 'j' to move down in Vim. 

Here's how to enable key repeat instead:

VSCode:

```bash
defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false
```

Cursor:

```bash
defaults write com.todesktop.230313mzl4w4u92 ApplePressAndHoldEnabled -bool false
```

To revert back to accent menu:

```bash
defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool true
defaults write com.todesktop.230313mzl4w4u92 ApplePressAndHoldEnabled -bool true
```

Remember to restart the app after applying. 

Note: Cursor's unusual bundle ID is permanent due to app release constraints ([source](https://forum.cursor.com/t/cursor-bundle-identifier/779)). You can identify bundle id's yourself by running `osascript -e 'id of app "Cursor"'`
