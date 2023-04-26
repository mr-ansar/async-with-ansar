import random
import ansar.create as ar

random.seed()

def adjust(period):
	s = int(period / 0.1) + 1
	b = int(s * 0.75)	# Faster
	e = int(s * 1.5)		# Slower
	a = random.randrange(b, e) * 0.1
	if a < 0.25:
		return 0.25
	return a

def db_query(self, query):
	period = adjust(0.75)
	self.start(ar.T1, period)
	self.select(ar.T1)
	return 'selection'

ar.bind(db_query)

def main(self):
	q = self.create(db_query, 'query')
	m = self.select(ar.Completed)
	selection = m.value
	return 0

ar.bind(main)

if __name__ == '__main__':
	ar.create_object(main)
