#!/bin/sh

# Install packages
sudo apt-get update
sudo apt-get install -y zsh build-essential
sudo chsh -s /bin/zsh

# Install dotfiles
sh install.sh

# Install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git $HOME/.fzf
$HOME/.fzf/install --no-key-bindings --no-completion --no-bash --no-zsh

# Install dotnet
wget -q https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo add-apt-repository universe
sudo apt-get update
sudo apt-get install -y apt-transport-https
sudo apt-get update
sudo apt-get install -y dotnet-sdk-3.1

# Install rust
curl https://sh.rustup.rs -sSf | sh -s -- -q -y

# Install goenv
git clone https://github.com/syndbg/goenv.git $HOME/.goenv

# Install zplug
git clone https://github.com/zplug/zplug $HOME/.zplug
zsh -ic 'zplug install' </dev/null

# Install NPM
sudo apt-get install -y npm

# Install tools
export PATH="$HOME/.cargo/bin:$PATH"
cargo install cargo-cache lsd bat sd fd-find dutree
npm install -g diff-so-fancy

# clean
sudo apt-get autoremove -y
sudo apt-get clean -y
sudo rm -rf /var/lib/apt/lists/*
cargo cache --remove-dir all
