---
description: PenTesting Focused  Tips on how to use Nmap
---

# Nmap

📃Greate Nmap cheatsheet

{% embed url="https://www.stationx.net/nmap-cheat-sheet" %}

using Nmap to BruteForce ssh login:

```
sudo nmap -p 22 --script ssh-brute --script-args userdb=<user.list>,passdb=<pass.lst> <IP>
```

> for exmaple pass.lst:
>
> ```
> /usr/share/nmap/nselib/data/passwords.lst
> ```

