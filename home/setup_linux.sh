#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

dotfiles_dir=$HOME/.dotfiles
rm -rf "$dotfiles_dir"
mkdir "$dotfiles_dir"
(cd ./linux && cp -r ./ "$dotfiles_dir")
for file in $(find "$dotfiles_dir" -maxdepth 1 -type f); do
    ln -snfv "$file" "$HOME"
done

mkdir -p "$HOME/.config/mise"
ln -snfv "$dotfiles_dir/.config/mise/config.toml" "$HOME/.config/mise/config.toml"

cp -r ./linux/nvim/plugins/* "$HOME/.config/nvim/lua/plugins/"

echo "dotfiles setup finished!"
