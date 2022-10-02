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
git clone --depth 1 https://github.com/zdharma-continuum/zinit.git ~/.zinit/bin

# install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install --no-key-bindings --no-completion --no-bash --no-zsh

# Install jdk
sudo apt-get install -y openjdk-11-jdk

# Install sbt
SBT_VERSION=1.6.0
curl -L -o sbt-${SBT_VERSION}.deb https://repo.scala-sbt.org/scalasbt/debian/sbt-${SBT_VERSION}.deb
sudo dpkg -i sbt-${SBT_VERSION}.deb
rm sbt-${SBT_VERSION}.deb

# install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash

# install rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -q -y
export PATH="$HOME/.cargo/bin:$PATH"

# install pyenv
git clone --depth 1 https://github.com/pyenv/pyenv.git ~/.pyenv

# install fd-find
sudo apt-get install -y fd-find

# install ripgrep
sudo apt-get install -y ripgrep

# install lsd
LSD_VERSION=0.21.0
curl -L -o lsd-${LSD_VERSION}.deb https://github.com/Peltoche/lsd/releases/download/${LSD_VERSION}/lsd_${LSD_VERSION}_amd64.deb
sudo dpkg -i lsd-${LSD_VERSION}.deb
rm lsd-${LSD_VERSION}.deb
