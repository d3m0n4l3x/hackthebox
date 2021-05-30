#!/usr/bin/python3
# All steps of the script herein:
#1. Ask if Port / Vulnerability Scan needs to be conducted
#1.1. If YES, ask for TARGET IP Address
#1.2. Update NMAP script feeds
#1.3. Conduct Port / Vulnerability Scan, and save report to a file
#1.4. Tell the report's path after the scan is done
#2. Ask if Web Scan needs to be conducted
#2.1. If YES, ask for TARGET URL
#2.2. Tell the website's structure after dirbustering is done
#2.3. Tell CMS information of the website after CMS Detection is done
#2.4. Tell downloaded website path after the download is done
#2.5. Ask if KEYWORD(s) needs to be specified, and what the KEYWORD(s) is
#2.6. Tell the KEYWORD report's path

import subprocess

def port_vuln_scan(target_ip):
    command = 'nmap --script-updatedb > /dev/null 2>&1; ports=$(nmap -p- --min-rate=1000 -T4 ' + target_ip + ' | grep ^[0-9] | cut -d \'/\' -f 1 | tr \'\\n\' \',\' | sed s/,$//); nmap --script vuln -sV -p$ports ' + target_ip + ' > ./reports/' + target_ip + '.scan_report.txt'
    subprocess.call(command, shell=True)
    print('Scan is complete, and the report is stored at ./reports/' + target_ip + '.scan_report.txt')

def search_keyword_in_website(single_keyword):
    command5 = 'grep -nR ' + single_keyword + ' ./temp/ | sed G > ./reports/keyword_' + single_keyword + '_searching_report.txt'
    subprocess.call(command5, shell=True)
    print("The KEYWORD " + single_keyword + " searching report is stored at ./reports/keyword_" + single_keyword + '_searching_report.txt')

#0: Initialize the scan:
print("Initializing ... ")
subprocess.call("rm -Rf ./reports ./temp; mkdir ./reports; mkdir ./temp", shell=True)

#1:
answer = input("Would you like to conduct Port / Vulnerability Scan (Y/N) : ")
answer = str(answer)
if answer.lower() == 'y':
    scan = 1
elif answer.lower() == 'n':
    scan = 0
else:
    print("Unknown answer, exit ...")
    exit()

#1.1:
if scan == 1:
    global_target_ip = input("What is the TARGET IP ADDRESS : ")

#1.2 + 1.3 + 1.4:
    print("Port / Vulnerability Scan is in progress ... ")
    port_vuln_scan(global_target_ip)

#2:
answer2 = input("Would you like to conduct Web Scan (Y/N) : ")
answer2 = str(answer2)
if answer2.lower() == 'y':
    web_scan = 1
elif answer2.lower() == 'n':
    web_scan = 0
else:
    print("Unknown answer, exit ...")
    exit()

#2.1:
if web_scan == 1:
    global_target_url = input("What is the TARGET URL : ")
    web_scan_report_name = global_target_url[:]
    web_scan_report_name = web_scan_report_name.replace(':', '_')
    web_scan_report_name = web_scan_report_name.replace('/', '_')
    web_scan_target_domain = global_target_url[:]
    web_scan_target_domain = web_scan_target_domain.replace('http://','')
    web_scan_target_domain = web_scan_target_domain.replace('https://','')
    web_scan_target_domain = web_scan_target_domain.replace('/','')
else:
    exit()

#2.2:
print("Website Directory Bustering is in progress ... ")
command2 = 'rm -Rf ./reports/' + web_scan_report_name + '.dirbustering_report.txt; timeout 5m dirb ' + global_target_url + ' -S -o ./reports/' + web_scan_report_name + '.dirbustering_report.txt > /dev/null 2>&1'
subprocess.call(command2, shell=True)
print('Dirbustering is complete, and the report is stored at ./reports/' + web_scan_report_name + '.dirbustering_report.txt')

#2.3:
print("Website CMS Detection is in progress ... ")
command3 = 'rm -Rf ./reports/' + web_scan_report_name + '.cms_detection_report.txt; whatweb ' + global_target_url + ' > ./reports/' + web_scan_report_name + '.cms_detection_report.txt'
subprocess.call(command3, shell=True)
print('CMS Detection is complete, and the report is stored at ./reports/' + web_scan_report_name + '.cms_detection_report.txt')

#2.4:
print("Website Mirroring is in progress ... ")
command4 = 'wget --recursive --page-requisites --adjust-extension --span-hosts --convert-links --restrict-file-names=windows --domains ' + web_scan_target_domain + ' --protocol-directories --mirror -e robots=off --directory-prefix=./temp --no-parent ' + global_target_url + ' > /dev/null 2>&1'
#command4 = 'wget --protocol-directories --directory-prefix=./temp -r ' + global_target_url + ' > /dev/null 2>&1'
subprocess.call(command4, shell=True)
print('Website Mirroring is complete, and the website is stored at ./temp/')

#2.5 + 2.6:
answer3 = input("Would you like to find any KEYWORD\(s\) in the website (Y/N) : ")
if answer3.lower() == 'y':
    search_keyword = 1
elif answer3.lower() == 'n':
    search_keyword = 0
else:
    print("Unknown answer. Exit ...")
    exit()
keywords = ["username", "password"]
if search_keyword != 1:
    exit()
else:
    keywords_entered = input("Any KEYWORD\(s\) \(e.g.: username,password\) : ")
if keywords_entered == '':
    searching_keywords = keywords[:]
else:
    searching_keywords = keywords_entered.split(',')
#print(searching_keywords)
print("Keyword Searching is in progress ... ")
for each_keyword in searching_keywords:
    #print(each_keyword)
    search_keyword_in_website(each_keyword)

#The End:
exit()
