# !!! Run this install-script using the python-executable that should run the application !!!


#--- Only import sys and os in the beginning ----------
import sys
import os

#--- Switch to the script-directory and insert that as searchpath ----------
install_localdir= os.path.dirname(__file__)
if install_localdir != '': 
    os.chdir(install_localdir)
install_localdir= os.getcwd()
sys.path.insert(0, install_localdir)
sys.path.insert(1, install_localdir+'/tools')

#--- Import other modules ----------
import io




#--- Gather interpreter and version information ----------
def _tryint(X):
    try:
        return int(X)
    except:
        pass
    return X

install_pythonexec= sys.executable
install_pythonver= tuple([str(X) for X in sys.version_info])
with io.open('VERSION','r') as _file:
    install_appver= _file.readline().strip()
    install_pythonmin= tuple(_file.readline().strip().split('.'))

#print(">> install_pythonexec = {}".format(install_pythonexec))
#print(">> install_pythonver  = {}".format(install_pythonver))
#print(">> install_localdir   = {}".format(install_localdir))
#print(">> install_appver     = {}".format(install_appver))
#print(">> install_pythonmin  = {}".format(install_pythonmin))

print("Using python exec: {}".format(install_pythonexec))

if tuple([_tryint(X) for X in install_pythonver]) < tuple([_tryint(X) for X in install_pythonmin]):
    print("!! ERROR: This application needs python version at least {}".format('.'.join(install_pythonmin)))
    exit(1)

print("Using python ver: {}".format('.'.join(install_pythonver)))


#--- Gather folder information ----------

install_prefix= os.getenv('PREFIX', '/opt/asdflab_sss')
install_prefix_prefix= install_prefix if install_prefix != '/' else ''

install_cfgdir= os.getenv('CFGDIR', install_prefix_prefix+'/cfg')
install_logdir= os.getenv('LOGDIR', install_prefix_prefix+'/log')
install_bindir= os.getenv('BINDIR', install_prefix_prefix+'/bin')
install_libexecdir= os.getenv('LIBEXECDIR', install_prefix_prefix+'/libexec')
install_modulesdir= os.getenv('MODULESDIR', install_prefix_prefix+'/modules')

#print(">> install_prefix     = {}".format(install_prefix))
#print(">> install_cfgdir     = {}".format(install_cfgdir))
#print(">> install_logdir     = {}".format(install_logdir))
#print(">> install_bindir     = {}".format(install_bindir))
#print(">> install_libexecdir = {}".format(install_libexecdir))
#print(">> install_modulesdir = {}".format(install_modulesdir))


print("Creating directories...")
for _dir in (install_prefix, install_cfgdir, install_logdir, install_bindir, install_libexecdir, install_modulesdir):
    print("  ...{}".format(_dir))
    os.makedirs(_dir, exist_ok=True)
