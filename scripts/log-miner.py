#!/usr/bin/python3
# Log content mining tool 
#
# Written by Marko Mäkiö (marko , makio (a) gmail , com) in 2020
# License: GNU GENERAL PUBLIC LICENSE Version 3
#
# Each log record starts with timestamp and a log record can consist of many lines.
# To be used with the following log format:
# [2020-12-29 13:45:56] - some log content
# [2020-12-29 13:45:57] - some bad exception happened
# Message Details: jaddajadda
#    at some line of code
# Caused by: diibadaa
#    at some line of code
# [2020-12-29 13:45:58] - some log content
#

import sys,argparse,re,os
from pathlib import Path

# Default global values
summarized={}
summary=False
log_record=''
regex_search = '(WARN|ERROR|FATAL|NullPointerException)'
neg_regex_search = '' 
column = 2
summary_extra_lines = re.compile(r'(Message Details: |Caused by: |^[a-zA-Z0-9\/_\$\.])')

def main(argv):
    global summarized
    global summary
    global log_record
    global regex_search 
    global neg_regex_search 
    global column 
    found_date = False
    search_date = None
    last_run_file = str(Path.home()) + '/log-miner.seek'
    log_record_start = re.compile(r'^\[20[2-3][0-9]-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]')
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='Log content mining tool')

    # Add arguments
    parser.add_argument('LogFile',
                        metavar='log_file',
                        type=str,
                        help='Log file')
    parser.add_argument('-s',
                        '--summary',
                        action='store_true',
                        help='Print unique log rows as counted summary')
    parser.add_argument('-l',
                        '--since_last_run',
                        action='store_true',
                        help='Read only new lines written to the log after previous run')
    parser.add_argument('-d',
                        '--date',
                        metavar='\'YYYY-mm-dd HH:MM:SS\'',
                        type=str,
                        help='Parse Apache httpd log format')
    parser.add_argument('-c',
                        '--column',
                        metavar='number',
                        type=int,
                        help='Start summary output from this column number')
    parser.add_argument('-r',
                        '--regex',
                        metavar='\'regex_pattern\'',
                        type=str,
                        help='RegEx search pattern. By default: ' + regex_search)
    parser.add_argument('-n',
                        '--negregex',
                        metavar='\'neg_regex_pattern\'',
                        type=str,
                        help='Negative RegEx search pattern. By default no value.')
    
    # Execute parse_args() method
    args = parser.parse_args()
    
    # Get argument values
    log_file = args.LogFile
    summary = args.summary
    neg_regex_search = args.negregex
    since_last_run = args.since_last_run
    if args.date is not None:
        search_date = re.sub('\D', '', args.date)
    if args.regex is not None:
        regex_search = args.regex
    if args.column is not None:
        column = args.column

    # Read inode and seek position values
    if since_last_run:
        try:
            s = open(last_run_file)
            seek_info = (s.readline().split(' '))
            seek_inode = int(seek_info[0])
            seek_position = int(seek_info[1])
            s.close()

        except IOError:
            print ('Failed to open file: ' + last_run_file)
            sys.exit(1)

    f = open(log_file)
    
    # Get current file inode value
    log_file_inode = int(os.stat(log_file).st_ino)
    
    # Seek position if the same file (inode)
    if since_last_run and seek_inode == log_file_inode and seek_position > 0:
        f.seek(seek_position)

    # Read log file line by line
    for line in f:

        # Search for given timestamp (if any) and skip log lines until newer logs found
        if search_date is not None and found_date == False:
            if re.match(log_record_start, line):
                split_line = line.split(' ')
                log_date = split_line[0] + split_line[1]
                # Strip all non-numeric from timestamp
                log_date = re.sub('\D', '', log_date)
                # Given timestamp can be partitial as comparing as strings
                if log_date > search_date:
                    found_date = True
                else:
                    continue
            else:
                continue

        # When new log record found, handle first previously stored log record
        if re.match(log_record_start, line):
            handle_log_record()
            # Clear log_record after handling
            log_record = ''

        # Add current log line to log_record
        log_record = log_record + line

    # Write log_file inode and seek position
    s = open(last_run_file, "w")
    s.write (str(log_file_inode) + ' ' + str(f.tell()))
    # Close files
    s.close()
    f.close()

    # Handle final log_record
    if len(log_record) > 0:
        handle_log_record()

    # Print sorted by count summary
    if summary:
        sorted_items = dict(sorted(summarized.items(), key = lambda item: (item[1], item[0])))
        for log, count in sorted_items.items():
            print ('{:8} {}'.format(count, log))

def handle_log_record():
    global summarized
    global summary
    global log_record
    global regex_search 
    global neg_regex_search 
    global column 
    global summary_extra_lines 
    search_match = False

    if neg_regex_search is not None:
        if re.search(regex_search, log_record) and not re.search(neg_regex_search, log_record):
            search_match = True
    elif re.search(regex_search, log_record):
        search_match = True

    if search_match == True and summary == False:
        print (log_record)
    elif search_match == True and summary == True:
        # Remove timestamp or selected number of columns
        split_log = log_record.split(' ')
        log_record = ' '.join(split_log[column:])
        # Split again by newlines to get extra lines
        split_log = log_record.split('\n')
        
        for i in range(len(split_log)):
            if i == 0:
                log_record = split_log[0]
            elif re.search(summary_extra_lines, split_log[i]):
                log_record = log_record + split_log[i]

        if log_record not in summarized:
            summarized[log_record] = 1
        else:
            summarized[log_record] = summarized[log_record] + 1

if __name__ == '__main__':
    main(sys.argv[1:])
