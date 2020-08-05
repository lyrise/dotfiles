nnoremap : ;
nnoremap ; :
vnoremap : ;
vnoremap ; :

inoremap kk <Esc>
inoremap jj <Esc>

nmap <UP> gk
nmap <DOWN> gj
inoremap <C-k> <UP>
inoremap <C-j> <DOWN>
inoremap <C-h> <LEFT>
inoremap <C-l> <RIGHT>
nnoremap k gk
nnoremap j gj
nnoremap <C-k> 5gk
nnoremap <C-j> 5gj
nnoremap <C-h> 5h
nnoremap <C-l> 5l
nnoremap <leader>dw di<leader>w
nnoremap <leader>cw ci<leader>w

nnoremap <leader>s <leader><leader>/
inoremap { {}<LEFT>
inoremap [ []<LEFT>
inoremap < <><LEFT>
inoremap ( ()<LEFT>
inoremap " ""<LEFT>
inoremap ' ''<LEFT>

inoremap <C-d> <DEL>
inoremap <C-r> <CR>
inoremap <S-CR> <End><CR>
inoremap <C-S-CR> <UP><End><CR>
nnoremap <C-d> <DEL>
nnoremap <C-r> <CR>
nnoremap <S-CR> <End><CR>
nnoremap <C-S-CR> <UP><End><CR>

nnoremap <C-w> :w!<CR>

nnoremap n nzz
nnoremap N Nzz
nmap s "_s
nmap x "_x

nnoremap <leader>P "0P
nnoremap <leader>p "0p
vnoremap P "_dP
vnoremap p "_dp

nnoremap <C-a> ggvG
inoremap <C-a> <Esc>ggvG

vnoremap < <gv
vnoremap > >gv
