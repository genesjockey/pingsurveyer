'''
Ping Surveyer
Version 1

Author: Nicholas Goldsmith
Date Started: 2023-02-13
Last Updated: 2023-02-14
'''

# User Defined Variables
'''
You may want to change these depending on how large of
data files you want and how long you want it to run

num_per_set: Number of pings to run per set (data file)
num_sets: Number of sets to run
sourcelist: Filename of the list with the sites

Comments: I set the number per set to 21176 as that
is about 4 hours on my machine.
'''
num_per_set = 21176
num_sets = 17
sourcelist = './sites.csv'

# Libraries
import subprocess
import re
import csv
import datetime
import random

# Ping Function
def pinger(hostname):
    '''
    input: hostname/ip
    return: hostname/ip, system time when ping initiated (as well as both day and hour individually), ping time
/timed out    '''
    # Get the time before the ping is run
    system_time_start = datetime.datetime.now() 
    # Run the ping command and capture the output
    ping = subprocess.Popen(["ping",'-n','1',hostname],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    res = "Request timed out"
    for line in iter(ping.stdout.readline,b""):
        line = line.decode("UTF-8")
        if "time=" in line:
            location1 = line.find("time=")
            location2 = line.find("ms")
            res = line[location1+5:location2]
            break
    res = [hostname]+[system_time_start]+[system_time_start.strftime('%d')]+[system_time_start.strftime('%H')]+[res]
    return res

# Progress Tracker
def progressBar(num_to_run, prefix = '', suffix = '', decimals = 1, printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        num_to_run  - Required  : number of times pinger will be run (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / num_to_run))
        print(f'\r{percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i in range(0, num_to_run):
        yield i
        printProgressBar(i+1)
    # Print New Line on Complete
    print()

# Opening Sites to Check
with open(sourcelist) as f:
    rows = csv.reader(f)
    sites = [r[0] for r in rows]

# Collecting and Saving Data
for i in range(0,num_sets):
    system_time_start = datetime.datetime.now()
    print("Set", i+1, "of", num_sets, "initiated at:", system_time_start)
    result = [pinger(random.choice(sites)) for iterations in progressBar(num_per_set)]
    system_time_end = datetime.datetime.now()
    print("Set", i+1, "of", num_sets, "ended at:", system_time_end)
    runtime = system_time_end - system_time_start
    print("It took,", runtime, "which amounts to", runtime/num_per_set, "per site pinged for set", i+1, "of", num_sets,)
    filename = datetime.datetime.now().strftime('pinger-data-%d-%m-%Y-%H-%M-%S.csv')
    with open(filename, 'w') as f:
        w = csv.writer(f)
        w.writerow(['Domain', 'StartTime', 'StartDay', 'StartHour', 'PingOutput'])
        for row in result:
            w.writerow(row)