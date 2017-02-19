# logtracker.py - Main code for the logtracker application
# Author - Matt (emdecay (at) protonmail.com)

import os, csv, time, sqlite3, dbinit, glob

# logdir_path is the path for the individual log directories, assuming a directory is created to hold the logs of each individual server or group of servers
logdir_path = "/var/log"
logdirs = os.listdir(logdir_path)

# For logs that are rotated hourly, determine whether a system is logging based on whether or not it logged during the previous hour
prevhour = int(time.strftime('%H'))-1
if prevhour == -1:
    prevhour = 23

# Connect to the database (previously initialized through dbinit.py)
dbconn = sqlite3.connect('logtracker.db')
dbc = dbconn.cursor()

# Stuff for CSV output of results
logfile = time.strftime("%Y-%m-%d_%H-%M-%S_") + "results.csv"
file = open(logfile, 'ab')
csvout = csv.writer(file)

# Create record for the scan
dbc.execute("INSERT INTO scan VALUES(\'" + str(time.strftime("%X")) + "\', \'" + str(time.strftime("%x")) + "\', NULL)")

# Get the scanid; used when adding records for each individual scan result
curscan = dbc.execute("SELECT MAX(scanid) FROM scan").fetchone()[0]

for dir in logdirs:
    day = "today"
    if prevhour == 23:
        day = "yesterday"
    logging = "No"
    dirpath = logdir_path + "/" + dir + "/"
    for fileobj in glob.glob(dirpath + day + "/" + str(prevhour).zfill(2) + "/*"):
        if os.path.isfile(fileobj):
			# System is logging
            logging = "Yes"
    for fileobj in glob.glob(dirpath + day + "/*"):
        if os.path.isfile(fileobj):
			# System is logging
            logging = "Yes"
    if logging == "No":
		# System is not logging; see if it was logging the last time logtracker was run
        prevresult = dbc.execute("SELECT status FROM scanresult WHERE dir = \'" + dir + "\' AND scanid =\'" + str(curscan-1) + "\'").fetchone()
        if prevresult is not None:
            prevresult = prevresult[0]
            if prevresult == "Yes":
                logging = "No - Newly Missing"
    csvout.writerow([dir, logging])
    # Create a record for the individual scan result
    logline = "INSERT INTO scanresult VALUES(\'" + dir + "\', \'" + logging + "\', " + str(curscan) + ", NULL)"
    dbc.execute(logline)

dbconn.commit()
file.close()
dbconn.close()
