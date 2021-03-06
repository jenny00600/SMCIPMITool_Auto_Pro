
import subprocess
import time
import re
import sys

#======================================================
# var
#======================================================
#groups = []  # [[___,____,_____,____87___,____90_,...,__],
             #  [___,____,_____,____87___,____90_,...,__],
             #  [___,____,_____,____87___,____90_,...,__],
             #  ...
             #  [___,____,_____,____20___,____10_,...,__]]   len(groups) = 105

#logs = []  #  [[time1,pout1,pin1],
           #   [time2,pout2,pin2],
           #   ...
           #   [timeN,poutN,pinN]]                          len(logs) = 105
name = []

#=====================================================================
# Function :    find_in_out
# Input :       input
# Output :      pout, pin
# Description : find the data we want
#=====================================================================
def find_in_out(input):
    pout = None
    pin = None

    if re.search( r'\Output Power\s', input, re.M|re.I):
        output_power = input
        pout = output_power.strip().split(' ')[-2]

    if re.search( r'\Input Power\s', input, re.M|re.I):
        Input_power = input
        pin = Input_power.strip().split(' ')[-2]
    return pout, pin

#=====================================================================
# Function :    groups_to_logs
# Input :       file name
# Output :      result(time, pout, pin) in file
# Description : find the data we want
#=====================================================================
#Compared P_out & P_in
def groups_to_logs(name):
    groups = []
    logs = []

    # file to groups
    with open(name , 'r') as searchfile:
        # read file to lines
        lines = searchfile.read().splitlines()

        # init groups
        group = []
        for line in lines:
            group.append(line)
            if line == '' :
                groups.append(group)
                group = []


    # for each group, find timestamp, p_out and p_in
    for group in groups:
        curr_pout = []
        curr_pin = []
        for word in group:
            pout, pin = find_in_out(word)# type(input) = string
            if pout != None: curr_pout = pout
            if pin != None:  curr_pin = pin

        l_time = group[1]
        l_pin = int(curr_pin)
        l_pout = int(curr_pout)
        logs.append( [l_time, l_pout, l_pin] )

    # ave for .csv
    with open( name +'.csv','w') as fout :
        for log in logs:
            fout.write( str(log[0]) + "," + str(log[1]) + "," + str(log[2]) + "\n")  # Thu Mar 29 11:29:46 2018

    # jenny save
    with open(name + '_result','w') as fout :
        for log in logs:
            # inputs
            pout = log[1]
            pin = log[2]
            curr_time = log[0] # 1522348227.33
            localtime =  time.asctime( time.localtime(float(curr_time)) )# Thu Mar 29 11:29:46 2018
            result = None

            # get result
            if int(pout) > int(pin) : result = " Pout > Pin : Error!"
            else : result = " Pout < Pin : Pass"
            if int(pout) > int(pin) : result = " Pout > Pin : Error!"


            # print to file
            fout.write(localtime + "\n")  # Thu Mar 29 11:29:46 2018
            fout.write(str(curr_time) + "\n") # 1522348227.33
            fout.write("--------------------------------" + "\n")
            fout.write(" Pout = " + str(pout) + "\n" )
            fout.write(" Pin = " + str(pin) + "\n" )
            fout.write(" Result = " + result + "\n\n")

#======================================================
# main
#======================================================
if __name__=='__main__':
    name = sys.argv[1] #('Which file you want to compared : ')
    groups_to_logs(name)

    # get time
    localtime = time.asctime( time.localtime(time.time()) )
    print "Finish Time : " + localtime
