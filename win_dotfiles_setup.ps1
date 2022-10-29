Remove-Item -Path $PROFILE -Force
New-Item -Type SymbolicLink $PROFILE -Value $PSScriptRoot\windows\pwsh_profile.ps1

Remove-Item -Path $HOME\.vimrc -Force
New-Item -Type SymbolicLink $HOME\.vimrc -Value $PSScriptRoot\linux\.vimrc

Remove-Item -Path $HOME\.vsvimrc -Force
New-Item -Type SymbolicLink $HOME\.vsvimrc -Value $PSScriptRoot\windows\.vsvimrc

Remove-Item -Path $HOME\.ideavimrc -Force
New-Item -Type SymbolicLink $HOME\.ideavimrc -Value $PSScriptRoot\windows\.ideavimrc
