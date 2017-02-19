# logtracker.py - Main code for the logtracker application
# Author - Matt (emdecay (at) protonmail.com)

import os, csv, time, sqlite3, dbinit, glob

logdir_path = "/var/log"
logdirs = os.listdir(logdir_path)
prevhour = int(time.strftime('%H'))-1
if prevhour == -1:
    prevhour = 23
print prevhour
dbconn = sqlite3.connect('logtracker.db')
dbc = dbconn.cursor()

# Stuff for CSV support; remove or modify when getting rid of CSV support
logfile = time.strftime("%Y-%m-%d_%H-%M-%S_") + "results.csv"
file = open(logfile, 'ab')
csvout = csv.writer(file)

# Create record for the scan
dbc.execute("INSERT INTO scan VALUES(\'" + str(time.strftime("%X")) + "\', \'" + str(time.strftime("%x")) + "\', NULL)")
# Get the scanid
curscan = dbc.execute("SELECT MAX(scanid) FROM scan").fetchone()[0]

for dir in logdirs:
    day = "today"
    if prevhour == 23:
        day = "yesterday"
    logging = "No"
    dirpath = logdir_path + "/" + dir + "/"
    for fileobj in glob.glob(dirpath + day + "/" + str(prevhour).zfill(2) + "/*"):
        if os.path.isfile(fileobj):
            logging = "Yes"
    for fileobj in glob.glob(dirpath + day + "/*"):
        if os.path.isfile(fileobj):
            logging = "Yes"
    if logging == "No":
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
