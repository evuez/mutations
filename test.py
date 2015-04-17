import logging
from time import sleep

from pyglet import app
from pyglet.window import Window
from pyglet.clock import schedule_interval

from render import MapView
from mutations import Map
from mutations import Body
from mutations import EnergyBank


logging.basicConfig(level=logging.DEBUG)


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
	for i in range(2):
		map_.add(EnergyBank(map_))
	for i in range(50):
		map_.add(Body(map_))

	def update(dt):
		map_.tick()

	window = Window(map_.width, map_.height)
	map_view = MapView(map_)
	schedule_interval(update, 0.1)

	@window.event
	def on_draw():
		window.clear()
		map_view.draw()


	app.run()


if __name__ == '__main__':
	test_view()
