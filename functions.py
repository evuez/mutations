def gaussian(gaussian, average, t=int):
	if average < 0:
		return t(-1)
	return t(max(min(average / 3.5 * gaussian + average, average * 2), 0))
