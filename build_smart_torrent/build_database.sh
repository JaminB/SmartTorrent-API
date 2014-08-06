#!/bin/bash
apt-get install mysql-server
apt-get install python-mysqldb 
mysql -u root -p < st.sql
