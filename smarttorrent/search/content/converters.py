#!/usr/bin/python

class date:
	def __init__(self, dateString):
		self.dateString = dateString
		self.months = {'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 'May' : '05', 'Jun' : '06', 'Jul': '07', 'Aug' : '08', 'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12'}  
	def convert(self):
		dateArray = self.dateString.split(' ')
		if len(dateArray[1]) > 1:
			return str(dateArray[2]) + "-" + self.months[dateArray[0]] + "-" + dateArray[1]
		else:
				
			return str(dateArray[2]) + "-" + self.months[dateArray[0]] + "-" + "0"+dateArray[1]
