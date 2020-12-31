Remove-Item -Path $PROFILE -Force
New-Item -Type SymbolicLink $PROFILE -Value $PSScriptRoot\windows\pwsh_profile.ps1

Remove-Item -Path $HOME\.vimrc -Force
New-Item -Type SymbolicLink $HOME\.vimrc -Value $PSScriptRoot\linux\.vimrc

Remove-Item -Path $HOME\AppData\Local\nvim\init.vim -Force
New-Item $HOME\AppData\Local\nvim -ItemType Directory -Force
New-Item -Type SymbolicLink $HOME\AppData\Local\nvim\init.vim -Value $PSScriptRoot\linux\.vimrc
