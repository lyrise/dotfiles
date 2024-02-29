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

echo "dotfiles setup finished!"
