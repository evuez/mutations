extern crate num;
extern crate rand;

use std::f32::consts::PI;
use std::fmt::{Display, Formatter, Result};
use std::vec::Vec;
use num::FromPrimitive;
use rand::{Rng, Rand, SeedableRng, XorShiftRng};
use functions;
use universe::God;


const MAP_WIDTH: f32 = 500.0;
const MAP_HEIGHT: f32 = 500.0;
const AVERAGE_LENGTH: f64 = 14.0; // TMP
const AVERAGE_MUTATION_RATE: f64 = 0.2; // TMP


pub struct Pose {
    pub x: f32,
    pub y: f32,
    pub d: f32,
}

pub struct Dna {
    seed: [u32; 4],
    length: u32,
    rate: f64,
    seeds: Vec<[u32; 4]>,
    genes: Vec<XorShiftRng>,
    current: u32,
}

pub struct Body {
    dna: Dna,
    pub pose: Pose,
    age: i32,
    pub energy: f32,
    decay: f32,
}


impl Pose {
    fn new_random(dna: &mut Dna) -> Pose {
        Pose {
            x: dna.next::<f32>() * MAP_WIDTH,
            y: dna.next::<f32>() * MAP_WIDTH,
            d: dna.next::<f32>() * PI,
        }
    }
}

impl Display for Pose {
    fn fmt(&self, f: &mut Formatter) -> Result {
        write!(f, "({}, {}, {})", self.x, self.y, self.d)
    }
}

impl Dna {
    // On 10th of December it should be OK to use associated constants.
    // const AVERAGE_LENGTH: f64 = 14.0;
    // const AVERAGE_MUTATION_RATE: f64 = 0.2;

    pub fn new(seed: [u32; 4]) -> Dna {
        let mut rng = XorShiftRng::from_seed(seed);

        let length = 1 + functions::gaussian(&mut rng, AVERAGE_LENGTH) as u32;
        let mut seeds = Vec::with_capacity(length as usize);
        let mut genes = Vec::with_capacity(length as usize);

        for _ in 0..length {
            let seed = [
                rng.gen::<u32>(),
                rng.gen::<u32>(),
                rng.gen::<u32>(),
                rng.gen::<u32>()
            ];

            seeds.push(seed);
            genes.push(XorShiftRng::from_seed(seed));
        }

        Dna {
            seed: seed,
            length: length,
            rate: functions::gaussian(&mut rng, AVERAGE_MUTATION_RATE),
            seeds: seeds,
            genes: genes,
            current: 0,
        }
    }

    fn next<T: Rand>(&mut self) -> T {
        self.current += 1;
        if self.current > self.length - 1 { self.current = 0; }

        self.genes[self.current as usize].gen::<T>()
    }
}

impl Body {
    pub fn new(seed: [u32; 4]) -> Body {
        let mut dna = Dna::new(seed);

        Body {
            pose: Pose::new_random(&mut dna),
            age: 0,
            energy: 6500.0 + dna.next::<f32>() * 1000.0,
            decay: 8000.0 + dna.next::<f32>() * 5000.0,
            dna: dna,
        }
    }

    fn drain(&mut self, amount: f32) -> f32 {
        self.energy -= amount;
        amount
    }

    // Routines
    pub fn step(&mut self) -> () {
        if self.dna.next::<f32>() > 0.7 {
            self.turn();
        }
        self.forward();
    }

    // Subroutines
    fn forward(&mut self) -> () {
        let speed = self.dna.next::<f32>() * 10.0 + 10.0;
        self.pose.x += speed * self.pose.d.cos();
        self.pose.y += speed * self.pose.d.sin();

        self.drain(speed * 2.0);
    }

    fn turn(&mut self) -> () {
        let speed = self.dna.next::<f32>() * 0.6 - 0.3;
        self.pose.d += speed;
        while self.pose.d < 0.0 {
            self.pose.d += 2.0 * PI;
        }
        while self.pose.d > 2.0 * PI {
            self.pose.d -= 2.0 * PI;
        }

        self.drain(speed);
    }

    // Actions
}
