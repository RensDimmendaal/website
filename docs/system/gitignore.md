# Gitignore

## TLDR
1. `echo "_justme*" >> ~/.gitignore`
2. `git config --global core.excludesfile '~/.gitignore'`
3. Add files and folders with prefix `_justme` in any repo and they'll always be ignored

## Longer version
As a data scientist I regularly make notebooks for some scratch analysis. I don't necessarily want to delete these. However, I also don't want to commit them to the repo and share them with my collaborators. Nor do I want to keep them popping up in my 'untracked' files. I also don't want to pollute the project's `.gitignore` file with my convention of naming local notebooks.

Today I found a solution on [stackoverflow](https://stackoverflow.com/a/22906950): a local gitignore file for all you projects. To do this, we first add our preferred prefix for our private files to a global gitignore file. In my case I add `_justme*` to `~/.gitignore`. To make sure all our projects know where to find this global gitignore file we then add the following section to our `~/.gitconfig` file:

```
 [core]
     excludesfile = ~/.gitignore
```

Finally, we can test our solution by adding any file or folder that starts with `_justme*` and see that it does not occur in our untracked files. Enjoy!
