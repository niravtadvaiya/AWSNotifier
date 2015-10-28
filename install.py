#!/usr/bin/env python
import os
import platform 
import subprocess

def pip_install():
        subprocess.call(['sudo pip install django==1.8.5'],shell=True)
        subprocess.call(['sudo pip install nexmo'],shell=True)
        subprocess.call(['sudo pip install httplib2'],shell=True)

def create_startup():
        cwd = os.getcwd()
        file_content = '#!/bin/bash' + '\n'
        file_content += '# Defalt-Start: 1 3 5' + '\n'
        file_content += '# chkconfig: 2345 20 80' + '\n'
        file_content += '. /etc/rc.d/init.d/functions' + '\n'
        file_content += 'python {0}/manage.py runserver 0.0.0.0:9033 --insecure &'.format(cwd)
        file_content += '\nexit 0'
        with open("/etc/init.d/start_aws_nexmo","wb") as f:
                f.write(file_content)
        f.close()
        os.chdir('/etc/init.d')
        subprocess.call(['sudo chmod +x start_aws_nexmo'],shell=True)
        subprocess.call(['sudo /sbin/chkconfig --add start_aws_nexmo'],shell=True)
        subprocess.call(['sudo /sbin/chkconfig start_aws_nexmo on'],shell=True)
        return True
                
def install(cmd):
        linux_cmd = "sudo {0} ".format(cmd)
        subprocess.call([linux_cmd + ' update -y '],shell=True)
        subprocess.call([linux_cmd + ' install -y python-pip '],shell=True)
        pip_install()
        create_startup()

def arch_linux():
        subprocess.call(['sudo pacman -Syu'],shell=True)
        subprocess.call(['sudo pacman -S python-pip '],shell=True)
        pip_install()
        create_startup()
def windows():
        os.system("pip install django==1.8.5")
        os.system("pip install nexmo")
        os.system("pip install httplib2")
        get_curret = os.getcwd()
        current = "start /B c:/Python27/python.exe {0}/manage.py runserver 0.0.0.0:9033 --insecure %*".format(get_curret)

        with open("aws_alert.bat","wb") as f:
                f.write(current)
        f.close()
        try:
                from getpass import getuser
                import shutil
                get_username = getuser()
                path_copy = "C:/Users/{0}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup".format(get_username)
                shutil.copy("aws_alert.bat", path_copy)
                os.system("aws_alert.bat")

        except:
                print "Copy and paste aws_alert.bat to Program startup.\n"
                print "Step1 : Open Run using window+R key.\n"
                print "Step2 : Type shell:startup\n"
                print "Step3 : Copy aws_alert.bat file to Startup folder.\n"



if __name__ == '__main__':
        get_current = os.getcwd()
        if platform.system().lower() == "windows":
                import sys
                windows()
                print "AWS alert installed successfully."
                #command = '{0}/manage.py runserver 0.0.0.0:9033 --insecure %*'.format(get_current)
                #os.system(command)
                sys.exit(0)
        distro = platform.linux_distribution()[0].lower()
        if distro in ['debian','ubuntu']:
                        install('apt-get')
                        print "AWS alert installed successfully."
        if distro in ['centos linux','centos','fedora','redhat']:
                        install('yum')
                        print "AWS alert installed successfully."
        if distro == 'Arch Linux':
                        arch_linux()
        subprocess.call(['python {0}/manage.py runserver 0.0.0.0:9033 --insecure &'.format(get_current)],shell=True)
