#!/bin/bash
echo TARGET IP:
read ip
searchsploit -u
mkdir ./reports
ports=$(nmap -p- --min-rate=1000 -T4 $ip | grep ^[0-9] | cut -d '/' -f 1 | tr '\n' ',' | sed s/,$//)
nmap -sV --open -oX ./reports/nmap.xml -p$ports $ip; searchsploit -v --nmap ./reports/nmap.xml > ./reports/final.exploit.report.txt
