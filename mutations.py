import logging
from random import Random
from math import sin, cos, pi, atan2, sqrt, exp
from collections import deque


class NothingFoundError(Exception):
	pass


class NotInThatSpotError(Exception):
	pass


class ConnectionRefusedError(Exception):
	pass


class Map(object):

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.things = []
		self.population = 0
		self.age = 0

	def tick(self):
		self.age += 1
		self.census()
		for thing in self.things:
			thing.tick()

	def add(self, thing):
		self.things.append(thing)

	def census(self, report=True):
		current = len(self.things)
		if not report:
			return current
		if current > self.population:
			logging.info(
				"Population increased: %d (was %d)",
				current, self.population
			)
		if current < self.population:
			logging.info(
				"Population decreased: %d (was %d)",
				current, self.population
			)
		self.population = current


class DNA(object):
	AVERAGE_LENGTH = 14
	AVERAGE_MUTATION_RATE = 0.2
	LENGTH = -1

	def __init__(self, seed_):
		self.seed = seed_
		init_rand = Random(self.seed)
		self.length = 1 + self.gauss(
			init_rand.gauss(0, 1),
			self.AVERAGE_LENGTH
		)
		self.mutation_rate = self.gauss(
			init_rand.gauss(0, 1),
			self.AVERAGE_LENGTH,
			float
		)
		self.seeds = deque(maxlen=self.length)
		self.genes = deque(maxlen=self.length)
		for s in range(self.length):
			self.seeds.append(init_rand.getrandbits(64))
			self.genes.append(Random(self.seeds[-1]))

		def __str__(self):
			return str(id(self))

	def gauss(self, gaussian, average, t=int):
		if average < 0:
			return -1
		return max(min(t(average / 3.5 * gaussian + average), average * 2), 0)

	def rotate(self):
		self.seeds.rotate(-1)
		self.genes.rotate(-1)

	def mutate(self, seed_):
		gen = Random(seed_)
		if gen.random() < self.mutation_rate:
			logging.warning('Mutation happened')
			self.genes[0] = Random(gen.getrandbits(64))

	def next_float(self, max_=1):
		self.rotate()
		return self.genes[0].random() * max_

	def next_bool(self):
		self.rotate()
		return bool(self.genes[0].getrandbits(1))

	def next_long(self):
		self.rotate()
		return self.genes[0].getrandbits(32)

	def next_choice(self, seq):
		self.rotate()
		return self.genes[0].choice(seq)



class Abilities(object):
	def __init__(self):
		self.move = True

	def toggle(ability):
		setattr(
			self,
			ability,
			not getattr(self, ability)
		)


class Spot(object):
	RADIUS = None

	def __init__(self, thing):
		self.thing = thing
		self.x = thing.x
		self.y = thing.y
		self.RADIUS = thing.RADIUS

	def has(self, thing_class):
		if isinstance(self.thing, thing_class):
			return True
		raise NotInThatSpotError


class Thing(object):
	RADIUS = 2

	def __init__(self, map_, seed_):
		self.map = map_
		self.dna = DNA(seed_)
		self.dna.mutate(self.dna.next_long())
		self.energy = None
		self.x = self.dna.next_float(self.map.width)
		self.y = self.dna.next_float(self.map.height)
		self.direction = self.dna.next_float(pi * 2)
		# self.weight = self.dna.next_float(5)

	@property
	def dead(self):
		return self.energy < 1

	def tick(self):
		raise NotImplementedError

	def recharge(self):
		raise NotImplementedError

	def connect(self, thing):
		if thing is self:
			raise ConnectionRefusedError
		thing.accept(self)

	def soft_connect(self, thing):
		try:
			self.connect(thing)
		except ConnectionRefusedError:
			return False
		return True

	def accept(self, thing):
		raise NotImplementedError

	def _drain(self, amount):
		logging.debug(
			"%s %d is draining, %0.2f remaining",
			self.__class__.__name__, id(self), self.energy
		)
		self.energy -= amount
		self.energy = max(self.energy, 0)
		return amount

	def is_neighbor(self, thing):
		distance = sqrt(
			(thing.x - self.x)**2 +
			(thing.y - self.y)**2
		)
		if distance > self.RADIUS + thing.RADIUS:
			return False
		return True


class Body(Thing):

	def __init__(self, map_, seed_):
		super().__init__(map_, seed_)
		self.age = 0
		self.energy = 6500 + self.dna.next_float(1000)
		self.decay_rate = 8000 + self.dna.next_float(5000)
		self.abilities = Abilities()
		self.connection = None
		self.next_spot = None

	def tick(self):
		self._decay()
		self._try_duplicate()
		if self.rested:
			self._disconnect(EnergyBank)
		if self.dead:
			logging.debug("Body %d died", id(self))
			self.map.things.remove(self)
		elif self.dying:
			logging.debug("Body %d is dying", id(self))
			self.survive()
		else:
			self.move()

	@classmethod
	def copy(cls, body):
		new_body = cls(body.map, body.dna.seed)
		new_body.energy = body.energy
		new_body.x, new_body.y = body.x, body.y
		return new_body

	@property
	def dying(self):
		return self.energy < self.max_energy / 3

	@property
	def dead(self):
		return (
			super().dead or
			(self.age / self.decay_rate) ** 4 > self.dna.next_float()
		)

	@property
	def rested(self):
		return (
			self.energy >
			self.max_energy / (self.dna.next_float(1.5) + 1)
		)

	@property
	def sick(self):
		return self.dna.next_float > 0.997

	@property
	def max_energy(self):
		return 4.8 * exp(3 / 4 - self.age / 2000) * (self.age + 500)

	def _decay(self):
		self.age += 1

	def _disconnect(self, thing_class=None):
		"""
		Disconnect from current spot. If thing_class
		specified, will only disconnect if current
		spot is instance of thing.
		"""
		if isinstance(self.connection, thing_class):
			self.next_spot = None
			self.connection = None
			self.abilities.move = True

	def recharge(self, amount):
		logging.debug("Body %d is recharging", id(self))
		self.energy = min(self.energy + amount, self.max_energy)

	def move(self):
		if not self.abilities.move:
			return
		if self.dna.next_float() > 0.7:
			self._turn()
		self._forward()

	def stop(self):
		self.abilities.move = False

	def move_to(self, spot):
		if not self.abilities.move:
			return
		self.direction = atan2(
			spot.y - self.y,
			spot.x - self.x
		)
		self._forward()
		if self.soft_connect(spot.thing):
			logging.debug("Body %d reached %s %d",
				id(self),
				spot.thing.__class__.__name__,
				id(spot.thing)
			)
			self.stop()

	def survive(self):
		"""
		Used when dying to find an EnergyBank
		"""
		logging.debug("Body %d is trying to survive", id(self))
		try:
			self.next_spot.has(EnergyBank)
		except (AttributeError, NotInThatSpotError):
			self.next_spot = self._find(EnergyBank)
			logging.debug(
				"Body %d has found EnergyBank %d",
				id(self), id(self.next_spot.thing)
			)
		except NothingFoundError:
			self.stop() # best thing to do to survive longer
			logging.info("Body %d stopped to survive longer", id(self))
		self.move_to(self.next_spot)

	def _find(self, thing_class, find_nearest=True):
		"""
		Return first match if find_nearest is False,
		return nearest otherwise.
		raise NothingFoundError if no matches
		"""
		if not issubclass(thing_class, Thing):
			raise NotImplementedError
		nearest = None
		for thing in self.map.things:
			if not isinstance(thing, thing_class):
				continue
			if not find_nearest:
				return thing
			if nearest is None:
				nearest = thing
				dist_nearest = (
					(thing.x - self.x) ** 2 +
					(thing.y - self.y) ** 2
				)
			dist_current = (thing.x - self.x) ** 2 + (thing.y - self.y) ** 2
			if dist_current < dist_nearest:
				nearest = thing
				dist_nearest = dist_current
		return Spot(nearest)

	def _forward(self):
		logging.debug("Body %d is moving forward", id(self))
		speed = self.dna.next_float(10) + 10
		self._drain(speed * 2)
		self.x += speed * cos(self.direction)
		self.y += speed * sin(self.direction)

		self.x = self.x if self.x < self.map.width else 0
		self.x = self.x if self.x > 0 else self.map.width
		self.y = self.y if self.y < self.map.height else 0
		self.y = self.y if self.y > 0 else self.map.height

	def _turn(self):
		logging.debug("Body %d is turning", id(self))
		speed = self.dna.next_float(0.6) - 0.3
		self._drain(speed)
		self.direction += speed
		while self.direction < 0:
			self.direction += 2 * pi
		while self.direction > 2 * pi:
			self.direction -= 2 * pi

	def _try_duplicate(self):
		if self.dna.next_float() < 0.99:
			return
		self._drain(1000 * self.dna.next_float() + self.energy / 2)
		if self.dead:
			return
		logging.debug("Body %d duplicated", id(self))
		self.map.add(Body.copy(self))

	def mutate(self):
		if self.dna.next_float() < 0.999:
			return


class EnergyBank(Thing):
	RADIUS = 10

	def __init__(self, map_, seed_):
		super().__init__(map_, seed_)
		self.energy = 20000 + self.dna.next_float(10000)
		self.max_energy = self.energy
		self.connected = set()
		self.rate = self.dna.next_float(100)

	@property
	def empty(self):
		return self.dead

	def _connect(self, thing):
		thing.connection = self
		self.connected.add(thing)

	def _disconnect(self, thing):
		if thing.connection is self:
			thing.connection = None
		self.connected.discard(thing)

	def _drain(self, amount):
		if self.empty:
			logging.debug("EnergyBank %d is empty", id(self))
			return 0
		super()._drain(amount)
		return amount

	def accept(self, thing):
		if self.empty:
			raise ConnectionRefusedError
		if thing.dead:
			raise ConnectionRefusedError
		if not self.is_neighbor(thing):
			raise ConnectionRefusedError
		logging.debug(
			"EnergyBank %d accept connection from %d",
			id(self), id(thing)
		)
		self._connect(thing)

	def recharge(self):
		logging.debug(
			"EnergyBank %d is recharging, %0.2f remaining",
			id(self), self.energy
		)
		self.energy += self.max_energy * self.dna.next_float(0.005)
		self.energy = min(self.energy, self.max_energy)

	def _supply(self):
		connected = set(self.connected)
		for thing in connected:
			if thing.dead or thing.connection is not self:
				self._disconnect(thing)
			else:
				thing.recharge(self._drain(self.rate))
		self.connected = connected

	def tick(self):
		self.recharge()
		self._supply()
