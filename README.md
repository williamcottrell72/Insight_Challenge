# Insight_Challenge
Sessionizes log data from the Edgar website.

The program works as follows.  First, we define a 'sessions' dictionary which
records information about open sessions, including which ip addresses currently 
have open sessions and which files they have accessed.  We then scan through 
the request one at time.  In each loop of the scan, we first clean the sessions
record by removing the closed sessions and recording them to the output file
sessionization.txt in the order of when the user first logged in.  Next, we 
update the sesssions file with the new request.  Finally, after all request have 
been scanned over, we record the remaining sessions data in the output file.  
