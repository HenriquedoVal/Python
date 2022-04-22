class UnderflowError(Exception):
	pass

class Array:
	def __init__(self):
		self.array = [None for i in range(7)]
		self.count = 0
		self.head = 0
		self.tail = 0

	def printar(self):
		print('tail - head - count -', 'array'.center(20))
		print(str(self.tail).center(4), str(self.head).center(4), str(self.count).center(5), *self.array, sep='   ')

	def put(self, x):
		if self.count >= 7:
			raise OverflowError

		self.array[self.tail] = x
		self.tail = (self.tail + 1) % 7
		self.count += 1
		self.printar()

	def get(self):
		if self.count == 0:
			raise UnderflowError

		aux = self.array[self.head]
		self.array[self.head] = None
		self.head = (self.head + 1) % 7
		self.count -= 1

		self.printar()
		return aux


