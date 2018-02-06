#!/bin/bash
# 换源,安装软件
sudo mv /etc/apt/sources.list /etc/apt/sources.list.origin
sudo echo "# 默认注释了源码仓库，如有需要可自行取消注释
deb https://mirrors.ustc.edu.cn/ubuntu/ xenial main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ xenial main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ xenial-security main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ xenial-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.ustc.edu.cn/ubuntu/ xenial-proposed main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ xenial-proposed main restricted universe multiverse
" > /etc/apt/sources.list.ustc
sudo echo "# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-proposed main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-proposed main restricted universe multiverse
" > /etc/apt/sources.list.tsinghua
sudo cp /etc/apt/sources.list.ustc /etc/apt/sources.list
sudo apt update
sudo apt upgrade -y
sudo apt install zsh git screen python3-pip mysql-server wget ctags -y
sudo apt autoremove -y
sudo -H pip3 install --upgrade pip

#安装中文
sudo apt install fonts-powerline -y
sudo apt install language-pack-zh-hans language-pack-zh-hans-base -y
sudo apt install `check-language-support -l zh` -y
sudo apt install ttf-wqy-zenhei -y
cd ~/
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt -f install
sudo localectl set-locale LANG=zh_CN.UTF-8

# 安装oh my zsh
cd ~/
git clone https://github.com/robbyrussell/oh-my-zsh.git
sudo ~/oh-my-zsh/tools/install.sh
USER=whoami
sudo chown  -hR $USER:$USER ~/*
chsh -s $(which zsh)
sudo chsh -s $(which zsh)
echo "# Add default user
DEFAULT_USER=Dora
BULLETTRAIN_CONTEXT_DEFAULT_USER=Dora

# Solve autojump error
unsetopt BG_NICE

# Set 256 colors mode
export TERM=xterm-256color
" >> ~/.zshrc
sudo apt install autojump
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone git://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions

# Vim配置
mkdir ~/.vim
mkdir ~/.vim/bundle
git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
echo "filetype off
set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

if filereadable(expand(\"~/.vimrc.bundles\"))
  source ~/.vimrc.bundles
endif

\" 显示行号
set nu
\" 启动时隐去援助提示
set shortmess=atI
\" 语法高亮
syntax on
\" 使用vim的键盘模式
\" set nocompatible
\" 不需要备份
\" set nobackup
\" 没有保存或文件只读时弹出确认
set confirm
\" 鼠标可用
\" set mouse=a
\" tab缩进
set tabstop=4
\" set shiftwidth=4
\" set expandtab
set smarttab
\" 文件自动检测外部更改
set autoread
\" c文件自动缩进
set cindent
\" 自动对齐
set autoindent
\" 智能缩进
set smartindent
\" 高亮查找匹配
set hlsearch
\" 背景色
\" set background=dark
\" 显示匹配
set showmatch
\" 显示标尺，就是在右下角显示光标位置
set ruler
\" 去除vi的一致性
set nocompatible
\" 允许折叠
\" set foldenable
\" 根据语法折叠
\" set fdm=syntax
\" 手动折叠
\" set fdm=manual
\" 设置键盘映射，通过空格设置折叠
\" nnoremap <space> @=((foldclosed(line('.')<0)?'zc':'zo'))<CR>
\" 不要闪烁
\" set novisualbell
\" 启动显示状态行
set laststatus=2
\" 浅色显示当前行
\" autocmd InsertLeave * se nocul
\" 用浅色高亮当前行
autocmd InsertEnter * se cul
\" 显示输入的命令
\" set showcmd
\" 被分割窗口之间显示空白
set fillchars=vert:/
set fillchars=stl:/
set fillchars=stlnc:/\")\"
" > ~/.vimrc
echo "filetype off
set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

\" Define bundles via Github repos
\" 提供函数列表
Plugin 'taglist.vim'
\" 快速注释/去掉注释
Plugin 'scrooloose/nerdcommenter'
\" 语法检查
Plugin 'tomtom/checksyntax_vim'
\" C/C++自动补全
Plugin 'vim-scripts/OmniCppComplete'
\" 目录树
Plugin 'scrooloose/nerdtree'
\" 自动检测编码
Plugin 'mbbill/fencview'
\" CSS实时着色
Plugin 'vim-scripts/css_color.vim'
\" Markdown着色
Plugin 'hallison/vim-markdown'
\" Json高亮
Plugin 'elzr/vim-json'
\" Python缩进
Plugin 'Vimjas/vim-python-pep8-indent'
\" JS高亮
Plugin 'jelera/vim-javascript-syntax'
\" 搜索
Plugin 'yegappan/grep'
\" Base64转换
Plugin 'christianrondeau/vim-base64'
" > ~/.vimrc.bundles
vim +BundleInstall +qall

#pip install
sudo -H pip3 install flask
sudo -H pip3 install flask_script
sudo -H pip3 install pymysql
sudo -H pip3 install flask_sqlalchemy
sudo -H pip3 install selenium
sudo -H pip3 install beautifulsoup4
sudo -H pip3 install requests

# misc
echo "Digital Ocean 128.199.143.200
Amazon AWS 52.196.215.160
" > ~/myservers
ln -s /mnt/d/WORKSPACE ~/work
ln -s /mnt/g/BaiduNetdiskDownload ~/downloads
ln -s /mnt/f/Study ~/software
zsh
alias display=DISPLAY=:0.0
alias chrome=google-chrome-stable