#!/bin/bash

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
    direnv

# set default shell
sudo chsh -s $(which zsh)

# create app dir
mkdir ~/app

# install goenv
git clone https://github.com/syndbg/goenv.git ~/.goenv

# install zplug
mkdir ~/.zinit
git clone --depth 1 https://github.com/zdharma-continuum/zinit.git ~/.zinit/bin

# install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install --no-key-bindings --no-completion --no-bash --no-zsh

# Install sdkman
curl -s "https://get.sdkman.io" | bash

# Install sbt
SBT_VERSION=1.8.0
curl -L -o sbt-${SBT_VERSION}.deb https://repo.scala-sbt.org/scalasbt/debian/sbt-${SBT_VERSION}.deb
sudo dpkg -i sbt-${SBT_VERSION}.deb
rm sbt-${SBT_VERSION}.deb

# install volta
curl https://get.volta.sh | bash

# install rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -q -y

# install pyenv
git clone --depth 1 https://github.com/pyenv/pyenv.git ~/.pyenv

# install fd-find
sudo apt-get install -y fd-find

# install ripgrep
sudo apt-get install -y ripgrep

# install lsd
sudo apt-get install -y lsd

# install kustomize
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
mv ./kustomize ~/bin
