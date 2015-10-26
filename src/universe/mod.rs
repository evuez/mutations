use std::sync::{Arc, Mutex, mpsc};
use std::thread;
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

    pub fn spawn_population(&mut self, body_count: i32) {
        let mut bodies = Vec::new();

        for _ in 0..body_count {
            bodies.push(self.spawn_body());
        }

        let (tx, rx) = mpsc::channel();

        for body in bodies {
            let mut body = Arc::new(Mutex::new(body));
            let (body, tx) = (body.clone(), tx.clone());

            thread::spawn(move || {
                let mut body = body.lock().unwrap();
                println!("Pose: {}, Energy: {}", body.pose, body.energy);
                tx.send(());
            });
        }

        for _ in 0..body_count {
            rx.recv();
        }
    }
}
