#!/bin/sh
### BEGIN INIT INFO
# Provides:          filenotifier
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Walmart-greeter shell script
# Description:       Updates recent.log when changes made to vh log
### END INIT INFO

DIR="/home/***REMOVED***/log/console"
inotifywait -m -e modify /home/***REMOVED***/log/console/vhserver-console.log | while read f

do
    echo 'log updated';
    cat /home/***REMOVED***/log/console/vhserver-console.log | egrep 'Got handshake from client|Closing socket' > /home/***REMOVED***/log/console/recent.log;
    python3 /home/***REMOVED***/source/vhserver_tools/discord_post.py;
done
