# log-miner.py

Log content mining tool. This tool is written to find complete log records even if the log record consist of multiple lines. By default log record separator is timestamp and every log record is expected to start with one. You can tune it to match your logs. However date search feature expects 'yyyy-mm-dd HH:MM:SS' order in timestamps.

Example log records:

    [2020-12-31 22:33:44] INFO some general info here
    [2020-12-31 22:33:45] ERROR bad exception occurred
    java.lang.NullPointerException
        at somewhere
    Message Details: some details here
        at some row of code
    Caused by: something here
        at some row of code
        at some row of code
    [2020-12-31 22:33:46] WARNING pay attention to this
    [2020-12-31 22:33:47] INFO everything running fine now

### Use case 1: Get summary of log content

Get summary of log content using default search pattern: `'(WARN|ERROR|FATAL|NullPointerException)'`

    ./log-miner.py -s logfile.log

### Use case 2: Get full log records based on RegEx search

Get all full log records based on given RegEx pattern.

    ./log-miner.py -r '(NullP|This is interesting)' logfile.log

### Use case 3: Start search from given timestamp

Start log search from given timestamp that can be partial.

    ./log-miner.py -d '2021-01-01 11' logfile.log

### Use case 4: Get only new logs written since last run

Get only new logs written after previous run. Ignored if the log file (file inode) has changed.

    ./log-miner.py -l logfile.log

### Use case 5: Mask log values to get better summary

Use mask to hide values or to get better summary. For example IP:Port:

    ./log-miner.py -s -m '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{2,5}' logfile.log

### Use case 6: Exclude logs

Leave out uninteresting logs.

    ./log-miner.py -r Exception -n 'This is not interesting' logfile.log

### Use case 7: Combine options

Combine different options.

    ./log-miner.py -r Exception -n 'Not this Exception' --since_last_run -m 'mask this string' logfile.log

