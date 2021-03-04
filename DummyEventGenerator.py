import PyTango
import sys
import time
import threading

class EventGeneratorThread(threading.Thread):

    def __init__(self, dev, attr_name, period):
        super(EventGeneratorThread,self).__init__()
        self.dev = dev
        self.attr_name = attr_name
        self.period = period

    def run(self):
        while not self.dev._stop_flag:
            self.dev.info_stream('Emitting %d event' % self.dev.attr)
            self.dev.push_change_event(self.attr_name, self.dev.attr)
            self.dev.info_stream('Sleeping %f seconds' % self.period)
            time.sleep(self.period)
            self.dev.attr += 1


class DummyEventGeneratorClass(PyTango.DeviceClass):

    cmd_list = { 'Start' : [ [ PyTango.ArgType.DevFloat, "Number" ],
                             [ PyTango.ArgType.DevVoid, "" ] ],
                 'Stop' : [ [ PyTango.ArgType.DevVoid, "" ],
                                     [ PyTango.ArgType.DevVoid, ""] ],
    }

    attr_list = { 'attr' : [ [ PyTango.ArgType.DevLong ,
                                    PyTango.AttrDataFormat.SCALAR ,
                                    PyTango.AttrWriteType.READ] ]
    }
    
    
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type("TestDevice")
        
class DummyEventGenerator(PyTango.Device_4Impl):

    #@PyTango.DebugIt()
    def __init__(self,cl,name):
        PyTango.Device_4Impl.__init__(self, cl, name)
        self.info_stream('In DummyEventGenerator.__init__')
        DummyEventGenerator.init_device(self)

    @PyTango.DebugIt()
    def init_device(self):
        self.info_stream('In Python init_device method')
        self.set_state(PyTango.DevState.ON)
        self.attr = 0
        self.set_change_event('attr', True, False)
        self._thread = None
        self._stop_flag = False


    #------------------------------------------------------------------

    @PyTango.DebugIt()
    def delete_device(self):
        self.info_stream('PyDsExp.delete_device')

    #------------------------------------------------------------------
    # COMMANDS
    #------------------------------------------------------------------

    @PyTango.DebugIt()
    def is_Start_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    @PyTango.DebugIt()
    def Start(self, period):
        self.info_stream('GenerateEvents %s', period)
        if self._thread and self._thread.isAlive():
            self.debug_stream('Thread is still alive. Execute Stop command...')
            PyTango.Except.throw_exception('Busy', 
                                           'The previous command execution is still running', 
                                           'Start')
        else:
            self._stop_flag = False
            self.debug_stream('Starting thread...')
            self._thread = EventGeneratorThread(self, 'attr', period)
            self._thread.setDaemon(True)
            self._thread.start()
        return 

    #------------------------------------------------------------------
    @PyTango.DebugIt()
    def is_Stop_allowed(self):
        return self.get_state() == PyTango.DevState.ON

    @PyTango.DebugIt()
    def Stop(self):
        self._stop_flag = True
        return 

    #------------------------------------------------------------------
    # ATTRIBUTES
    #------------------------------------------------------------------

    @PyTango.DebugIt()
    def read_attr_hardware(self, data):
        self.info_stream('In read_attr_hardware')

    @PyTango.DebugIt()
    def read_attr(self, the_att):
        self.info_stream("read_attr")
        the_att.set_value(self.attr)

    @PyTango.DebugIt()
    def is_attr_allowed(self, req_type):
        return self.get_state() in (PyTango.DevState.ON,)

if __name__ == '__main__':
    util = PyTango.Util(sys.argv)
    util.add_class(DummyEventGeneratorClass, DummyEventGenerator)

    U = PyTango.Util.instance()
    U.server_init()
    U.server_run()

