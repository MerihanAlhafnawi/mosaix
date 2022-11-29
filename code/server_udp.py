import socket
import time
import subprocess
import _thread
import json
from csv import writer
import os
import math
from datetime import datetime
filename = ''
started1 = False
started2 = False
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port). 
# Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
# For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
# Thanks to @stevenreddie


server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.bind(("", 37021))
#server.setblocking(0)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
#server.settimeout(0.2)
started1 = False
started2 = False
neighbourhood = []
send_neighbourhood = ''
op_count= [0]*21 #list containing opinions spaced by 5%
count = 0
filename = os.path.join('robot_logs' + '.csv')
while (os.path.isfile(filename) == True):
   filename = os.path.join('robot_logs' +  str(count) + '.csv')
   count = count + 1
open(filename, 'a').close()
fields =["robot_id", "opinion", "aggregate", "hour", "minute", "second", "comp_hour", "comp_minute", "comp_second"]
with open(filename, 'a+', newline='') as write_obj:
    # Create a writer object from csv modules
    csv_writer = writer(write_obj)
    # Add contents of list as last row in the csv file
    csv_writer.writerow(fields)
print (filename)
def recv_thread(server):
    global neighbourhood
    global send_neighbourhood
    global filename
    while True:
        send_neighbourhood = ''
        found_neighbour = False
        data, addr = server.recvfrom(1024)
        print("message received!", data) 
        decoded = bytes.decode(data, 'utf-8')
        #data = 'rpi77a2oMORE_WATER_NOW rpi89a6oBUILD_PARKS rpi77a2oLESS_WATER_NOW'
        #neighbours = data.split()
        print (neighbourhood)
        rid = ""
        found_neighbour = False
        aggregate = ""
        curr_pos = 0
        opinion = ""
        for i in range (3, len(decoded)):
            if (decoded[i] != 'a'):
                rid += decoded[i]
            else:
                break
            curr_pos = i
        for i in range (curr_pos+2, len(decoded)):
            if (decoded[i] != 'o'):
                aggregate += decoded[i]
            else:
                break
            curr_pos = i
        for i in range (curr_pos+2, len(decoded)):
            if (decoded[i] != ' '):
                opinion += decoded[i]
            else:
                break
            curr_pos = i
        #opinion = opinion.replace("_", " ")
        for l in range (len(neighbourhood)):  

            if (neighbourhood[l][0] == rid):
                if (neighbourhood[l][1] != aggregate or neighbourhood[l][2] != opinion):
                    dateTimeObj = datetime.now()
                    h = str(dateTimeObj.hour)
                    m = str(dateTimeObj.minute)
                    s = str(dateTimeObj.second)
                    print ("rid: ", rid, ", opinion: ", opinion, ", aggregate: ", aggregate, "time: ", h, ":", m, ":",s)
                    fields =[rid, aggregate, opinion, h, m,s]
                    with open(filename, 'a+', newline='') as write_obj:
                       # Create a writer object from csv modules
                       csv_writer = writer(write_obj)
                       # Add contents of list as last row in the csv file
                       csv_writer.writerow(fields)
    
                neighbourhood[l][1] = aggregate
                neighbourhood[l][2] = opinion
                found_neighbour = True
                break
        if (found_neighbour == False):
            neighbourhood.append([rid, aggregate, opinion]) 
            dateTimeObj = datetime.now()
            h = str(dateTimeObj.hour)
            m = str(dateTimeObj.minute)
            s = str(dateTimeObj.second)
            print ("rid: ", rid, ", opinion: ", opinion, ", aggregate: ", aggregate, "time: ", h, ":", m, ":",s)
            fields =[rid, aggregate, opinion, h, m,s]
            with open(filename, 'a+', newline='') as write_obj:
               # Create a writer object from csv modules
               csv_writer = writer(write_obj)
               # Add contents of list as last row in the csv file
               csv_writer.writerow(fields)
        print ("rid: ", rid, ", aggregate: ", aggregate, ", opinion: ", opinion)
        print (neighbourhood)
        
        for neighbour in neighbourhood:
            send_neighbourhood += 'rpi' + neighbour[0] + 'a' + neighbour[1] + 'o' + neighbour[2] + '-'
        if (send_neighbourhood[len(send_neighbourhood)-1] == '-'):
             send_neighbourhood = send_neighbourhood[:-1]
        print ("string: ", send_neighbourhood)
        
        
        
        send_text = str.encode(send_neighbourhood, 'utf-8')
        #server.sendto(send_text, ('<broadcast>', 37021))
#example: b'rid13uid8cond35h1m9s7'
#example: b'rid1uid8cond35h1m9s7'
#rid: robot ID that goes from 1-100
#uid: user ID, can vary depending on application, but it is a number
#cond: condition (or opinion) user has entered
#h,m,s: time in hour, minute and second the condition was entered


print ("Welcome robot witch/wizard...\n")

print ("Here is the order of how to communicate with robots\n")
print ("First, you need to shake hands with the robots, then you need to update the code you want them to run")
print ("then you need to tell them to start running, you can then tell them to stop running and finally, to shut down\n")
print ("How to do this you ask?? Well here is the list:\n")
print ("For shaking hands, type \"handshake\"")
print ("For code update, type \"update\"")
print ("For updating startup code, type \"startup\"")
print ("For running the code, type \"run\"")
print ("For stopping the code, type \"stop\"")
print ("For deleting csv log files on robots, type \"delete\"")
print ("For rebooting, type \"reboot\"")
print ("For shutting down, type \"shutdown\"")

#start a different thread that listens to the robots
_thread.start_new_thread(recv_thread,(server,))
 #need to add: update source code (send_start_up) so we also need to add
 #reboot
 #add run1 and run2 to save on different files
def send_message(message):
    for i in range(10):
        server.sendto(message, ('<broadcast>', 37020))

while True:

    command = input()
    if (command == 'handshake'):
        count = 0
        
        send_message(b"handshake")
        print("Handshake command sent!")

    elif (command == 'update'):   
        send_message(b"update")
        print("Update command sent!")

    elif (command == 'update_directory'):   
        send_message(b"update_directory")
        print("Update command sent!")

    elif (command == 'motors'):   
        send_message(b"motors")
        print("Motors sent")

    elif (command == 'central'):   
        send_message(b"central")
        print("Central sent")

    elif (command == 'adhoc'):   
        send_message(b"adhoc")
        print("Adhoc sent")

    elif (command == 'run' or command == 'run1' or command == 'run2' or command == 'run3' or command == 'run4'):
        send_message(command.encode())
        print("Run command sent!")
        if (started1 == False):
            started1 = True
            count = 1
            

    elif (command == 'stop'):    
        send_message(b"stop")
        started2 = False
        started1 = False
        neighbourhood = []
        print("Stop command sent!")

    elif (command == 'shutdown'):    
        send_message(b"shutdown")
        #server.close()
        print("Shutdown command sent!")
        print ("Mischief managed! Goodbye")
        quit()

    elif (command == 'startup'):
        send_message(b"startup")
        print("Startup command sent!")

    elif (command == 'reboot'):    
        send_message(b"reboot")
        #server.close()
        print("Reboot command sent!")
        print ("Next command should be handshake")

    elif (command == 'delete'):
        send_message(b"delete")
        print("Delete command sent!")

    else:
        print ("This is not a valid command, here is the list again:\n")
        print ("For shaking hands, type \"handshake\"")
        print ("For code update, type \"update\"")
        print ("For updating startup code, type \"startup\"")
        print ("For running the code, type \"run\"")
        print ("For stopping the code, type \"stop\"")
        print ("For deleting csv log files on robots, type \"delete\"")
        print ("For rebooting, type \"reboot\"")
        print ("For shutting down, type \"shutdown\"")

       
    command = ''




    
