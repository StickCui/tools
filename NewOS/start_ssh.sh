#!/usr/bin/bash
set -e

choice=""

if [ ! -n "$1" ]; then
    choice="look"
fi

case ${choice} in 
    look)
        ps -e | grep ssh;;
    start)
        /etc/init.d/ssh start;;
    stop)
        /etc/init.d/ssh stop;;
    restart)
        /etc/init.d/ssh restart;;
esac
