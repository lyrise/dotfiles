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
    pkg-config \
    direnv

# set default shell
sudo chsh -s $(which zsh)

# install zplug
mkdir ~/.zinit
git clone https://github.com/zdharma-continuum/zinit.git ~/.zinit/bin

# install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install --no-key-bindings --no-completion --no-bash --no-zsh

# Install jdk
sudo apt-get install -y openjdk-11-jdk

# Install sbt
SBT_VERSION=1.6.0
sudo curl -L -o sbt-$SBT_VERSION.deb https://repo.scala-sbt.org/scalasbt/debian/sbt-$SBT_VERSION.deb
sudo dpkg -i sbt-$SBT_VERSION.deb
sudo rm sbt-$SBT_VERSION.deb
sudo apt-get update
sudo apt-get install -y sbt

# install rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -q -y
export PATH="$HOME/.cargo/bin:$PATH"

# install pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# install tools
sudo apt-get install -y fd-find ripgrep
cargo install cargo-edit bat lsd
