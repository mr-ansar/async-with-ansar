import random
import ansar.create as ar

random.seed()

def adjust(period):
	s = int(period / 0.1) + 1
	b = int(s * 0.75)	# Quicker.
	e = int(s * 1.5)		# Slower.
	a = random.randrange(b, e) * 0.1
	if a < 0.25:
		return 0.25
	return a

class DbQuery(ar.Point, ar.Stateless):
    def __init__(self, query):
        ar.Point.__init__(self)
        ar.Stateless.__init__(self)
        self.query = query

def DbQuery_Start(self, message):
	period = adjust(1.75)
	self.start(ar.T1, period)

def DbQuery_T1(self, message):
	self.complete('selection')

def DbQuery_Stop(self, message):
	self.complete(ar.Aborted())

DB_QUERY_DISPATCH = (ar.Start, ar.T1, ar.Stop)

ar.bind(DbQuery, DB_QUERY_DISPATCH)

def main(self):
	q = self.create(DbQuery, 'query')
	m = self.select(ar.Completed, ar.Stop)
	if isinstance(m, ar.Stop):
		self.send(m, q)
		self.select(ar.Completed)
		return ar.Aborted()
	selection = m.value
	return 0

ar.bind(main)

if __name__ == '__main__':
	ar.create_object(main)
