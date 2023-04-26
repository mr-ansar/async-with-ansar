import ansar.create as ar

class DeviceControl(object):
	def __init__(self, control='control'):
		self.control = control

class DevicePoll(object):
	def __init__(self, poll='poll'):
		self.poll = poll

ar.bind(DeviceControl)
ar.bind(DevicePoll)
