# !!! Run this script using the python-executable that should run the application !!!


#--- Only import sys and os in the beginning
import sys
import os

#--- Switch to the script-directory and insert that as searchpath
install_localdir= os.path.dirname(__file__)
if install_localdir != '': 
    os.chdir(install_localdir)
install_localdir= os.getcwd()
sys.path.insert(0, install_localdir)

#--- Import other modules
import io


#--- Gather some information
install_python= sys.executable
with io.open('VERSION','r') as _file:
    install_version= _file.readline().strip()



print("install_python     = {}".format(install_python))
print("install_localdir   = {}".format(install_localdir))
print("install_version    = {}".format(install_version))


install_prefix= os.getenv('PREFIX', '/opt/asdflab_sss')
install_prefix_prefix= install_prefix if install_prefix != '/' else ''

install_cfgdir= os.getenv('CFGDIR', install_prefix_prefix+'/cfg')
install_logdir= os.getenv('LOGDIR', install_prefix_prefix+'/log')
install_bindir= os.getenv('BINDIR', install_prefix_prefix+'/bin')
install_libexecdir= os.getenv('LIBEXECDIR', install_prefix_prefix+'/libexec')
install_modulesdir= os.getenv('MODULESDIR', install_prefix_prefix+'/modules')

print("install_prefix     = {}".format(install_prefix))
print("install_cfgdir     = {}".format(install_cfgdir))
print("install_logdir     = {}".format(install_logdir))
print("install_bindir     = {}".format(install_bindir))
print("install_libexecdir = {}".format(install_libexecdir))
print("install_modulesdir = {}".format(install_modulesdir))
