#---------------------------------------------------------------------------------------------
#!/usr/bin/python
import os
import getpass
import pexpect
import base64


#Color For Terminal
r = '\033[31m' #red
b = '\033[34m' #blue
g = '\033[32m' #green


print ("##################################################")
print ("##################################################")

print ("Scanning Options")
print ("[1] KR")
print ("[2] JP")
print ("[3] SG")
print ("[4] CN")
print ("[5] US")
print ("[6] UK")

option = input("Choose your Scanning Option:")


uid = 'minsu.kim2'#raw_input("Active directory Accout: ")
#upw = getpass.getpass()
#upw = base64.decodestring('MDUxMEFsc3RuJA==')
#upw = raw_input("Active directory Password: ")
upw = '0510Alstn)'
#os.system("ssh " + uid + "@10.40.194.253")

if option == '1': #KR
   host = '10.40.194.253'
elif option == '2': #JP
   host = '10.42.255.106'
elif option == '3': #SG
   host = '10.212.8.31'
elif option == '4': #CN
   host = '10.41.255.240'
elif option == '5': #US
   host = '10.10.253.6'
elif option == '6': #UK
   host = '10.20.253.6'
else:
 print ("Goodbye")

def ssh(uid, host):
    return 'ssh %s@%s' % (uid, host)

def wait_password():
    return 'Password:'

child = pexpect.spawn(ssh(uid, host))
child.setwinsize(400, 400)
child.expect(wait_password())
child.sendline(upw)
child.interact()
child.close()
