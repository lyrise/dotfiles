#!/bin/bash

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
export PATH="/opt/homebrew/bin:$PATH"

# install pyenv
brew install pyenv

# install goenv
brew install --HEAD goenv

# install zplug
mkdir ~/.zinit
git clone --depth 1 https://github.com/zdharma-continuum/zinit.git ~/.zinit/bin

# install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install --no-key-bindings --no-completion --no-bash --no-zsh
