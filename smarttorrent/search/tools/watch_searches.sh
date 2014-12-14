#! /bin/bash
while true
do	
	output="$(mysql -u st --password=tech0nsite! searches < show_table.sql)"
	previousOutput="$(cat output)"
	
	if [ "$output" != "$previousOutput" ];
		then
			echo "$output" > output
			echo "$previousOutput" > prevOutput
			diff output prevOutput |head -n 4 | mail -s 'SmartTorrent Search' 9198809427@vtext.com

	fi		
	sleep 5
	clear
done
