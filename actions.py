class Action(object):

	def __init__(self, body):
		self.body = body

	def _log(self):
		raise NotImplementedError

	def _execute(self):
		raise NotImplementedError

	def _drain(self):
		raise NotImplementedError

	def do(self):
		self._execute()
		self._drain()
		self._log()


class Find(Action):

	def _log(self):
		logging.info(
			"%s has found %d %s",
			self.body,
			len(self.found),
			self.thing_class
		)

	def _execute(self):
		pass # ffi

	def _drain(self):
		self.body.do_drain(
			God.count(self.thing_class) * self.body.dna.next_float()
		)

	def do(self, thing_class):
		self.thing_class = thing_class
		super().do()


class Absorb(Routine):

	def _log(self):
		logging.info(
			"%s has absorbed %d particles of gas!",
			self.body,
			self.absorbed
		)

	def _execute(self):
		self.absorbed = God.remove_all(self.body.find_nearby('Particle'))

	def _drain(self):
		self.body.do_drain(-self.absorbed * self.body.dna.next_float())
