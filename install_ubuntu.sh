#!bin/zsh

# base install
zsh install.sh
. ~/.zshrc

# dotnet
wget -q https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo add-apt-repository universe
sudo apt update
sudo apt install -y apt-transport-https
sudo apt update
sudo apt install -y dotnet-sdk-3.1

# rust
curl https://sh.rustup.rs -sSf | sh -s -- -q -y

# goenv
git clone https://github.com/syndbg/goenv.git $HOME/.goenv

# zplug
git clone https://github.com/zplug/zplug $HOME/.zplug

# tools
cargo install exa bat sd fd-find dutree
