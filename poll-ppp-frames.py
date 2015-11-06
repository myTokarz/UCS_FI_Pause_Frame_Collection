#!/usr/bin/env python
#-------------------------------------------#
# Custom report to grab txppp and rxppp off
# of the Fabric Interconnects
#
# 10/23/15 @myTokarz
#-------------------------------------------#

# ------------- CONFIG AREA ----------------# 
USER = 'admin'
PASSWORD = 'secret'
# ---------- END OF CONFIG AREA ------------#

devices = ['10.50.0.20',
          ]
 

# Commands to execut
# List of lists, each list containing
#   1. Command to execute
#   2. Amount of time to wait for the command to come back
#   3. Boolean if the command output should be kept or discarded 
commands = [
    ['connect nxos a', '10', '0'],
    ['show interface priority-flow-control', '3', '1'],
    ['exit', '2', '0'],
    ['connect nxos b', '10', '0'],
    ['show interface priority-flow-control', '3', '1']
    ]

# Disable |MORE paging on output
def disable_paging(remote_conn):
    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)
    return output


for device in devices:

    print "Querying device: "+device

    try: 
        # Create an SSH session to the fabric interconnect 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device, username=USER, password=PASSWORD)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        chan = ssh.invoke_shell()
        disable_paging(chan)
         
        # Execute command to gather expanded server inventory  
    
        for command in commands:
    	    print "executing command: "+command[0]+"\n"
            chan.send(command[0]+'\n')
            time.sleep(float(command[1]))
            output = chan.recv(99999)
            if (command[2] != '0'):
                print output
    
    finally:
        if ssh:
            # Close all connections 
            ssh.close()
    
