from time import sleep
from mutations import Map
from mutations import Body
from mutations import EnergyBank
import logging


logging.basicConfig(filename='test.log', level=logging.INFO)


def test():
	map_ = Map(1000, 1000)
	for i in range(2):
		map_.add(EnergyBank(map_))
	for i in range(5):
		map_.add(Body(map_))

	for i in range(1000):
		map_.tick()


if __name__ == '__main__':
	test()
