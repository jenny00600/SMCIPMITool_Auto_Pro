import subprocess
import time
import re
import sys

# var
name = 0
_ipmi_tool = '/home/jenny/SMCIPMITool/SMCIPMITool'
_ipmi_user = 'ADMIN'
_ipmi_pswd = 'ADMIN'
#=====================================================================
# funcions
#=====================================================================
#=====================================================================
# Function :    get_ipmi_data
# Input :       ipmi_ip, ipmi_cmd, sample_rate, time_cycle
# Output :      logs
# Description : Get data of ipmi and time, then save in logs
#=====================================================================
def get_ipmi_data(ipmi_ip, ipmi_cmd, sample_rate, time_cycle):
    # var
    logs = []  # [str, str, str, str,....]
    count = 0

    while (count < int(time_cycle)):  # 61 < 60)
        # get data
        process = subprocess.Popen(    \
            [_ipmi_tool, ipmi_ip, _ipmi_user, _ipmi_pswd \
             ,ipmi_cmd],stdout=subprocess.PIPE)
        out, err = process.communicate()

        # get time
        curr_time = time.time()  # 1234567891.33
        localtime = time.asctime( time.localtime(float(curr_time)) )  # May 09 ....

        # save to logs
        logs.append(str(localtime)+ "\n")
        logs.append(str(curr_time)+ "\n")
        logs.append(out)

        # count ++
        count = count + 1

        # loop contorl
        time.sleep(int(sample_rate)) # sleep 5 sec

    return logs

#=====================================================================
# Function :    save_logs
# Input :       logs, filename
# Output :      log in file
# Description : Save the log data
#=====================================================================
def save_logs(logs, filename):

    with open(filename,'w') as fout:
        for log in logs:
            fout.write(str(log))

#=====================================================================
# main
#=====================================================================
if __name__=='__main__':

    # get input ip and output filename
    logs = get_ipmi_data('172.31.36.124', 'pminfo', 5, 3)

    # save data
    file_name = sys.argv[1]
    save_logs( logs, file_name)
