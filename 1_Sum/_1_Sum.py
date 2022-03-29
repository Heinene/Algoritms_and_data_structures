import sys
import re
d = 0
elem = 0
plus = True
while True:
	ch = sys.stdin.read(1) 
	if re.findall(r'^[0-9]$', ch):
		elem=(elem*10)+int(ch)        
	else:      
		if plus== True:
			d+=elem                               
		if plus== False:
			d-=elem   
			plus=True
		if  re.findall(r'-', ch):
			plus = False
		elem=0    
	if not ch:
		break
print(d)