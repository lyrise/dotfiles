#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

sudo apt-get update

# install packages
sudo apt-get install -y \
    curl wget \
    zip unzip \
    git zsh build-essential \
    openssl libssl-dev \
    libbz2-dev zlib1g-dev \
    libsqlite3-dev \
    postgresql-client libpq-dev \
    pkg-config \
    direnv \
    fd-find ripgrep lsd

# set default shell
sudo chsh -s $(which zsh)

# install zinit
mkdir ~/.zinit
git clone --depth 1 https://github.com/zdharma-continuum/zinit.git ~/.zinit/bin

# install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install --no-key-bindings --no-completion --no-bash --no-zsh

# install mise
curl https://mise.run | sh

# install mise managed tools
"$HOME/.local/bin/mise" install

# install rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -q -y
