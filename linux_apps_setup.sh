#!/bin/bash

sudo apt-get update

# install packages
sudo apt-get install -y \
    curl wget \
    git zsh build-essential \
    openssl libssl-dev \
    libbz2-dev zlib1g-dev \
    libsqlite3-dev \
    postgres-client libpq-dev \
    direnv \
    npm

# set default shell
sudo chsh -s /bin/zsh

# install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git $HOME/.fzf
$HOME/.fzf/install --no-key-bindings --no-completion --no-bash --no-zsh

# install rust
curl https://sh.rustup.rs -sSf | sh -s -- -q -y
export PATH="$HOME/.cargo/bin:$PATH"

# install goenv
git clone https://github.com/syndbg/goenv.git $HOME/.goenv
export GOENV_DISABLE_GOPATH=1
export GOENV_ROOT=$HOME/.goenv
export GOPATH=$HOME/.go
export PATH="$HOME/.goenv/bin:$PATH"
export PATH="$GOPATH/bin:$PATH"
eval "$(goenv init -)"
GOLANG_VERSION="1.14.4"
goenv install $GOLANG_VERSION
goenv global $GOLANG_VERSION
goenv rehash

# install pyenv
git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
PYTHON_VERSION="3.9.0"
pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION
pyenv rehash

# install tools
sudo apt-get install -y fd-find ripgrep
cargo install cargo-cache bat dutree lsd
sudo npm install -g diff-so-fancy

# install zplug
git clone https://github.com/zplug/zplug $HOME/.zplug
zsh -ic 'zplug install' </dev/null

# clean
sudo apt-get autoremove -y
sudo apt-get clean -y
sudo rm -rf /var/lib/apt/lists/*
cargo cache --remove-dir all
