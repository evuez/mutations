import math
from colorsys import hsv_to_rgb
from pyglet.gl import glBegin
from pyglet.gl import glEnd
from pyglet.gl import glColor3f
from pyglet.gl import glVertex2f
from pyglet.gl import GL_TRIANGLE_FAN
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
