use std::sync::{Arc, Mutex, mpsc};
use std::thread;
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

    pub fn spawn_population(&mut self, body_count: i32) {
        let mut self_ = Arc::new(Mutex::new(self));
        let (tx, rx) = mpsc::channel();

        for _ in 0..body_count {
            let (self_, tx) = (self_.clone(), tx.clone());

            thread::spawn(move || {
                let mut self_ = self_.lock().unwrap();
                self_.spawn_body();
                tx.send(());
            });
        }

        for _ in 0..body_count {
            rx.recv();
        }
    }
}
