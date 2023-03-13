#!/bin/python3
if __name__ == '__main__':
    import os
    import telnetlib
    import datetime
    import time
    import colorama
    from colorama import Fore
    import socket
    import sys
    os.system("clear")
    def pos( x, y ): #{
        return '\x1b[' + str(y) + ";" + str(x) + 'H';
        #}
    def reset_hpswitchport(host, switchport): #{
        try:
            print("Telnetting to: ", host)
            tn = telnetlib.Telnet()
            print ("connecting to host")
            tn.open(host)
            print ("sending character")
            tn.write(b"a\n")
            print ("config t")
            tn.write(b"Config T\n")
            print ("interface reset")
            tn.write(b"interface " + switchport.encode('ascii')+ b"\n")
            print ("enable")
            tn.write(b"disable\n")
            print ("disable")
            tn.write(b"enable\n")
            print ("exit interface mode")
            tn.write(b"exit\n")
            print ("exit config t mode")
            tn.write(b"exit\n")
            print ("close session")
            tn.close
        except tn.EOFError as e:
            print (e)
        return True
        #}
    runtimes = 0
    i = 1
    a = 1
    while i <= 1:
    #    os.system("clear")
        f = 10
        ftime = f
        runtimes = runtimes + 1
        while ftime > 1:
            print (pos(1,47) + Fore.YELLOW + "Sleeping for ", ftime, " Seconds", Fore.LIGHTBLUE_EX, "Runtime: ", runtimes, "                    ")
            ftime = ftime - 1
            time.sleep(1)
        print (pos(1,47) + "Starting Network Scan Please wait for it to complete         ")
        print (pos(1,1) + "HP POE Switch Manager           ")
        with open("/etc/ip_list.csv") as iplistfile:
            iplist = iplistfile.read()
            iplist = iplist.splitlines()
            iplistfile.close()
        print ("Hello2")
        for ipline in iplist:
            ipline = ipline.split(",")
            host = ipline[3]
            switchport = ipline[4]
            camera = ipline[1]
            ipaddr = ipline[0]
            print (pos(1,2) + Fore.GREEN, "Host",  "IP Address", "Camera Device         ")
            print (pos(1,3) + Fore.GREEN, host, Fore.RED, ipaddr, camera, "      ")
            response = os.popen(f"ping -c 3 {ipaddr}").read()
            print(f" " + ipaddr," ",host, " ",switchport, " ")
            if("Request timed out." or "unreachable") in response:
                print (pos( 1, 4) + Fore.YELLOW, "Host: ", ipaddr, Fore.RED ,"is down         ")
                a = (a + 1)
                today = datetime.date.today()
                now = time.localtime()
                nowstr = time.strftime("%H:%M:%S", now)
                print(f"{today},{ipaddr},{host},{switchport}")
                logfile = open("/var/log/ipcamresets.log", "a")
                logfile.write(f"{today} {nowstr},{ipaddr},{host},{switchport}\n")
                logfile.close()
                print (pos( 1, a) + camera, ipaddr, " IS Was Down at", nowstr, "           ")
                reset_hpswitchport(ipaddr,switchport)
            else:
                print (pos( 1, 4), Fore.YELLOW, "Host: ", ipaddr, Fore.GREEN," is okay        ")
                print (pos( 51, 3), Fore.YELLOW, "Checking Port ", Fore.RED, " 80             ")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(20)
                result = sock.connect_ex((ipaddr,80))
                if result == 0:
                    print (pos(52,4) + Fore.YELLOW, "Port is", Fore.GREEN + " open           ")
                    sock.close()
                    time.sleep(1)
                else:
                    print (pos(52,4) + Fore.RED, "Port is", Fore.GREEN + " DOWN              ")
                    today = datetime.date.today()
                    now = time.localtime()
                    nowstr = time.strftime("%H:%M:%S", now)
                    a = (a + 1)
                    print (pos( 1, a) + camera, ipaddr, " IS Was Down at ", nowstr, "        ")
                    sock.close()
                    reset_hpswitchport(ipaddr,switchport)
                    time.sleep(1)
