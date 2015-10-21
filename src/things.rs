extern crate num;
extern crate rand;

use std::f32::consts::PI;
use std::vec::Vec;
use num::FromPrimitive;
use rand::{Rand, Rng, ThreadRng};
use universe::God;


const MAP_WIDTH: f32 = 500.0;
const MAP_HEIGHT: f32 = 500.0;


struct Position {
    x: f32,
    y: f32,
    d: f32,
}

pub struct Dna {
    pub seed: u32,
    pub length: i32,
    pub rate: f64,
    pub seeds: Vec<i64>,
    genes: Vec<ThreadRng>,
    current: i32,
}

struct Body {
    dna: Dna,
    position: Position,
    age: i32,
    energy: f32,
    decay: f32,
}


impl Position {
    fn new_random(dna: &mut Dna) -> Position {
        Position {
            x: dna.next::<f32>() * MAP_WIDTH,
            y: dna.next::<f32>() * MAP_WIDTH,
            d: dna.next::<f32>() * PI,
        }
    }
}


impl Dna {
    pub fn new(seed: u32) -> Dna {
        let mut rng = rand::thread_rng();

        let length = 1 + God::gaussian::<i32>();
        let mut seeds = Vec::with_capacity(length as usize);
        let mut genes = Vec::with_capacity(length as usize);

        for _ in 0..length {
            seeds.push(rng.gen::<i64>());
            genes.push(rand::thread_rng());
        }

        Dna {
            seed: seed,
            length: length,
            rate: God::gaussian::<f64>(),
            seeds: seeds,
            genes: genes,
            current: 0,
        }
    }

    fn next<T: Rand>(&mut self) -> T {
        if self.current >= self.length - 1 {
            self.current = 0;
        } else {
            self.current += 1;
        }

        self.genes[self.current as usize].gen::<T>()
    }
}

impl Body {
    fn new(seed: u32) -> Body {
        let mut dna = Dna::new(seed);

        Body {
            position: Position::new_random(&mut dna),
            age: 0,
            energy: 6500.0 + dna.next::<f32>() * 1000.0,
            decay: 8000.0 + dna.next::<f32>() * 5000.0,
            dna: dna,
        }
    }
}
