# dbinit.py - Initialize the database connectivity for logtracker
# Author - Matt (emdecay (at) protonmail.com)

import os, sqlite3

db = "logtracker.db"

# If database doesn't yet exist, initialize it with the table structure
if not os.path.isfile(db):
    print "No database found; initializing \'" + db + "\'..."
    # Initialize database
    dbconn = sqlite3.connect(db)
    dbc = dbconn.cursor()
    dbc.execute("CREATE TABLE scan (scantime TEXT, scandate TEXT, scanid INTEGER PRIMARY KEY AUTOINCREMENT)")
    dbc.execute("CREATE TABLE scanresult (dir TEXT, status TEXT, scanid INTEGER, resultid INTEGER PRIMARY KEY AUTOINCREMENT, FOREIGN KEY(scanid) REFERENCES scan(scanid))")
    dbconn.commit()
    dbconn.close()
