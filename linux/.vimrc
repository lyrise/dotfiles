set clipboard+=unnamed
set clipboard+=autoselect

let mapleader = ","

inoremap <C-k> <UP>
inoremap <C-j> <DOWN>
inoremap <C-h> <LEFT>
inoremap <C-l> <RIGHT>
nnoremap k gk
nnoremap j gj
nnoremap <C-k> 5k
nnoremap <C-j> 5j
nnoremap <C-h> 0
nnoremap <C-l> $
vnoremap <C-k> 5k
vnoremap <C-j> 5j
vnoremap <C-h> ^
vnoremap <C-l> $

nnoremap <CR> i<CR><Esc>
inoremap <S-CR> <End><CR>
inoremap <C-S-CR> <UP><End><CR>
nnoremap <S-CR> <End><CR>
nnoremap <C-S-CR> <UP><End><CR>

nnoremap <C-w> :w<CR>
nnoremap <C-q> :q<CR>

nnoremap n nzz
nnoremap N Nzz
nnoremap s "_s
vnoremap s "_s
nnoremap x "_x
vnoremap x "_x

nnoremap <C-a> ggVG
inoremap <C-a> <Esc>ggVG

vnoremap $ $<LEFT>

" surround
vnoremap { S}
vnoremap ( S)
vnoremap [ S]
vnoremap " S"
vnoremap ' S'
vmap < S]<ESC>cs[>

" easymotion
nnoremap t <leader><leader>/
