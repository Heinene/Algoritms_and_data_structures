import sys

polov = -1
for line in sys.stdin:
    try:
        polov = int(line)
        break
    except:
        print('error')
if polov < 0:
    quit()

def bit(one, two):
    while one & 0b1 == 0b0 and two & 0b1 == 0b0:
        one >>= 0b1
        two >>= 0b1
    return two & 0b1 - one & 0b1

oper = []
while polov != 0:
    if polov & 0b1 == 0b0:
        oper.append('dbl')
        polov >>= 0b1
    elif polov == 0b11 or bit(polov - 0b1, polov + 0b1) > 0b0:
        oper.append('inc')
        polov -= 0b1
    else:
        oper.append('dec')
        polov += 0b1
print(*reversed(oper), sep='\n')
