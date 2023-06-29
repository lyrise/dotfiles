#!/bin/bash

set -u

current_dir=$(
    cd $(dirname $0)
    pwd
)

dotfiles_dir=$HOME/.dotfiles
rm -r $dotfiles_dir
mkdir $dotfiles_dir
(cd ./linux && cp -r ./ $dotfiles_dir)
for file in $(find $dotfiles_dir -maxdepth 1 -type f); do
    ln -snfv $file $HOME
done

nvim_user_dir=$HOME/.config/nvim/lua/user/
rm -r $nvim_user_dir
mkdir $nvim_user_dir
(cd ./linux/nvim && cp -r ./ $nvim_user_dir)

echo "dotfiles setup finished!"
