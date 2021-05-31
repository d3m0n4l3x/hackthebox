#!/bin/sh
rm -Rf ./reports
mkdir ./reports
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall >/dev/null 2>&1 && chmod 755 msfinstall > /dev/null && ./msfinstall > /dev/null
echo KEYWORD:
read keyword
grep -nR $keyword /opt/metasploit-framework/embedded/framework/modules/exploits > ./reports/$keyword.report.txt
find /opt/metasploit-framework/embedded/framework/modules/exploits -name "*$keyword*" -type f -print >> ./reports/$keyword.report.txt
echo The report is stored at ./reports/$keyword.report.txt
