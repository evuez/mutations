import logging
from argparse import ArgumentParser
from random import random

from pyglet import app
from pyglet.window import Window
from pyglet.clock import schedule_interval
from pyglet.gl import glClearColor

from render import SimView
from render import GraphView
from mutations import Map
from mutations import Body
from mutations import EnergyBank


parser = ArgumentParser(description='Start a Mutations simulation.')
parser.add_argument('--width', dest='map_width', default=500, type=int)
parser.add_argument('--height', dest='map_height', default=500, type=int)
parser.add_argument('--banks', dest='banks', default=5, type=int)
parser.add_argument('--bodies', dest='bodies', default=200, type=int)
values = parser.parse_args()

logging.basicConfig(level=logging.INFO)


def test_view():
	global map_width
	map_ = Map(values.map_width, values.map_height)
	for i in range(values.banks):
		map_.add(EnergyBank(map_, random()))
	for i in range(values.bodies):
		map_.add(Body(map_, random()))

	def update(dt):
		map_.tick()


	sim = Window(map_.width, map_.height)
	sim_view = SimView(map_)
	schedule_interval(update, 0.1)

	@sim.event
	def on_draw():
		glClearColor(.5, .6, .6, 1)
		sim.clear()
		sim_view.draw()


	graph = Window(500, 100)
	graph_view = GraphView(map_)

	@graph.event
	def on_draw():
		graph.clear()
		graph_view.draw()


	app.run()


if __name__ == '__main__':
	test_view()
