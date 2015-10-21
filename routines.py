import logging
from math import pi


class Routine(object):
	def __init__(self, body):
		self.body = body

	def _log(self):
		raise NotImplementedError

	def _execute(self):
		raise NotImplementedError

	def _drain(self):
		raise NotImplementedError

	def tick(self):
		self._execute()
		self._drain()
		self._log()


class Forward(Routine):

	def _log(self):
		logging.info("%s has moved forward at %dPPT!", self.body, self.speed)

	def _execute(self):
		self.speed = self.body.dna.next_float(10) + 10
		self.body.x += self.speed * cos(self.body.direction)
		self.body.y += self.speed * sin(self.body.direction)

	def _drain(self):
		self.body.do_drain(self.speed * 2)


class Turn(Routine):

	def _log(self):
		logging.info(
			"%s has turned to %d at %dPPT!",
			self.body,
			self.body.direction,
			self.speed
		)

	def _execute(self):
		self.speed = self.dna.next_float(0.6) - 0.3
		self.body.direction += self.speed
		while self.body.direction < 0:
			self.body.direction += 2 * pi
		while self.body.direction > 2 * pi:
			self.body.direction -= 2 * pi

	def _drain(self):
		self.body.do_drain(self.speed)


class Rest(Routine):

	def _log(self):
		logging.info("%s has rested!", self.body)

	def _execute(self):
		pass

	def _drain(self):
		self.body.do_drain(-self.body.next_float(10))
