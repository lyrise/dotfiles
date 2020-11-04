#!/bin/sh

set -u

current_dir=$(
    cd $(dirname $0)
    pwd
)
dotfiles_dir=$HOME/.dotfiles

rm -r $dotfiles_dir
mkdir $dotfiles_dir

for f in $(find ./linux -type f); do
    target=$dotfiles_dir/$(basename $f)
    cp "$f" "$target"
    ln -snfv $target ~/
done

echo "dotfiles setup finished!"
