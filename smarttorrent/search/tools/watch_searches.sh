#! /bin/bash
while true
do	
	output="$(mysql -u st --password=tech0nsite! searches < show_table.sql)"
	previousOutput="$(cat output)"
	
	if [ "$output" != "$previousOutput" ];
		then
			echo CHANGE!
			echo "$output" > output
			echo "$output"
	else
			echo "$output"

	fi		
	sleep 2
	clear
done
