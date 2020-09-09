#!/bin/sh

# Install packages
sudo apt-get update
sudo apt-get install -y git zsh build-essential gcc make openssl libssl-dev libbz2-dev libreadline-dev libsqlite3-dev zlib1g-dev
sudo chsh -s /bin/zsh

# Install dotfiles
sh install.sh

# Install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git $HOME/.fzf
$HOME/.fzf/install --no-key-bindings --no-completion --no-bash --no-zsh

# Install dotnet
wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update; \
  sudo apt-get install -y apt-transport-https && \
  sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-3.1
rm packages-microsoft-prod.deb

# Install rust
curl https://sh.rustup.rs -sSf | sh -s -- -q -y
export PATH="$HOME/.cargo/bin:$PATH"

# Install goenv
git clone https://github.com/syndbg/goenv.git $HOME/.goenv
export GOENV_DISABLE_GOPATH=1
export GOENV_ROOT=$HOME/.goenv
eval "$(goenv init -)"
export GOPATH=$HOME/.go
export PATH="$HOME/.goenv/bin:$PATH"
export PATH="$GOPATH/bin:$PATH"
GOLANG_VERSION="1.14.4"
goenv install $GOLANG_VERSION
goenv global $GOLANG_VERSION
goenv rehash

# Install pyenv
git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
PYTHON_VERSION="3.8.3"
pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION
pyenv rehash

# Install npm
sudo apt-get install -y npm

# Install tools
cargo install cargo-cache lsd bat sd fd-find dutree
npm install -g diff-so-fancy

# Install zplug
git clone https://github.com/zplug/zplug $HOME/.zplug
zsh -ic 'zplug install' </dev/null

# clean
sudo apt-get autoremove -y
sudo apt-get clean -y
sudo rm -rf /var/lib/apt/lists/*
cargo cache --remove-dir all
