# PATH と連動する path 配列を一意化し、zsh の再起動時に同じ要素を重ねない
typeset -U path PATH

# 実行環境を識別
if [ "$(uname)" = 'Darwin' ]; then
    OS='Mac'
elif [ "$(expr substr $(uname -s) 1 5)" = 'Linux' ]; then
    OS='Linux'
fi

if [ "${OS}" = 'Mac' ]; then
    # /etc/zprofile の path_helper による PATH の再構成を停止する
    unsetopt GLOBAL_RCS
    export PATH="/opt/homebrew/bin:$PATH"
fi

# common
export PATH="$HOME/bin:$PATH"

# dotenv
eval "$(direnv hook zsh)"

# docker
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# fzf
export PATH="$HOME/.fzf/bin:$PATH"

# rust
export PATH="$HOME/.cargo/bin:$PATH"

# dotnet
export PATH="$HOME/.dotnet/tools:$PATH"

# go
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# local bin
export PATH="$HOME/.local/bin:$PATH"

# vim
export EDITOR=vim
bindkey -v

# snap
export PATH=/snap/bin:$PATH

# dotnet
export PATH="$PATH:$HOME/.dotnet/tools"

# mise
# 非対話シェルでもランタイムを解決できるよう shims を PATH に追加し、対話シェルでは .zshrc の mise activate が上書きする
eval "$(mise activate zsh --shims)"

# 任意の設定を読み込む
if [ -e ~/.zshenv.local ]; then
    . ~/.zshenv.local
fi
