#!/bin/bash
echo TARGET IP:
read ip
nmap --script-updatedb
mkdir ./reports
ports=$(nmap -p- --min-rate=1000 -T4 $ip | grep ^[0-9] | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)
nmap --script vuln -sV -p$ports $ip > ./reports/nmap.report.txt
