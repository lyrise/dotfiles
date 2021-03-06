# デバッグ用環境変数
DEBUG=

# zshベンチマーク
# zmodload zsh/zprof && zprof

# zcompileを実施
if [ ! -f ~/.zshrc.zwc -o ~/.zshrc -nt ~/.zshrc.zwc ]; then
    zcompile ~/.zshrc
fi

# 実行環境を識別
if [ "$(uname)" = 'Darwin' ]; then
    OS='Mac'
elif [ "$(expr substr $(uname -s) 1 5)" = 'Linux' ]; then
    OS='Linux'
fi

# common
export PATH="$HOME/bin:$PATH"

# direnv
eval "$(direnv hook zsh)"

# docker
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# fzf
export PATH="$HOME/.fzf/bin:$PATH"

# dotnet
export PATH="$HOME/.dotnet/tools:$PATH"

# goenv
export GOENV_DISABLE_GOPATH=1
export GOENV_ROOT=$HOME/.goenv
export GOPATH=$HOME/.go
export PATH="$HOME/.goenv/bin:$PATH"
export PATH="$GOPATH/bin:$PATH"
eval "$(goenv init -)"

# rust
export PATH="$HOME/.cargo/bin:$PATH"

# poetry
export PATH="/home/lyrise/.local/bin:$PATH"

# vim
export EDITOR=vim

# エイリアス集
alias ll='lsd -al --date "+%F %T"'
# alias grep='grep --color=always'
alias k='kubectl'
alias d='docker'
alias dc='docker-compose'
alias g='git'
alias g-pr='git pull-request'

if [ $OS = 'Linux' ]; then
    alias pbcopy='xclip -selection clipboard'
    alias pbpaste='xclip -selection clipboard -o'
fi

# 履歴の保存先
HISTFILE=$HOME/.zsh-history
# メモリに展開する履歴の数
HISTSIZE=100000
# 保存する履歴の数
SAVEHIST=100000

# 補完機能の強化
autoload -Uz compinit
compinit

# コアダンプサイズを制限
limit coredumpsize 102400
# 出力の文字列末尾に改行コードが無い場合でも表示
unsetopt promptcr
# Emacsライクキーバインド設定
bindkey -e

# 色を使う
setopt prompt_subst
# ビープを鳴らさない
setopt nobeep
# 内部コマンド jobs の出力をデフォルトで jobs -l にする
setopt long_list_jobs
# 補完候補一覧でファイルの種別をマーク表示
setopt list_types
# サスペンド中のプロセスと同じコマンド名を実行した場合はリジューム
setopt auto_resume
# 補完候補を一覧表示
setopt auto_list
# 直前と同じコマンドをヒストリに追加しない
setopt hist_ignore_dups
# cd 時に自動で push
setopt auto_pushd
# 同じディレクトリを pushd しない
setopt pushd_ignore_dups
# ファイル名で #, ~, ^ の 3 文字を正規表現として扱う
setopt extended_glob
# TAB で順に補完候補を切り替える
setopt auto_menu
# zsh の開始, 終了時刻をヒストリファイルに書き込む
setopt extended_history
# =command を command のパス名に展開する
setopt equals
# --prefix=/usr などの = 以降も補完
setopt magic_equal_subst
# ヒストリを呼び出してから実行する間に一旦編集
setopt hist_verify
# ファイル名の展開で辞書順ではなく数値的にソート
setopt numeric_glob_sort
# 出力時8ビットを通す
setopt print_eight_bit
# ヒストリを共有
setopt share_history
# 補完候補のカーソル選択を有効に
zstyle ':completion:*:default' menu select=2
# 補完候補の色づけ
#eval `dircolors`
export ZLS_COLORS=$LS_COLORS
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}
# ディレクトリ名だけでcd
setopt auto_cd
# カッコの対応などを自動的に補完
setopt auto_param_keys
# ディレクトリ名の補完で末尾の / を自動的に付加し、次の補完に備える
setopt auto_param_slash
# スペルチェック
setopt correct
# {a-c} を a b c に展開する機能を使えるようにする
setopt brace_ccl
# Ctrl+S/Ctrl+Q によるフロー制御を使わないようにする
setopt NO_flow_control
# コマンドラインの先頭がスペースで始まる場合ヒストリに追加しない
setopt hist_ignore_space
# コマンドラインでも # 以降をコメントと見なす
setopt interactive_comments
# ファイル名の展開でディレクトリにマッチした場合末尾に / を付加する
setopt mark_dirs
# history (fc -l) コマンドをヒストリリストから取り除く。
setopt hist_no_store
# 補完候補を詰めて表示
setopt list_packed
# 最後のスラッシュを自動的に削除しない
setopt noautoremoveslash
# ヒストリーに重複を表示しない
setopt histignorealldups
# 履歴をインクリメンタルに追加
setopt inc_append_history
# 余分な空白は詰めて記録
setopt hist_reduce_blanks
# cdrコマンドで履歴にないディレクトリにも移動可能に
# zstyle ":chpwd:*" recent-dirs-default true
# cdrコマンドを有効 ログアウトしても有効なディレクトリ履歴
# cdr タブでリストを表示
autoload -Uz add-zsh-hook
autoload -Uz chpwd_recent_dirs cdr
add-zsh-hook chpwd chpwd_recent_dirs
# 区切り文字の設定
autoload -Uz select-word-style
select-word-style default
zstyle ':zle:*' word-chars "_-./;@"
zstyle ':zle:*' word-style unspecified

# zplugのセットアップ
source ~/.zplug/init.zsh
zplug 'zplug/zplug', hook-build:'zplug --self-manage'
# cdの強化
zplug 'b4b4r07/enhancd', use:init.sh
# fzfのセットアップ
# 'junegunn/fzf-bin'のインストールに失敗するようになった
#zplug 'junegunn/fzf-bin', from:gh-r, as:command, rename-to:fzf
zplug 'junegunn/fzf', use:shell/key-bindings.zsh
zplug 'junegunn/fzf', use:shell/completion.zsh
# シンタックスハイライト
zplug 'zsh-users/zsh-syntax-highlighting', defer:2
# コマンド補完
zplug 'zsh-users/zsh-autosuggestions', lazy:true
zplug 'zsh-users/zsh-completions', lazy:true
zplug 'zsh-users/zsh-history-substring-search', lazy:true
zplug 'chrissicool/zsh-256color', lazy:true
zplug 'kwhrtsk/docker-fzf-completion', lazy:true
zplug 'docker/cli', use:'contrib/completion/zsh/_docker', lazy:true
zplug 'docker/compose', use:'contrib/completion/zsh/_docker-compose', lazy:true
# gitのショートカット
# forgit_log="g-log"
# forgit_diff="g-diff"
# forgit_add="g-add"
# forgit_reset_head="g-reset-hard"
# forgit_ignore="g-ignore"
# forgit_restore="g-restore"
# forgit_clean="g-clean"
# forgit_stash_show="g-stash-show"
# zplug 'wfxr/forgit'
# zのセットアップ
zplug 'rupa/z', use:z.sh
# コマンドの実行時間を表示
zplug "popstas/zsh-command-time"
# kube-ps1のセットアップ
zplug 'jonmosco/kube-ps1'
# プラグインのインストール
# if ! zplug check --verbose; then
#     printf "Install? [y/N]: "
#     if read -q; then
#         echo
#         zplug install
#     fi
# fi
zplug load

# プロンプトの設定
PROMPT=""
## ユーザー名とホスト名
PROMPT=$PROMPT$'%{\e[38;5;246m%}%n@%m%{${reset_color}%} '
## カレントディレクトリパスの表示
PROMPT=$PROMPT$'%{\e[38;5;2m%}%~%{${reset_color}%}'
## Gitのブランチ名の表示
# autoload -Uz vcs_info
# setopt prompt_subst
# zstyle ':vcs_info:git:*' check-for-changes true
# zstyle ':vcs_info:git:*' stagedstr "%F{yellow}!"
# zstyle ':vcs_info:git:*' unstagedstr "%F{red}+"
# zstyle ':vcs_info:git*' formats " %{$fg[blue]%}%b%{$reset_color%}%m%u%c%{$reset_color%}"
# zstyle ':vcs_info:git*' actionformats "%s  %r/%S %b %m%u%c "
# precmd () { vcs_info }
# PROMPT=$PROMPT'${vcs_info_msg_0_}'
## kubernetes情報の表示
source $ZPLUG_REPOS/jonmosco/kube-ps1/kube-ps1.sh
KUBE_PS1_SYMBOL_ENABLE='false'
KUBE_PS1_PREFIX=' ['
KUBE_PS1_SUFFIX=']'
KUBE_PS1_DIVIDER=':'
KUBE_PS1_CTX_COLOR=red
KUBE_PS1_NS_COLOR=cyan
PROMPT=$PROMPT'$(kube_ps1)'
PROMPT=$PROMPT"
> "

# コマンド実行前に時刻を表示
preexec () {
    echo -e "Execution start: $(date +"%Y/%m/%d %H:%M:%S")"
}

# zsh-command-timeの設定
ZSH_COMMAND_TIME_MIN_SECONDS=1
ZSH_COMMAND_TIME_MSG="Execution time: %s"

# fzfの設定
export FZF_DEFAULT_OPTS="--height 80% --layout=reverse --border --inline-info --exact --no-sort"
export FZF_COMPLETION_TRIGGER=','

# zの履歴をfzfで検索
z-fzf() {
    local res=$(z | tac | cut -c 12- | awk '!a[$0]++' | fzf)
    if [ -n "$res" ]; then
        BUFFER+="cd $res"
        zle accept-line
    else
        return 1
    fi
}
zle -N z-fzf
bindkey '^z' z-fzf

# ヒストリーをfzfで検索
history-fzf() {
    local tac=${commands[tac]:-"tail -r"}
    print -z $( ([ -n "$ZSH_NAME" ] && fc -l 1 || history) | sed 's/ *[0-9]* *//' | eval $tac | awk '!a[$0]++' | fzf +s)
    zle accept-line
}
zle -N history-fzf
bindkey '^r' history-fzf

# killするプロセスをfzfで検索
kill-fzf() {
    if [ $OS = 'Mac' ]; then
        local list=$(ps auxwl)
        local head=$(echo $list | head -n 1)
        local pid=$(echo $list | sed 1d | fzf -m --header="$head" | awk '{print $2}')

        if [ "$pid" != "" ]
        then
            echo $pid | xargs sudo kill -${1:-9}
        fi
    elif [ $OS = 'Linux' ]; then
        local list=$(ps all)
        local head=$(echo $list | head -n 1)
        local pid=$(echo $list | sed 1d | fzf -m --header="$head" | awk '{print $3}')

        if [ "$pid" != "" ]
        then
            echo $pid | xargs sudo kill -${1:-9}
        fi
    fi
    zle accept-line
}
zle -N kill-fzf
bindkey '^x' kill-fzf

# ファイルをfzfで検索
rg-file() {
    if [ ! "$#" -gt 0 ]; then echo "Need a string to search for!"; return 1; fi
    rg --files-with-matches --no-messages "$1" | fzf --preview "highlight -O ansi -l {} 2> /dev/null | rg --colors 'match:bg:yellow' --ignore-case --pretty --context 10 '$1' || rg --ignore-case --pretty --context 10 '$1' {}"
}
zle -N rg-file
bindkey '^f' rg-file

# アタッチするDockerコンテナをfzfで検索
d-attach() {
    local cid
    cid=$(docker ps -a | sed 1d | fzf -1 -q "$1" | awk '{print $1}')

    [ -n "$cid" ] && docker start "$cid" && docker attach "$cid"
}

# 停止するDockerコンテナをfzfで検索
d-stop() {
    local cid
    cid=$(docker ps | sed 1d | fzf -q "$1" | awk '{print $1}')

    [ -n "$cid" ] && docker stop "$cid"
}

# 削除するDockerコンテナをfzfで検索
d-rm() {
    local cid
    cid=$(docker ps -a | sed 1d | fzf -q "$1" | awk '{print $1}')

    [ -n "$cid" ] && docker rm -f "$cid"
}

# すべてのDockerコンテナを削除
d-rm-all() {
    docker container rm $(docker ps -aq) -f
}

# checkout git branch or tag with previews
g-checkout() {
    local tags branches target
    branches=$(
        git --no-pager branch --all \
            --format="%(if)%(HEAD)%(then)%(else)%(if:equals=HEAD)%(refname:strip=3)%(then)%(else)%1B[0;34;1mbranch%09%1B[m%(refname:short)%(end)%(end)" \
        | sed '/^$/d') || return
    tags=$(
        git --no-pager tag | awk '{print "\x1b[35;1mtag\x1b[m\t" $1}') || return
    target=$(
        (echo "$branches"; echo "$tags") |
        fzf --no-hscroll --no-multi -n 2 \
            --ansi --preview="git --no-pager log -150 --pretty=format:%s '..{2}'") || return
    git checkout $(awk '{print $2}' <<<"$target" )
}
zle -N g-checkout
bindkey '^b' g-checkout

alias glNoGraph='git log --color=always --format="%C(auto)%h%d %s %C(black)%C(bold)%cr% C(auto)%an" "$@"'
_gitLogLineToHash="echo {} | grep -o '[a-f0-9]\{7\}' | head -1"
_viewGitLogLine="$_gitLogLineToHash | xargs -I % sh -c 'git show --color=always % | diff-so-fancy'"

# checkout git commit with previews
g-checkout-commit() {
    local commit
    commit=$( glNoGraph |
        fzf --no-sort --reverse --tiebreak=index --no-multi \
            --ansi --preview="$_viewGitLogLine" ) &&
    git checkout $(echo "$commit" | sed "s/ .*//")
}

# Custom
if [ -e ~/.zshrc.include ]; then
    . ~/.zshrc.include
fi

# if (which zprof > /dev/null 2>&1) ;then
#   zprof
# fi
