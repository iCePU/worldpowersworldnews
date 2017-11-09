#!/usr/bin/python3
#this is going to be the data agregator the analysis is going to be a different program i heard thata the praw lib is not thread safe but i think if its in the main program it will be fine
import praw
import json
from time import time
import multiprocessing as mp
clId = "string" #this is client id this will be on your reddit
clSe = "string" #this is the client secret. it'll be on the app page thats under your reddit
subRed = "string" #the subreddit that you want to poll
Pass = "string" #password to your own account
Username = "string" # your username 
refresh = 5 *1000 #the first number is in seconds the second is to convert from micro seconds to seconds 
def request(reddit):
    return reddit.request("GET","/r/"+subRed+"/hot")
def request2pdf(string):
    string = json.dumps(string)
    #Do something with the json lib 
    return string
def writefile(q):
    #check to see if log.txt is a thing if not make it
    while True:
        tmp = q.get()
        log = open("log.txt","a")
        log.write(tmp)
        log.write("\n")
        log.close()
def main(q):
    reddit = praw.Reddit(client_id = clId,
        client_secret              = clSe,
        password                   = Pass,
        user_agent                 = "python3:worldpowersworldnews:v0.0.1 (by /u/iCePU))",
        username                   = Username)
    start_time = time()
    frame = 0
    current_time = start_time
    frame_start = start_time
    while True:
        current_time = time()
        if current_time > frame_start:
            tmp = request(reddit)#make a request, this locks the thread
            tmp = request2pdf(tmp)
            q.put(tmp)# pipe the data to another process
            frame +=1
            if frame % 60 ==0:
                frame = 0
                frame_start = time()
            frame_start += refresh # its 5 seconds
            #add frame
if __name__ == '__main__':
    #start the file write process
    q = mp.Queue()
    filewrite = mp.Process(target=writefile, args=(q,))
    filewrite.start()
    main(q)
