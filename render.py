import math
from collections import deque
from colorsys import hsv_to_rgb
from pyglet.gl import glBegin
from pyglet.gl import glEnd
from pyglet.gl import glColor3f
from pyglet.gl import glVertex2f
from pyglet.gl import GL_TRIANGLE_FAN
from pyglet.gl import GL_POLYGON
from mutations import Body


def circle(cx, cy, r, color):
	segments = int(2 * math.pi * r)

	cos = math.cos(2 * math.pi / segments)
	sin = math.sin(2 * math.pi / segments)

	x, y = r, 0

	glBegin(GL_TRIANGLE_FAN)
	glColor3f(*color)
	for counter in range(segments):
		glVertex2f(x + cx, y + cy)
		x, y = cos * x - sin * y, sin * x + cos * y
	glEnd()


def square(x, y, size, color):
	size /= 2
	x1, y1 = x - size, y - size
	x2, y2 = x + size, y + size

	glColor3f(*color)
	glBegin(GL_POLYGON)
	glVertex2f(x1, y1)
	glVertex2f(x1, y2)
	glVertex2f(x2, y2)
	glVertex2f(x2, y1)
	glEnd()


class MapView(object):

	def __init__(self, map_):
		self.map = map_

	def draw(self):
		for thing in self.map.things:
			if isinstance(thing, Body):
				color_rgb = hsv_to_rgb(
					1 / 3 * thing.energy / thing.max_energy,
					1, 1
				)
				circle(
					thing.x, thing.y,
					thing.RADIUS,
					color_rgb
				)
			else:
				circle(
					thing.x, thing.y,
					thing.RADIUS,
					[1 * thing.energy / thing.max_energy] * 3
				)


class GraphView(object):

	def __init__(self, map_):
		self.map = map_
		self.censuses = deque(maxlen=200)

	def draw(self):
		self.censuses.append(self.map.census(False))
		max_ = max(self.censuses)
		count = len(self.censuses)
		for k, census in enumerate(self.censuses):
			square(
				k * (500 / count),
				census * (100 / max_),
				1,
				(1, 1, 1)
			)
