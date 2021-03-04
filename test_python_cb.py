#!/usr/bin/env python

import sys
import time
import PyTango

Cb = PyTango.utils.EventCallback
 
def test_cb(dev_name, attr_name, event_type, subscription_time):   
    d = PyTango.DeviceProxy(dev_name)
    cb = Cb()
    while True:
        print('subscribing')
        id = d.subscribe_event(attr_name, event_type, cb)
        time.sleep(subscription_time)
        print('unsubscribing')
        d.unsubscribe_event(id)

if __name__ == '__main__':
    try:
        dev_name = sys.argv[1]
        attr_name = sys.argv[2]
        event_type_str = sys.argv[3]
        if event_type_str == 'periodic':
            event_type = PyTango.EventType.PERIODIC_EVENT
        elif event_type_str == 'change':
            event_type = PyTango.EventType.CHANGE_EVENT
        else:
            raise ValueError('Accepted event_type is: periodic or change')
        subscription_time = float(sys.argv[4])
    except Exception as e:
        print('usage: test_python_cb <dev_name> <attr_name> ' +
              '<event_type> <subscription_time>')
        raise e
    test_cb(dev_name, attr_name, event_type, subscription_time)

