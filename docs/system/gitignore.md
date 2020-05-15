# Gitignore

As a data scientist I regularly make notebooks for some scratch analysis. I don't necessarily want to delete these, but I also don't want to commit them to the repo and share them with my collaborators, nor do I want to keep them popping up in my 'untracked' files. I also don't want to pollute the project's `.gitignore` file with my convention of naming local notebooks.

Today I found a solution on [stackoverflow](https://stackoverflow.com/a/22906950): a local .gitignore file for all you projects. All you need to do is:

1. Add things you want to ignore to your `~/.gitignore`, for example `Untitled*.ipynb`
2. Make sure your `~/.gitconfig` file is aware of your `~/.gitignore` file. To do this run: `git config --global core.excludesfile '~/.gitignore'`. 
3. If you're curious: take a look at `~/.gitconfig` what happened at step 2.

I have`_*.ipynb` rather than `Untitled*.ipynb`, in my `~/.gitignore` because it prompts me to rename those pesky `Untitled*.ipynb` with more descriptive titles, even when its something I'm trying out just for myself.
