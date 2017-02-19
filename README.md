# logtracker

Log Tracker is designed to quickly determine whether a log file has recently been created or not.  This tool is useful for servers used as central syslog repositories, allowing an analyst to quickly determine which hosts are and are not sending logs.  It also reports which hosts are newly not logging (as opposed to systems that haven't been logging for a while).

The program stores results in a local database, allowing results for many scans to be stored and queried.  This allows historical analysis and enables an analyst to determine when a host first stopped sending logs.
