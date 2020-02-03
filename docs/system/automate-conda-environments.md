# Automate Conda Environments

If you're aware of the benefits of having a separate conda environment for each project, but are too lazy to create and activate it all the time. Then the aliases for your .bashrc / .zshrc below might help.

When start a new project i simply type `mkconda` in my project directory which creates a new conda environment, with the same name as the project root directory. To remove the conda environment I run `rmconda`. When I return later to the project I can activate the environment by running `ca`. To setup jupyterlab \*within\* an environment I can run `mkjupy`. I also have commands to quickly open jupyter lab `jl` and other environments like vscode.

```bash
# Make conda environment
function mkconda() {
    dir=$(echo $PWD | rev | cut -d/ -f1 | rev)
    conda create -n ${dir} -y python=3.7
    conda deactivate
    conda activate ${dir}
}

# Remove conda environment
function rmconda() {
    dir=$(echo $PWD | rev | cut -d/ -f1 | rev)
    conda deactivate
    conda remove -n ${dir} --all
}

# Activate conda environment
function ca() {
    dir=$(echo $PWD | rev | cut -d/ -f1 | rev)
    conda deactivate
    conda activate ${dir}
}

function mkjupy() {
     pip install jupyterlab voila jupyterlab_code_formatter black
     jupyter labextension install @jupyter-widgets/jupyterlab-manager \
                              @jupyterlab/toc \
                              @ryantam626/jupyterlab_code_formatter \
                              @jupyter-voila/jupyterlab-preview \
                              --no-build
     jupyter serverextension enable --py jupyterlab_code_formatter
     jupyter lab build
 }

# Python aliases
alias ci="code-insiders ."
alias jn="jupyter notebook"
alias jl="jupyter lab"
alias ip="ipython"
```

