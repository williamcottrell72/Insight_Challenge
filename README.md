# Insight_Challenge
Sessionizes log data from the Edgar website.

To run the file, open the src file 'insightEdgar_v6.py' in python and run.

The program works as follows.  First, we define a 'sessions' dictionary which
records information about open sessions, including which ip addresses currently 
have open sessions and which files they have accessed.  We then scan through 
the request one at time.  In each loop of the scan, we first clean the sessions
record by removing the closed sessions and recording them to the output file
sessionization.txt in the order of when the user first logged in.  Next, we 
update the sesssions file with the new request if it is for a new document.  If
the request is by the same user for the same document in the same session (though
at a different time) we ignore this.  Finally, after all request have been scanned 
over, we record the remaining sessions data in the output file.  The final time for
these remaining elements is assumed to be the time of the last request.
