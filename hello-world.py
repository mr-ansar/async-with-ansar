import ansar.create as ar

def main(self):
	print('hello world')
	return 0

ar.bind(main)

if __name__ == '__main__':
	ar.create_object(main)

