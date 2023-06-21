
import uuid
import re

"macro part"

"users's tool"


import os

def filepath_search(dir):
    # dir example is "C:/Users/"
    path2 = os.path.dirname(dir)
    for path, dirs, files in os.walk(path2):
        print(os.path.join(path2,path))
        for file in files:
            file_path = os.path.join(path, file)
            print(file_path)
            if file_path.find('path_footprint.txt')>=0:
                folder_name = path
                folder_name = folder_name.replace("\\","/")
                folder_name = folder_name + '/ipocc_info'
                try:

                    if not os.path.isdir(folder_name):
                        os.makedirs(folder_name)
                    else:
                        pass
                except OSError:
                    print('Error: Creating directory. ' + folder_name)
                file = open(os.path.join(folder_name, "folder_name_for_ipocc.txt"), 'w')
                file.write(folder_name)
                file.close()

                break
            else:
                pass


def macaddress_ex(folder_name):
    Gen_key = ''.join(re.findall('..', '%012x' % uuid.getnode())).upper()
    # print(Gen_key)
    file = open(os.path.join(folder_name,"Gen_key.txt"),'w')
    file.write(Gen_key)
    file.close()

    return Gen_key

dir = "C:/Users/"
folder_name = filepath_search(dir)


info_path = 'C:/ipocc_info'
if not os.path.exists(info_path):
    os.makedirs(info_path)
else:
    pass

Gen_key = macaddress_ex(info_path)

