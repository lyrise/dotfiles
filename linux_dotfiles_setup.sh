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

for f in $(find $dotfiles_dir -maxdepth 1 -type f); do
    ln -snfv $f $HOME
done

nvim_user_dir=$HOME/.config/nvim/lua/user/
rm -r $nvim_user_dir
mkdir $nvim_user_dir

for f in $(find $dotfiles_dir/nvim/lua/user/ -maxdepth 1 -type f); do
    ln -snfv $f $nvim_user_dir
done

echo "dotfiles setup finished!"
