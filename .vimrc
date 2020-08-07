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
vnoremap <C-k> 5gk
vnoremap <C-j> 5gj
vnoremap <C-h> 5h
vnoremap <C-l> 5l
nnoremap <leader>dw di<leader>w
nnoremap <leader>cw ci<leader>w

nnoremap <leader>s <leader><leader>/
inoremap { {}<LEFT>
inoremap [ []<LEFT>
inoremap < <><LEFT>
inoremap ( ()<LEFT>
inoremap " ""<LEFT>
inoremap ' ''<LEFT>

nnoremap <CR> i<CR><Esc>

nnoremap <C-w> :w!<CR>

nnoremap n nzz
nnoremap N Nzz
nnoremap s "_s
nnoremap x "_x

nnoremap <leader>P "0P
nnoremap <leader>p "0p
vnoremap p "_dp
vnoremap P "_dP

nnoremap <C-a> ggvG
inoremap <C-a> <Esc>ggvG

vnoremap < <gv
vnoremap > >gv
