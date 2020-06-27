#!/bin/sh

set -u

current_dir=$(
    cd $(dirname $0)
    pwd
)
dotfiles_dir=$HOME/.dotfiles

rm -r $dotfiles_dir
mkdir $dotfiles_dir

for f in .??*; do
    [ "$f" = ".git" ] && continue

    cp "$f" $dotfiles_dir/"$f"
    ln -snfv $dotfiles_dir/"$f" ~/
done

echo "dotfiles setup finished!"
