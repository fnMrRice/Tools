#!/bin/bash

USER=$(whoami)
cd ~
lsb_release  -c
VERSION=$(echo $(lsb_release -c) | sed 's/\t//g' | cut -d ":" -f2 | sed 's/ //g')
# 换源
 # 中科大 https 源
echo "# 默认注释了源码仓库，如有需要可自行取消注释
deb https://mirrors.ustc.edu.cn/ubuntu/ "$VERSION" main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ "${VERSION}" main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ "${VERSION}"-updates main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ "${VERSION}"-updates main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ "${VERSION}"-backports main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ "${VERSION}"-backports main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ "${VERSION}"-security main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ "${VERSION}"-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.ustc.edu.cn/ubuntu/ "${VERSION}"-proposed main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ "${VERSION}"-proposed main restricted universe multiverse
" > ~/sources.list.ustc
mv ~/sources.list.ustc /etc/apt/sources.list.ustc
 # 清华 https 源
echo "# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ "${VERSION}" main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ "${VERSION}" main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ "${VERSION}"-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ "${VERSION}"-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ "${VERSION}"-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ "${VERSION}"-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ "${VERSION}"-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ "${VERSION}"-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ "${VERSION}"-proposed main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ "${VERSION}"-proposed main restricted universe multiverse
" > ~/sources.list.tsinghua
mv ~/sources.list.tsinghua /etc/apt/sources.list.tsinghua
 # 备份
sudo mv /etc/apt/sources.list /etc/apt/sources.list.origin
 # 使用清华源
sudo cp /etc/apt/sources.list.ustc /etc/apt/sources.list
 # 更新软件源
sudo apt update
sudo apt upgrade -y

# 安装软件
sudo apt install vim wget git screen zsh fonts-powerline python python-pip python3 python3-pip mysql-server shadowsocks firefox nodejs npm -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i ./google-chrome-stable_current_amd64.deb
sudo apt -f install -y
sudo rm -rf ./google-chrome-stable_current_amd64.deb
sudo apt autoremove -y
sudo -H pip3 install --upgrade pip
 # pip install
sudo -H pip3 install requests beautifulsoup4 flask flask_script pymysql flask_sqlalchemy mysqlclient selenium pillow

# 中文语言
sudo apt install language-pack-zh-hans language-pack-zh-hans-base fonts-wqy-zenhei -y
sudo update-locale LANG=zh_CN.UTF-8

# alias display=DISPLAY=:0.0

# 安装oh my zsh
git clone https://github.com/robbyrussell/oh-my-zsh.git
nohup ~/oh-my-zsh/tools/install.sh
sudo apt install autojump
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone git://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
sudo chsh -s $(which zsh)
echo "# Add default user
DEFAULT_USER="${USER}"
BULLETTRAIN_CONTEXT_DEFAULT_USER="${USER}"

# Solve autojump error
# unsetopt BG_NICE

# Set 256 colors mode
export TERM=xterm-256color

# Alias
alias chrome=google-chrome-stable
" >> ~/.zshrc
source ~/.zshrc