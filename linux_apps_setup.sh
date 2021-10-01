#!/bin/bash

sudo apt-get update

# install packages
sudo apt-get install -y \
    curl wget \
    git zsh build-essential \
    openssl libssl-dev \
    libbz2-dev zlib1g-dev \
    libsqlite3-dev \
    postgresql-client libpq-dev \
    direnv

# set default shell
sudo chsh -s $(which zsh)

# install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git $HOME/.fzf
~/.fzf/install --no-key-bindings --no-completion --no-bash --no-zsh

# install rust
curl https://sh.rustup.rs -sSf | sh -s -- -q -y
export PATH="$HOME/.cargo/bin:$PATH"

# install tools
sudo apt-get install -y fd-find ripgrep
cargo install cargo-cache bat dutree lsd

# install zplug
mkdir ~/.zinit
git clone https://github.com/zdharma/zinit.git ~/.zinit/bin
