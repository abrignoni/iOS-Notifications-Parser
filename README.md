# iOS-Notifications-Parser
Python script that generates a HTML triage report of iOS notifications content.

![alt text](usage.PNG "Usage example")

Usage:   
python iOSNotificationsParser.py /path/to/data/directory  

See blog post here for more details:  
https://github.com/abrignoni/iOS-Notifications-Parser

Requisites:  
1) Python 3 . 
2) The ccl_bplist module is required for the script to work. It can be found here: https://github.com/cclgroupltd/ccl-bplist (But a version has been inluded in this repo) . 
3) The included script.txt enables fields in the HTML report to be toggled between show and hide.  
4) The included NotificationParams.txt defines which values to be toggled between show and hide. Add more as needed one value per line.   

After process is completed a folder will be created in the same directory where the script is located. The folder will be named TriageReports_script_run_timestamp.

Caveat:  
Script depends on the UserNotification directory (where notifications on iOS are kept) to be at least one level down (or more) from the data directory provided to the script. 
