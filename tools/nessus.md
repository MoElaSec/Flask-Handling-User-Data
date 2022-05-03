---
description: Vul. Scanner
---

# 🔍Nessus

1- Starting Nessus:

```
sudo systemctl start nessusd && systemctl --no-pager status nessusd
```

`--no-pager:`don't pip the output to a pager&#x20;

> if you don't pipe your output through a pager ( less , more and most), **that output will appear on your screen all at once** and thus you might lose something if said output is bigger than the number of lines of your terminal.

{% embed url="https://access.redhat.com/sites/default/files/attachments/12052018_systemd_6.pdf" %}
Systemmd cheatsheet
{% endembed %}

2- Visit the Client (Config scanner):

```
https://localhost:8834/#/
```

3- Stop Nessus:

```
sudo systemctl stop nessusd 
```
