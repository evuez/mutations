from logging import debug, info


class Brain(object):
	ACTIONS = [
		Find,
		Duplicate,
		Rest,
		Turn,
		Forward
	]

	def __init__(self, body):
		self.body = body
		self.actions = [a(self.body) for a in self.ACTIONS]

	def tick(self):
		self.dna.next_choice(self.actions).tick()


class Action(object):
	def __init__(self, body):
		self.body = body

	def log(self):
		raise NotImplementedError

	def tick(self):
		raise NotImplementedError


class Move(Action):
	pass


class Find(Action):
	pass


class Duplicate(Action):
	pass


class Turn(Action):
	def log(self):
		debug("Body %s is turning", self.body.dna)

	def tick(self):
		speed = self.body.dna.next_float(0.6) - 0.3
		self.body.drain(amount)
		self.body.direction += speed
		while self.body.direction < 0:
			self.body.direction += 2 * pi
		while self.body.direction > 2 * pi:
			self.body.direction -= 2 * pi


class Forward(Action):
	def log(self):
		debug("Body %s is moving forward", self.body.dna)

	def tick(self):
		speed = self.body.dna.next_float(10) + 10
		self.body.drain(speed * 2)
		self.body.x += speed * cos(self.body.direction)
		self.body.y += speed * sin(self.body.direction)


class Rest(Action):
	pass
