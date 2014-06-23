import sys
#Config Location
configFile = "/var/www/api/smarttorrent/config"
#DO NOT EDIT BELOW THIS LINE#
config = open(configFile, "r")
options = ["ip_list", "wordlist_location", "utility_data", "search_cache"]
variables = {}
lineCount = 0
for line in config:
	lineCount+=1
	p1 = line.strip().replace(" ", "").split(" ")
	p2 = line.strip().replace(" ", "").split("=")
	if line.strip() != '' and line[0] != '#':
		for option in options:
			if p1[0].lower().strip() == option or p2[0].lower().strip() == option:
				if len(p2) == 2:
					if p2[1].strip() != "":
						variables.update({option:p2[1]})
				
					else:
						print "Line " + str(lineCount) + " error: must follow form 'variable = someValue' ."
						sys.exit()
				elif len(p2) > 2:
						print "Line " + str(lineCount) + " error: multiple assignments not supported' ."
						sys.exit()
				else:
					print "Line " + str(lineCount) + " error: must follow form 'variable = someValue' ."
					sys.exit()
	
