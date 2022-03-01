
import uuid
import re

"macro part"

"users's tool"
def macaddress_ex():
    Gen_key = ''.join(re.findall('..', '%012x' % uuid.getnode())).upper()
    # print(Gen_key)
    file = open("D:/Gen_key.txt",'w')
    file.write(Gen_key)
    file.close()

    return Gen_key

Gen_key = macaddress_ex()