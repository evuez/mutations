from random import random
from math import sin, cos, pi, atan2


class NothingFoundError(Exception):
	pass


class NotInThatSpotError(Exception):
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

	def tick(self):
		raise NotImplementedError

	def recharge(self):
		raise NotImplementedError

	def drain(self, amount):
		self.energy -= amount
		return amount


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
		if self.dying:
			self.survive()
		elif self.dead:
			self.map.things.remove(self)
		else:
			self.move()

	@property
	def dying(self):
		return self.energy < self.MAX_ENERGY / 100
	
	@property
	def dead(self):
		return self.energy < 1

	def is_neighbor(thing):
		distance = sqrt(
			(thing.x - self.x)**2 +
			(thing.y - self.y)**2
		)
		if distance > self.RADIUS + thing.RADIUS:
			return False
		return True

	def recharge(self, amount):
		self.energy = min(self.energy + amount, MAX_ENERGY)

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
		if thing.is_neighbor(spot):
			self.stop()

	def survive(self):
		"""
		Used when dying to find an EnergyBank
		"""
		try:	
			self.next_spot.has(EnergyBank)
		except (AttributeError, NotInThatSpotError):
			self.next_spot = self._find(EnergyBank)
		except NothingFoundError:
			self.stop() # best thing to do to survive longer
		self.move_to(self.next_spot)

	def _find(thing_class, find_nearest=True):
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
		speed = random() * 10 + 10
		self.x += speed * cos(self.direction)
		self.y += speed * sin(self.direction)

	def _turn(self):
		speed = random() * 0.6 - 0.3
		self.direction += speed
		while self.direction < 0:
			self.direction += 2 * pi
		while self.direction > 2* pi:
			self.direction -= 2 * pi

	def mutate(self):
		pass


class EnergyBank(Thing):
	RADIUS = 5

	def __init__(self, map_):
		super().__init__(map_)
		self.energy = 20000 + random() * 10000
		self.max_energy = self.energy
		self.connected = frozenset()
		self.rate = random()

	def _connect(self, thing):
		thing.connection = self
		self.connected.add(thing)

	def _disconnect(self, thing):
		if thing.connection is self:
			thing.connection = None
		self.connected.discard(thing)

	def recharge(self):
		self.energy = self.max_energy * random() * 0.005

	def _supply(self):
		for thing in self.connected:
			if thing.connected is self:
				thing.recharge(self.drain(self.rate))
			else:
				self._disconnect(thing)

	def tick(self):
		self.recharge()
		self._supply()
		for thing in self.map.things:
			if thing is self:
				continue
			if isinstance(thing, self.__class__):
				continue
			self._connect(thing)
