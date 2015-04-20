import logging
from random import random

from pyglet import app
from pyglet.window import Window
from pyglet.clock import schedule_interval
from pyglet.gl import glClearColor

from render import MapView
from mutations import Map
from mutations import Body
from mutations import EnergyBank


logging.basicConfig(level=logging.INFO)


def test():
	map_ = Map(1000, 1000)
	for i in range(2):
		map_.add(EnergyBank(map_))
	for i in range(5):
		map_.add(Body(map_))

	for i in range(1000):
		map_.tick()


def test_view():
	map_ = Map(500, 500)
	for i in range(10):
		map_.add(EnergyBank(map_, random()))
	for i in range(10):
		map_.add(Body(map_, random()))

	def update(dt):
		map_.tick()

	window = Window(map_.width, map_.height)
	map_view = MapView(map_)
	schedule_interval(update, 0.1)

	@window.event
	def on_draw():
		glClearColor(.5, .6, .6, 1)
		window.clear()
		map_view.draw()


	app.run()


if __name__ == '__main__':
	test_view()
