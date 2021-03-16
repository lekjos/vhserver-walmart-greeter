#!/bin/bash
DIR="/home/***REMOVED***/log/console"
inotifywait -m -e modify /home/***REMOVED***/log/console/vhserver-console.log | while read f

do
    echo 'do something';
    cat /home/***REMOVED***/log/console/vhserver-console.log | egrep 'Got handshake from client|Closing socket' > /home/***REMOVED***/log/console/recent.log;
    python3 /home/***REMOVED***/source/vhserver_tools/discord_post.py;
done
