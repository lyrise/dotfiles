#!/usr/bin/env bash
set -euo pipefail
cd $(dirname $0)

dotfiles_dir=$HOME/.dotfiles
rm -rf $dotfiles_dir
mkdir $dotfiles_dir
(cd ./linux && cp -r ./ $dotfiles_dir)
for file in $(find $dotfiles_dir -maxdepth 1 -type f); do
    ln -snfv $file $HOME
done

# rm -rf ~/.config/nvim
# git clone --depth 1 https://github.com/AstroNvim/template ~/.config/nvim
cp -r ./linux/nvim/plugins/* "$HOME/.config/nvim/lua/plugins/"

echo "dotfiles setup finished!"
