import os

def output():
    # o = str(os.system("cat Apache/Apache_2k.log | ./logmine"))
    # return o
    return '%s'%str(os.system("cat Apache/Apache_2k.log | ./logmine"))

print(output())