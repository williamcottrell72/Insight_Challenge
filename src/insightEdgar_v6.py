# -*- coding: utf-8 -*-
"""
Created on Sat May 26 17:12:52 2018

@author: willi
"""

from datetime import datetime, timedelta
import csv



f=open(r"..\input\log.csv") 
g=open(r"..\input\inactivity_period.txt")
out=open('..\output\sessionization.txt','w+')
csv_f=csv.reader(f)
t_gap=int(g.readlines(1)[0])


#In the code below we will iterate over the rows in the log.csv file.
#The functions yr(), month(), day(), hr(), minute() and sec() parse
#the rows of the log.csv file and return variables with the names 
#suggested.  These are fed into the function 'date_function' which
#returns a datetime variable and its associated calendar functions. 
#Finally, doc_id is the unique doc identifier.  The doc identifier is 
#just a string consisting of the 'cik', 'accession' and 'extensions' 
#data. If the same user access a file with the same identifier at two 
#different times in the same session this will not be considered as a 
#new document request and the current browsing session data will not 
#be updated.

def yr(elem):
    return int(elem[1][0:4])
def month(elem):
    return int(elem[1][5:7])
def day(elem):
    return int(elem[1][8:10])
def hr(elem):
    return int(elem[2][0:2])
def minute(elem):
    return int(elem[2][3:5])
def sec(elem):
    return int(elem[2][6:8])
def date_function(elem):
    return  datetime(yr(elem),month(elem),day(elem),hr(elem),minute(elem),sec(elem))
def doc_id(elem):
    return elem[4]+elem[5]+elem[6]

#Initialize the dictionary 'sessions' whose keys are IP addresses, which
#represent users, and whose values are a list [#docs checked,last request,
#first request, list of docs previously checked].  We need to temporarily 
#store the list of docs previously checked (based on doc_id) in order to 
#avoid over-counting.

sessions = {} 

#The variable ct is defined as a device to skip over the first line of the data
#file.
ct=True
counter=0

for elem in csv_f:  
    counter+=1
    if counter%1000==0:
        out.flush()
#    print(counter)
    #The variable 'df' stores the date+time of a request.  We must run it 
    #through a 'try' in order to avoid the errors on the first line. The
    #'elapsed' variable is the time between the current request and the 
    #last request in the current active session for a given user.
    try:
        df = date_function(elem)
        elapsed0=df-sessions[elem[0]][1]
        elapsed=24*3600*elapsed0.days+elapsed0.seconds   
    except(ValueError,KeyError):
        pass
    #First we go through the open sessions and see which ones should be closed.
    #We re-sort the open-sessions file in the order of when the data was first
    #accessed so that they are closed and written to the 'sessionation.txt' file
    #in the appropriate order.
    sl=list(sessions.items())
    sl.sort(key=lambda x: x[1][1])    
    for stuff in sl:
        delta=df-stuff[1][1]
        time_since_use=24*3600*delta.days+delta.seconds
        if time_since_use > t_gap:
            time_session=stuff[1][1]-stuff[1][2]
            seconds_on=24*3600*time_session.days+time_session.seconds
            out.write(stuff[0]+','+str(stuff[1][2])+','+str(stuff[1][1])+',' \
                     +str(seconds_on)+','+str(stuff[1][0])+"\n")
            del sessions[stuff[0]]
    #We set up 'ct' as a filter just to skip the first row in the csv file
    if ct:
        ct=False
    #Check to see if the new element is in an open session.  If so, we want to 
    #add 1 to the doc counts and update the time of access. However, first we
    #need to check to see if the doc_id has already been accessed in the current
    #session.    
    elif elem[0] in sessions and (elapsed<t_gap):
        try:
            #The doc_id tells us whether the the same document is being requested
            #a second time by the same user in a given session.  If so, I am
            #interpreting the instructions to say that we should do nothing.  
            #Visuallly scanning the data, this does not seem to happen
            #that often, i.e., basically every line in the csv file corresponds
            #to a different document request.  However, there may be some rare
            #exceptions where multiple lines represent the same user requesting
            #the same document in a short time interval and this must be
            #accounted for.
            if doc_id(elem) in sessions[elem[0]][3]:
                pass
            #For a new doc request by the same user we update the session data.
            else:
                sessions[elem[0]][0]+=1
                sessions[elem[0]][1]=df
                tmp=sessions[elem[0]][3]
                tmp.append(doc_id(elem))
                sessions[elem[0]]=[sessions[elem[0]][0],sessions[elem[0]][1],\
                              sessions[elem[0]][2],tmp]
        except(IndexError,TypeError,AttributeError):
            pass
    #If elem is not in sessions at all then we must create a new entry in the
    #sessions dictionary.  The order is [doc count, current time, opening time,
    #list of doc's requested.]
    else:                   
        sessions[elem[0]]=[1,df,df,doc_id(elem)]
         
# Finally, we record anything that is left over at the end. Note
#that the value of df is already set as the datetime element of 
#the last request that was made.  If any open sessions remain at
#the end, we just assign session times by assuming that they close
#with the last element of the file.  Note that by construction these 
#times will be smaller than t_gap.
        
sl=list(sessions.items())
sl.sort(key=lambda x: x[1][1])    
for stuff in sl:
    delta=df-stuff[1][2]
    time_session=24*3600*delta.days+delta.seconds
    out.write(stuff[0]+','+str(stuff[1][2])+','+str(stuff[1][1])+',' \
       +str(time_session)+','+str(stuff[1][0])+"\n")
    del sessions[stuff[0]]        
        
f.close()
out.close()

