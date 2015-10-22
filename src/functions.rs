use rand::distributions::normal::Normal;
use rand::distributions::Sample;
use rand::XorShiftRng;


pub fn gaussian(rng: &mut XorShiftRng, average: f64) -> f64 {
	if average < 0.0 {
		return -1.0;
	}
	(average / 3.5 * Normal::new(0.0, 1.0).sample(rng) + average)
		.min(average * 2.0)
		.max(0.0)
}
