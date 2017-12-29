set -e
# Set Color var
NC='\033[0m' # No Color
BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
LIGHTGRAY='\033[0;37m'
DARKGRAY='\033[1;30m'
LIGHTRED='\033[1;31m'
LIGHTGREEN='\033[1;32m'
YELLOW='\033[1;33m'
LIGHTBLUE='\033[1;34m'
LIGHTPURPLE='\033[1;35m'
LIGHTCYAN='\033[1;36m'
WHITE='\033[1;34m'

# get current dir
CURDIR=$(cd "$(dirname "$0")";pwd)
HAS_CUDA=""

if [ ! -n "$1" ]; then
    HAS_CUDA="false"
else
    HAS_CUDA="$1"
fi


sudo apt-get update
sudo apt-get upgrade # dist-upgrade

# Build compiler
sudo apt-get install build-essential

# Install Cmake
sudo apt-get install cmake

# # If has NVIDIA card; Install driver
#　# Maybe possible
case ${HAS_CUDA} in
    false)
        echo "${GREEN}If the compute does not has a NVIDIA card, ignore below informations!!!${NC}"
        echo "${RED}To install NVIDIA driver if available:${NC}"
        echo "${CYAN}Open /etc/modprobe.d/blacklist-nouveau.conf, add bellow:${NC}"
        echo "${CYAN}    blacklist nouveau${NC}"
        echo "${CYAN}    options nouveau modeset=0${NC}"
        echo "${CYAN}Then run 'sudo update-initramfs -u'${NC}"
        echo "${RED}Type 'Ctrl+Alt+F1' to install NVIDIA driver & cuda${NC}"
        echo "${RED}Before install run bellow${NC}"
        echo "${CYAN}    sudo service lightdm stop${NC}"
        echo "${RED}After install run bellow${NC}"
        echo "${CYAN}    sudo service lightdm start${NC}"
        echo "${RED}Then restart to run this shell script without param of 'true'${NC}"
        echo "${RED}Unzip cudnn package and copy the cudnn library files into CUDA's include and lib folders${NC}"
        echo "${CYAN}    sudo cp cuda/include/cudnn.h /usr/local/cuda/include${NC}"
        echo "${CYAN}    sudo cp -a cuda/lib64/libcudnn* /usr/local/cuda/lib64${NC}"
        echo "${CYAN}    sudo chmod a+r /usr/local/cuda/lib64/libcudnn*${NC}"
    ;;
    true)
        sudo echo "\nblacklist nouveau" >> /etc/modprobe.d/blacklist-nouveau.conf
        sudo echo "\noptions nouveau modeset=0" >> /etc/modprobe.d/blacklist-nouveau.conf
        sudo update-initramfs -u
        echo "${RED}Type 'Ctrl+Alt+F1' to install NVIDIA driver & cuda${NC}"
        echo "${RED}Before install run bellow${NC}"
        echo "${CYAN}    sudo service lightdm stop${NC}"
        echo "${RED}After install run bellow${NC}"
        echo "${CYAN}    sudo service lightdm start${NC}"
        echo "${RED}Then restart to run this shell script without param of 'true'${NC}"
        # Add bashrc
        echo "\nexport PATH=$PATH:/usr/local/cuda-8.0/bin" >> ~/.bashrc
        echo "\nexport CUDA_HOME=/usr/local/cuda-8.0" >> ~/.bashrc
        echo "\nexport LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-8.0/lib64:/usr/local/cuda-8.0/extras/CUPTI/lib64:/usr/lib/nvidia" >> ~/.bashrc
    ;;
    *)
    ;;
esac
# sudo update-initramfs -u
# sudo apt-get install nvidia-384
# # Install cuda & cudnn
# sudo sh "cuda***.run"
# #　copy the library files into CUDA's include and lib folders
# sudo cp cuda/include/cudnn.h /usr/local/cuda/include
# sudo cp -a cuda/lib64/libcudnn* /usr/local/cuda/lib64
# sudo chmod a+r /usr/local/cuda/lib64/libcudnn*
# # Add bashrc
# echo "\nexport PATH=$PATH:/usr/local/cuda-8.0/bin" >> ~/.bashrc
# echo "\nexport CUDA_HOME=/usr/local/cuda-8.0" >> ~/.bashrc
# echo "\nexport LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-8.0/lib64:/usr/local/cuda-8.0/extras/CUPTI/lib64:/usr/lib/nvidia" >> ~/.bashrc

# Install OpenCV
sudo apt-get install libopencv-dev python-opencv python3-opencv

# If build opencv by source, bellow is the required toolkit
sudo apt-get install git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
# Install Qt5
sudo apt-get install qt5-default
sudo apt-get install libqt5x11extras5-dev

# Install FFmpeg
sudo apt-get install ffmpeg

# Python about
sudo apt-get install python2.7-dev python3.5-dev python-pip python3-pip python-numpy python3-numpy
sudo pip3 install --upgrade pip3
sudo pip2 install --upgrade pip2
sudo pip install pillow sk-video scikit-image six matplotlib protobuf urllib3

# About Caffe
sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler
sudo apt-get install --no-install-recommends libboost-all-dev
sudo apt-get install libatlas-base-dev # Or sudo apt-get install libopenblas-dev

# Install Shadowsocks-qt5
sudo add-apt-repository ppa:hzwhuang/ss-qt5
sudo apt-get update
sudo apt-get install shadowsocks-qt5

# Install openssh-server
sudo apt-get install openssh-server

# Config git
ssh-keygen # Also can use for ssh
git config --global user.name "StickCui"
git config --global user.email "StickCui@users.noreply.github.com"
echo "${GREEN}Don't forget to copy/upload '~/.ssh/id_rsa.pub' to github/server${NC}"

# Install vim
sudo apt-get install vim
# Config vim
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
git clone https://github.com/Valloric/YouCompleteMe.git ~/.vim/bundle/YouCompleteMe
cd ~/.vim/bundle/YouCompleteMe/
python3 ./install.py
cd CURDIR
# Write vimrc
echo ./vimrc > ~/.vimrc
echo "${GREEN}Don't forget to run 'PluginInstall' when open vim to install other plugin${NC}"

# Sublime Text 3
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update
sudo apt-get install sublime-text
echo "${GREEN}Don't forget to fix chinese input${NC}"
echo "  ${GREEN}git clone https://github.com/lyfeyaj/sublime-text-imfix.git${NC}"

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i --force-depends google-chrome-stable_current_amd64.deb
sudo apt-get install -f

echo "${ORANGE}Download TeXlive and install it.${NC}"
# TeXLive ver[2017]
# echo "\nexport MANPATH=${MANPATH}:/usr/local/texlive/2017/texmf-dist/doc/man" >> ~/.bashrc
# echo "\nexport INFOPATH=${INFOPATH}:/usr/local/texlive/2017/texmf-dist/doc/info" >> ~/.bashrc
# echo "\nexport PATH=${PATH}:/usr/local/texlive/2017/bin/x86_64-linux" >> ~/.bashrc

echo "${ORANGE}Download Atom and install it.${NC}"
echo "Plugin for atom list bellow:"
echo "  Sublime-Style-Column-Selection"
echo "  atom-beautify"
echo "  autocomplete-python"
echo "  highlight-selected"
echo "  language-cmake/cpp14/cython/latex"
echo "  latex"
echo "  markdown-pdf"
echo "  markdown-preview-plus"
echo "  pdf-view"
echo "  simplified-chinese-menu"

# For matlab
echo "${ORANGE}After install matlab then run:${NC}"
echo "  ${ORANGE}sudo apt-get install matlab-support${NC}"

# For PyTorch
echo "\nexport LD_PRELOAD=/usr/lib/libtcmalloc_minimal.so.4" >> ~/.bashrc

. ~/.bashrc
