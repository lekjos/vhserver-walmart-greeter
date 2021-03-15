#!/bin/bash
DIR="/home/***REMOVED***/log/console"
inotifywait -m -e modify ~/log/console/vhserver-console.log | while read f

do
    echo 'do something';
    cat vhserver-console.log | egrep 'Got handshake from client|Closing socket' > ./recent.log;
    python3 /home/***REMOVED***/source/vhservertools/discord_post.py;
done
