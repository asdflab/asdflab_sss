

import sys
import os
import io
import signal
import traceback
import inspect
import syslog
import logging
import time
import datetime
import iso8601 # pip install iso8601
import threading
import multiprocessing
import queue
import subprocess

from Global import *


#def get_callername():
#    framelist= inspect.stack()
#    try:
#        return framelist[2].function
#    finally:
#        del framelist


#def get_exception(ex):
#    exc_buffer = io.StringIO()
#    traceback.print_exc(file=exc_buffer)
#    return exc_buffer.getvalue()

#def format_ts(ts):
#    if ts == None: return None
#    return ts.strftime('%Y-%m-%d %H:%M:%S.%f %z')




#--------------------------------------------------------------------------------------


class TimeTicker(object):

    def __init__(self, boundary, resolution, tick_proc, tick_args=[], autostart=False):
        self._timer= None
        self._lasttick= None
        self._running= False
        self._boundary= boundary
        self._resolution= resolution
        self._tick_proc= tick_proc
        self._tick_args= tick_args
        if (autostart): self.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if (not self._running): return
        self._running= False
        self._timer.join(3 * self._resolution)


    def _restart(self):
        self._timer= threading.Timer(self._resolution, self._tick)
        self._timer.start()

    def _tick(self):
        if (not self._running): return
        self._restart()

        PIT= datetime.datetime.now(datetime.timezone.utc)
        SEC= ((((PIT.hour)*60)+PIT.minute)*60)+PIT.second

        if not (SEC % self._boundary == 0): return
        if (SEC == self._lasttick): return
        self._lasttick= SEC

        if (self._tick_proc==None): return
        self._tick_proc(self._tick_args)


    def start(self):
        if (self._running): return
        self._running= True
        self._restart()
        return self

    def stop(self):
        self.__exit__(None, None, None)
        return self
        





class TaskWorker(object):
    instance= None

    def __init__(self, msgq, debuglevel, initmethod=None, initargs=[]):
        self.debuglevel= debuglevel
        self.msgq= msgq
        self.taskid= ''

        try:
            if initmethod != None:
                getattr(self, initmethod)(initargs)
        except Exception as exc:
            self.log_exception(exc)



    @staticmethod
    def _init(workerclass, msgq, debuglevel, initmethod=None, initargs=[]):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        TaskWorker.instance=workerclass(msgq, debuglevel, initmethod, initargs)

    @staticmethod
    def _run(taskname, taskid, taskargs=[]):
        obj=TaskWorker.instance
        if taskname=='': 
            taskname='run'
        mth=getattr(obj,taskname)
        obj.taskid= taskid
        try:
            mth(taskargs)
        finally:
            obj.taskid= ''

    def _log(self, severity, caller, message):
        ##self.msgq.put(['LOG', time.strftime('%Y%m%d-%H%M%S%z'), severity, os.getpid(), caller, self.taskid, message])
        self.msgq.put(['LOG', severity, os.getpid(), caller, self.taskid, message])
 

    def log(self, severity, message):
        self._log(severity, get_callername(), message)

    def log_proc_enter(self, args):
        if (3>self.debuglevel): return
        self._log(syslog.LOG_DEBUG, get_callername(), 'ENTER {}:{}'.format(len(args), '|'.join(map(str,args))))

    def log_proc_leave(self):
        if (3>self.debuglevel): return
        self._log(syslog.LOG_DEBUG, get_callername(), 'LEAVE')


    def log_exception(self, ex):
        self._log(syslog.LOG_EMERG, get_callername(), 'EXCEPTION '+get_exception(ex))

    def log_error(self, message):
        self._log(syslog.LOG_ERR, get_callername(), message)

    def log_warning(self, message):
        self._log(syslog.LOG_WARNING, get_callername(), message)

    def log_info(self, message):
        self._log(syslog.LOG_INFO, get_callername(), message)

    def log_debug(self, level, message):
        if (level>self.debuglevel): return
        self._log(syslog.LOG_DEBUG, get_callername(), message)



    def submit(self, taskname, taskid, taskargs=[]):
        self.msgq.put(['SUBMIT', taskname, taskid]+taskargs)

    def signaldone(self):
         self.msgq.put(['DONE'])


    #def initialize(self, args=[]):
    #    """Abstract"""
    #    pass

    #def run(self, args=[]):
    #    """Abstract"""
    #    pass



class TaskProcessor(object):

    def __init__(self, parallelprocesses=None, maxtasksperprocess=None, loghandler=None, debuglevel=0, workerclass=TaskWorker, initmethod=None, initargs=[]):
        self.mpctx= multiprocessing.get_context('fork')
        self.mpman= self.mpctx.Manager()
        self.msgq= self.mpman.Queue()
        self.pool= self.mpctx.Pool(
            processes=parallelprocesses, 
            maxtasksperchild=maxtasksperprocess, 
            initializer=TaskWorker._init, 
            initargs=[workerclass,self.msgq,debuglevel,initmethod,initargs]
        )
        self.ars= []
        self.doneflag= False
        self.workerclass= workerclass
        self.loghandler= loghandler

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pool.close()
        self.pool.join()
        while self._process_msgq(True):
            pass
        pass


    def _process_msgq(self,offhour):
        result= False
        while True:
            try:
                item=self.msgq.get_nowait()
                result= True
                if item[0]=='DONE':
                    self.doneflag= True
                    logging.info("{} [{}]: {}.{}[{}]: {}".format(syslog.LOG_INFO, os.getpid(), 'TaskProcessor', get_callername(), '', 'Recieved DONE-notification, awaiting completion of work-queue'))
                elif item[0]=='LOG':
                    #print("LOG {}".format(item))
                    logging.info("{} [{}]: {}.{}[{}]: {}".format(item[1], item[2], self.workerclass.__name__, item[3], item[4], item[5]))
                elif item[0]=='SUBMIT':
                    #print("SUBMIT {}".format(item))
                    if not offhour:
                        self.submit(item[1],item[2],(item[3:]))
            except (queue.Empty, ConnectionResetError, BrokenPipeError):
                break
        return result

    def _process_ars(self):
        self.ars= [ar for ar in self.ars if not ar.ready()]
        return len(self.ars)!=0

    def submit(self, taskname, taskid, taskargs=[]):
        self.ars.append(self.pool.apply_async(func=TaskWorker._run, args=[taskname,taskid,taskargs]))

    def isdone(self):
        return self.doneflag and len(self.ars)==0

    def process(self):
        try:
            self._process_msgq(False)
            self._process_ars()
        except (KeyboardInterrupt):
            pass
        return

    def process_loop(self):
        while not self.isdone():
            self.process()
            time.sleep(0.1)


    def terminate(self):
        self.pool.terminate()

    def cleanup(self):
        self.__exit__(None, None, None)


