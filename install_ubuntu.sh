#!/bin/sh

# dotfiles
sh install.sh

# dotnet
wget -q https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo add-apt-repository universe
sudo apt-get update
sudo apt-get install -y apt-transport-https
sudo apt-get update
sudo apt-get install -y dotnet-sdk-3.1

# rust
curl https://sh.rustup.rs -sSf | sh -s -- -q -y

# goenv
git clone https://github.com/syndbg/goenv.git $HOME/.goenv

# zplug
git clone https://github.com/zplug/zplug $HOME/.zplug

# tools
export PATH=$HOME/.cargo/bin:$PATH
cargo install exa bat sd fd-find dutree

# clean
sudo apt autoremove -y
sudo apt clean -y
sudo rm -rf /var/lib/apt/lists/*
