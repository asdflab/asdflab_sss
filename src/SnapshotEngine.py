

import gc

import syslog
import logging
import importlib.util
import regex

from Global import *
import TaskScheduling


def GetModule(PATH):
    _spec= importlib.util.spec_from_file_location("MOD", PATH)
    _result= importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_result)
    return _result

def CheckFunction(OBJ, FUNC):
    #return FUNC in dir(OBJ) and callable(getattr(OBJ, FUNC))
    return FUNC in dir(OBJ) and inspect.isfunction(getattr(OBJ, FUNC))




#======================================================================================================
class SnapshotWorker(TaskScheduling.TaskWorker):


    #---------------------------------------------
    def Initialize(self, args=[]):
        self.modules= {}

    #---------------------------------------------
    def GetModule(self, type, org, name):
        type= regex.sub(r'[\\\/\$\.\:]','', type)
        org=  regex.sub(r'[\\\/\$\.\:]','', org)
        name= regex.sub(r'[\\\/\$\.\:]','', name)

        if not type in ['database','bulkstorage','stateinfo','docinfo']:
            raise Exception('Unknown moduletype: '+type)

        modulename= type+'/'+org+'/'+name
        filename= './modules/'+modulename+'.py'
        module= self.modules.get(modulename, None)

        if module==None:
            _spec= importlib.util.spec_from_file_location(modulename, filename)
            module= importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(module)
            self.modules[modulename]= module

        return module



##END class SnapshotWorker



#======================================================================================================
class SnapshotWorker_Default(SnapshotWorker):


    #---------------------------------------------
    def Initialize(self, args=[]):
        self.log_proc_enter(args)
        try:

            super().Initialize(args)

            (_AgentID, _MainDB, _Daemon, ) = args

            self.log_debug(1, 'Initialize worker')
            for _VAR in ['_AgentID', '_Daemon', '_MainDB']:
                self.log_debug(4, '  {}={}'.format(_VAR, locals()[_VAR]))

            self.AgentID= _AgentID
            self.MainDB= _MainDB
            self.Daemon= _Daemon


            self.log_debug(2, 'Completed')
        except Exception as ex:
            self.log_exception(ex)
        finally:
            self.log_proc_leave()

    ##END def Initialize




    #---------------------------------------------
    def DaemonTick(self, args=[]):
        self.log_proc_enter(args)
        try:
            self.log_debug(1, 'Daemontick')

            if self.Daemon:
                time.sleep(1)
                self.submit('Snapshot', '', [False, 0])
            else:
                self.signaldone()


            self.log_debug(2, 'Completed')
        except KeyboardInterrupt:
            pass
        except Exception as ex:
            self.log_exception(ex)
        finally:
            self.log_proc_leave()

    ##END def DaemonTick



    #---------------------------------------------
    def Snapshot(self, args=[]):
        self.log_proc_enter(args)
        try:

            (_ToplevelTask, _SnapshotID, )= args

            self.log_debug(1, 'Run snapshot')
            for _VAR in ['_ToplevelTask', '_SnapshotID']:
                self.log_debug(4, '  {}={}'.format(_VAR, locals()[_VAR]))

            self.log_debug(1, 'X={}'.format(len(gc.get_objects())))

            #MOD= GetModule('./mod-stateinfo-imapbackup.py')
            MOD= self.GetModule('stateinfo', 'asdflab' ,'imapbackup')
            self.log_debug(1, 'X={}'.format(len(gc.get_objects())))

            del MOD
            self.log_debug(1, 'X={}'.format(len(gc.get_objects())))

            #MOD= GetModule('./mod-stateinfo-imapbackup.py')
            MOD= self.GetModule('stateinfo', 'asdflab' ,'imapbackup')
            self.log_debug(1, 'X={}'.format(len(gc.get_objects())))

            del MOD
            self.log_debug(1, 'X={}'.format(len(gc.get_objects())))

            #MOD= GetModule('./mod-stateinfo-imapbackup.py')
            MOD= self.GetModule('stateinfo', 'asdflab' ,'imapbackup')
            self.log_debug(1, 'X={}'.format(len(gc.get_objects())))


            if _ToplevelTask:
                self.signaldone()
            self.log_debug(2, 'Completed')


        except KeyboardInterrupt:
            pass
        except Exception as ex:
            self.log_exception(ex)
        finally:
            self.log_proc_leave()

    ##END def Snapshot


##END class SnapshotWorker_Default







#======================================================================================================
class SnapshotEngine(object):


    #---------------------------------------------
    def __init__(self, verbosity):
        self.verbosity= verbosity

    #---------------------------------------------
    def log_output(self, severity, caller, message):
        logging.info("{} [{}]: {}.{}[{}]: {}".format(
            severity, 
            os.getpid(), 
            self.__class__.__name__, 
            caller, 
            '', 
            message
        ))


    #---------------------------------------------
    def log_critical(self, message):
        self.log_output(syslog.LOG_CRIT, get_callername(), message)

    #---------------------------------------------
    def log_info(self, message):
        self.log_output(syslog.LOG_INFO, get_callername(), message)

    #---------------------------------------------
    def log_debug(self, level, message):
        if (level>self.verbosity): return
        self.log_output(syslog.LOG_DEBUG, get_callername(), message)








##END class SnapshotEngine





#======================================================================================================
class DefaultEngine(SnapshotEngine):

    #---------------------------------------------
    def __init__(self, verbosity, initargs=[]):
        super().__init__(verbosity)
        self.started= False
        self.taskprocessor= TaskScheduling.TaskProcessor(
            parallelprocesses=    1, 
            maxtasksperprocess=   15, 
            loghandler=           None, 
            #loghandler=           log_output, 
            debuglevel=           verbosity,
            workerclass=          SnapshotWorker_Default, 
            initmethod=           'Initialize',
            initargs=             initargs
        )
        self.timeticker= TaskScheduling.TimeTicker(
            boundary=             10, 
            resolution=           0.1, 
            tick_proc=            self._daemontick,
            tick_args=            [],
            autostart=            False
        )

    #---------------------------------------------
    def __enter__(self):
        self.started= True
        self.timeticker.start()
        return self

    #---------------------------------------------
    def __exit__(self, exc_type, exc_value, traceback):
        self.timeticker.stop()
        self.taskprocessor.cleanup()

    #---------------------------------------------
    def _daemontick(self, args=[]):
        self.taskprocessor.submit('DaemonTick', '', [False])



    #---------------------------------------------
    def SubmitManualSnapshot(self, args=[]):
        if not self.started: return
        self.taskprocessor.submit('Snapshot', '', [True]+args)



    #---------------------------------------------
    def LoopUntilDone(self):
        if not self.started: return

        try:
            while not self.taskprocessor.isdone():
                self.taskprocessor.process()
                time.sleep(0.1)
        except (SystemExit, KeyboardInterrupt):
            self.log_info('Stopping')
            self.timeticker.stop()
            self.taskprocessor.terminate()





## END class DefaultEngine
