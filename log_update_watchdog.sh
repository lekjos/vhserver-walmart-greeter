#! /home/***REMOVED***/log/console
DIR="/home/***REMOVED***/log/console"
while inotifywait -m -e modify ~/log/console/vhserver-console.log; do
    cat vhserver-console.log | egrep 'Got handshake from client|Closing socket' > ./recent.log
    python3 /home/***REMOVED***/source/discord_post.py;
done