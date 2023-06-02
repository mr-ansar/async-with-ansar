import random
import ansar.create as ar
from device_if import DeviceControl, DevicePoll

random.seed()

def adjust(period):
    s = int(period / 0.1) + 1
    b = int(s * 0.75)    # Quicker.
    e = int(s * 1.5)     # Slower.
    a = random.randrange(b, e) * 0.1
    if a < 0.25:
        return 0.25
    return a

def db_query(self, query):
    period = adjust(0.75)
    self.start(ar.T1, period)
    m = self.select(ar.T1, ar.Stop)
    if isinstance(m, ar.Stop):
        return ar.Aborted()
    return 'selection'

ar.bind(db_query)

class NetworkRequest(object):
    def __init__(self, request='request'):
        self.request = request

class NetworkResponse(object):
    def __init__(self, response='response'):
        self.response = response

class NetworkDown(object):
    pass

ar.bind(NetworkRequest)
ar.bind(NetworkResponse)
ar.bind(NetworkDown)

def one_chance_in(possibles):
    r = random.randrange(0, possibles)
    return r == 0

def connect():
    if one_chance_in(20):
        return False
    return True

def request_response(request):
    if one_chance_in(100):
        return None
    return 'response'

def disconnect():
    pass

class INITIAL: pass
class READY: pass
class STANDBY: pass

class NetworkServer(ar.Point, ar.StateMachine):
    def __init__(self):
        ar.Point.__init__(self)
        ar.StateMachine.__init__(self, INITIAL)

def NetworkServer_INITIAL_Start(self, message):
    if connect():
        return READY
    self.start(ar.T1, 5.0)
    return STANDBY

def NetworkServer_READY_NetworkRequest(self, message):
    response = request_response(message.request)
    if response is None:
        self.reply(NetworkDown())
        self.start(ar.T1, 5.0)
        return STANDBY
    self.reply(NetworkResponse(response))
    return READY

def NetworkServer_READY_Stop(self, message):
    disconnect()
    self.complete(ar.Aborted())

def NetworkServer_STANDBY_NetworkRequest(self, message):
    self.reply(NetworkDown())
    return STANDBY

def NetworkServer_STANDBY_T1(self, message):
    if connect():
        return READY
    self.start(ar.T1, 5.0)
    return STANDBY

def NetworkServer_STANDBY_Stop(self, message):
    self.complete(ar.Aborted())

NETWORK_SERVER_DISPATCH = {
    INITIAL: (
        (ar.Start,), ()
    ),
    READY: (
        (NetworkRequest, ar.Stop), ()
    ),
    STANDBY: (
        (NetworkRequest, ar.T1, ar.Stop), ()
    ),
}

ar.bind(NetworkServer, NETWORK_SERVER_DISPATCH)

def main(self):
    api = self.create(NetworkServer)

    q = self.create(db_query, 'query')
    self.send(NetworkRequest('request'), api)
    p = self.create(ar.Process, 'device-poll', input=DeviceControl('control'))
    a = [q, p]

    def stop():
        for t in a:
            self.send(ar.Stop(), t)
            self.select(ar.Completed)
        self.send(ar.Stop(), api)
        self.select(ar.Completed)

    try:
        while len(a) > 0:
            m = self.select(NetworkResponse, NetworkDown, ar.Completed, ar.Stop)
            if isinstance(m, ar.Stop):
                return ar.Aborted()
            elif isinstance(m, ar.Completed):
                a.remove(self.return_address)
            elif isinstance(m, NetworkResponse):
                pass
            elif isinstance(m, NetworkDown):
                pass
    finally:
        stop()
    return 0

ar.bind(main)

if __name__ == '__main__':
    ar.create_object(main)
