#!/bin/bash
#Install dependent packages
apt-get install git
apt-get install apache2
apt-get install python
#Add our cgi-bin configuration
rm /etc/apache2/sites-enabled/000-default.conf
cp cgi-apache2.conf /etc/apache2/sites-available/
#Download our API
cd /tmp
git clone root@162.243.247.84:/var/www/smart_torrent.git
mv smart_torrent /var/www/api
#Give apache user proper permissions to cache
chown www-data:www-data /var/www/api/search/cache
#Give the apache user proper permissions to tmp file
chown www-data:www-data /var/www/api/utilities/data/tmp
#Give the apache user proper permissions to ips.list
chown www-data:www-data /var/www/api/utilities/ips.list
#Enable the CGI-bin modules
cd /etc/apache2/mods-enabled
ln -s ../mods-available/cgi.load .
cd ../sites-enabled
#Load our cgi-bin configuration
ln -s ../sites-available/cgi-apache2.conf
#Restart apache
service apache2 restart
