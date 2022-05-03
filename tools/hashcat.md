---
description: >-
  Hashcat uses precomputed dictionaries, rainbow tables and even brute-force
  approaches to find an effective and efficient way to crack passwords.  + GPU
  support.
---

# 🐱‍👤Hashcat

{% embed url="https://hashcat.net/hashcat/" %}

Benchmarking our device for Hashcat:

```
hashcat -b
```

to run hashcat:

```
hashcat -m <Hash_algo> -a <attack_type> -D2 <file_to_crack> <hash_dictionary> 
```

> \-m: 0 for md5, 1800 sha512(Unix) ex. Kali\
> \-a: 0 straight has crack\
> \-rule: more efficient attack as you can apply stuff like mangling. [A great discussion about rules](https://notsosecure.com/one-rule-to-rule-them-all/).\
> [read more also about mask me](https://www.4armed.com/blog/perform-mask-attack-hashcat/)[thod with Hashcat.](https://www.4armed.com/blog/perform-mask-attack-hashcat/) (for ex: ?l?l?l?l?l?a first 5 char are lower 6'th all possible char \[Symbols, Lower, Upper, Numbers])

{% hint style="info" %}
you can use `hashid 'hash-to-check'` or `hash-identifier` command on kali to check what Hashing Algorithm is used on the obtained hash value.
{% endhint %}

#### Cracking a MS office doc:

```
hashcat -a 0 -m 9600 --status <hash> <worldlist> --force
```

> `-a 0`: Set attack mode to the dictionary.
>
> `-m 9600`: Set method to MS Office 2013
>
> `--status`: Enable automatic update of the status screen
>
> `hash`: File containing crackable information
>
> for exmaple use this worldlist: /1000000-password-seclists.txt or whatever
