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

LOG_PATH=/home/***REMOVED***/log/console/vhserver-console.log #path to vhserver console log
RECENT_PATH=/home/***REMOVED***/log/console/recent.log #path to where you'd like to store recent.log (grep of vhserver console log)
PROGRAM_PATH=/home/***REMOVED***/source/vhserver_tools/discord_post.py #path to discord_post.py

inotifywait -m -e modify $LOG_PATH | while read f

do
    echo 'log updated';
    cat $LOG_PATH | egrep 'Got handshake from client|Closing socket' > $RECENT_PATH;
    python3 $PROGRAM_PATH;
done
