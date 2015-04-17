import logging
from random import random
from math import sin, cos, pi, atan2, sqrt


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

	def tick(self):
		for thing in self.things:
			thing.tick()

	def add(self, thing):
		self.things.append(thing)


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

	def __init__(self, map_):
		self.map = map_
		self.energy = None
		self.x = random() * self.map.width
		self.y = random() * self.map.height
		self.direction = random() * pi * 2

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
		logging.info(
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
	MAX_ENERGY = 10000

	def __init__(self, map_):
		super().__init__(map_)
		self.age = 0
		self.energy = 6500 + random() * 1000
		self.decay = 8000 + random() * 5000
		self.abilities = Abilities()
		self.connection = None
		self.next_spot = None

	def tick(self):
		if self.dead:
			logging.info("Body %d died", id(self))
			self.map.things.remove(self)
		elif self.dying:
			logging.info("Body %d is dying", id(self))
			self.survive()
		else:
			self.move()

	@property
	def dying(self):
		return self.energy < self.MAX_ENERGY / 2

	def recharge(self, amount):
		logging.info("Body %d is recharging", id(self))
		self.energy = min(self.energy + amount, self.MAX_ENERGY)

	def move(self):
		if self.abilities.move:
			if random() > 0.7:
				self._turn()
			self._forward()

	def stop(self):
		self.abilities.move = False

	def move_to(self, spot):
		self.direction = atan2(
			spot.y - self.y,
			spot.x - self.x
		)
		self._forward()
		if self.soft_connect(spot.thing):
			logging.info("Body %d reached energy bank %d",
				id(self), id(spot.thing)
			)
			self.stop()

	def survive(self):
		"""
		Used when dying to find an EnergyBank
		"""
		logging.info("Body %d is trying to survive", id(self))
		try:
			self.next_spot.has(EnergyBank)
		except (AttributeError, NotInThatSpotError):
			self.next_spot = self._find(EnergyBank)
			logging.info(
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
				dist_nearest = (thing.x - self.x)**2 + (thing.y - self.y)**2
			dist_current = (thing.x - self.x)**2 + (thing.y - self.y)**2
			if dist_current < dist_nearest:
				nearest = thing
				dist_nearest = dist_current
		return Spot(nearest)

	def _forward(self):
		logging.info("Body %d is moving forward", id(self))
		speed = random() * 10 + 10
		self._drain(speed * 2)
		self.x += speed * cos(self.direction)
		self.y += speed * sin(self.direction)

	def _turn(self):
		logging.info("Body %d is turning", id(self))
		speed = random() * 0.6 - 0.3
		self._drain(speed)
		self.direction += speed
		while self.direction < 0:
			self.direction += 2 * pi
		while self.direction > 2* pi:
			self.direction -= 2 * pi

	def mutate(self):
		pass


class EnergyBank(Thing):
	RADIUS = 10

	def __init__(self, map_):
		super().__init__(map_)
		self.energy = 20000 + random() * 10000
		self.max_energy = self.energy
		self.connected = set()
		self.rate = random() * 100

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
		super()._drain(amount)
		if self.empty:
			logging.info("EnergyBank %d is empty", id(self))
			return 0
		return amount

	def accept(self, thing):
		if self.empty:
			raise ConnectionRefusedError
		if thing.dead:
			raise ConnectionRefusedError
		if not self.is_neighbor(thing):
			raise ConnectionRefusedError
		logging.info(
			"EnergyBank %d accept connection from %d",
			id(self), id(thing)
		)
		self._connect(thing)

	def recharge(self):
		logging.info(
			"EnergyBank %d is recharging, %0.2f remaining",
			id(self), self.energy
		)
		self.energy += self.max_energy * random() * 0.005
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
