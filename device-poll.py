import random
import ansar.create as ar
from device_if import DeviceControl, DevicePoll

random.seed()

def adjust(period):
	s = int(period / 0.1) + 1
	b = int(s * 0.75)	# Quicker.
	e = int(s * 1.5)		# Slower.
	a = random.randrange(b, e) * 0.1
	if a < 0.25:
		return 0.25
	return a

def device_poll(self, settings, control):
	period = adjust(0.5)
	self.start(ar.T1, period)
	m = self.select(ar.T1, ar.Stop)
	if isinstance(m, ar.Stop):
		return ar.Aborted()
	return DevicePoll('status')

ar.bind(device_poll)

default_input = DeviceControl()

if __name__ == '__main__':
	ar.create_object(device_poll, compiled_input=default_input)
