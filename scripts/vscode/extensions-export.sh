code --list-extensions | tail -n +2 | xargs -L 1 echo code --install-extension | sort > vscode_import.sh
