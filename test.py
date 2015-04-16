from mutations import Map
from mutations import Body
from mutations import EnergyBank
import logging


logging.basicConfig(level=logging.INFO)


def test():
	map_ = Map(1000, 1000)
	for i in range(20):
		map_.add(EnergyBank(map_))
	for i in range(5000):
		map_.add(Body(map_))

	for i in range(1000):
		map_.tick()


if __name__ == '__main__':
	test()
