use std::vec::Vec;
use rand::{Rng, SeedableRng, XorShiftRng};

mod functions;
mod world;


pub struct Universe {
    rng: XorShiftRng,
}


impl Universe {
    pub fn new(seed: [u32; 4]) -> Universe {
        Universe { rng: XorShiftRng::from_seed(seed) }
    }

    fn next_seed(&mut self) -> [u32; 4] {
        [
            self.rng.gen::<u32>(),
            self.rng.gen::<u32>(),
            self.rng.gen::<u32>(),
            self.rng.gen::<u32>()
        ]
    }

    pub fn spawn_body(&mut self) -> world::Body {
        world::Body::new(self.next_seed())
    }

    pub fn spawn_population(&mut self, body_count: i32) -> Vec<world::Body> {
        let mut population = Vec::new();

        for _ in 0..body_count {
            population.push(self.spawn_body());
        }

        population
    }
}
