#!/bin/bash
DIR="/home/***REMOVED***/log/console"
while inotifywait -m -e modify ~/log/console/vhserver-console.log; do
    echo 'do something';
    cat vhserver-console.log | egrep 'Got handshake from client|Closing socket' > ./recent.log;
    python3 /home/***REMOVED***/source/vhservertools/discord_post.py;
done
