import re
import sys
import array
mas = [] 
sozd_mas = 0
size = 0 
kolvelem = -1 
for string in sys.stdin:
    if (string=='\n'):
            pass      
    else: 
        if((re.match(r'set_size\s\d*',string)) or (re.match(r'push\s\w*',string)) or (re.match(r'pop',string)) or (re.match(r'print',string)))==None:
            print('error')             
        if(re.match(r'^set_size\s\d*$',string)):
            if(sozd_mas==0):
                sozd_mas=sozd_mas +1
                size= int (sum( [float(i) for i in  re.findall(r'-?\d+\d*', string)]))
                mas=[0]*size                      
            else:
                print('error')                
        if(re.match(r'push\s\w*',string)):
            schet=0
            for i in string:
                if(i==' '):
                    schet=schet+1
            if (sozd_mas==0):
                print('error')
            else:
                if(schet!=1): 
                        print('error')
                else:
                    if (kolvelem + 1> size - 1):
                        print('overflow')
                    else:
                        if ((schet==1)):
                            num=string[5:len(string)-1] 
                            kolvelem=kolvelem+1
                            mas[kolvelem]=num                              
        if((re.match(r'pop',string))):
            if(sozd_mas==0):
                print('error')
            elif((re.match(r'^pop$',string))):
                    if(kolvelem<0):
                        print('underflow')
                    else:
                        print(mas[kolvelem])
                        kolvelem=kolvelem-1
            elif ((re.match(r'^pop',string))):
               print('error')
            
          
        if(re.match(r'print',string)):
            if(re.findall(r'^print$',string)):
                if (sozd_mas==0):
                    print ('error')
                elif (kolvelem<0):
                    print ('empty')
                elif kolvelem>=0:
                    print(' '.join(map(str,mas[0:kolvelem+1])))
            else:
                print('error')