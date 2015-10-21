extern crate num;
extern crate rand;


use std::vec::Vec;
use std::f32::consts::PI;
use num::FromPrimitive;
use rand::distributions::{Normal, Sample};
use rand::{Rand, Rng, ThreadRng};


const MAP_WIDTH: f32 = 500.0;
const MAP_HEIGHT: f32 = 500.0;


struct Position {
    x: f32,
    y: f32,
    d: f32,
}


struct God {
    seed: u32,
}

struct Dna {
    seed: u32,
    length: i32,
    rate: f64,
    seeds: Vec<i64>,
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

impl God {
    fn new(seed: u32) -> God {
        God {
            seed: seed
        }
    }

    fn gaussian<T: FromPrimitive>() -> T {
        FromPrimitive::from_f64(
            Normal::new(2.0, 3.5).sample(&mut rand::thread_rng())
        ).expect("Cannot convert to given type")
    }
}

impl Dna {
    fn new(seed: u32) -> Dna {
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


fn main() {
    let god = God::new(123);
    let dna = Dna::new(123);

    println!("Seed: {}", god.seed);

    println!(
        "Seed: {}\nLength: {}\nRate: {}\nSeeds: {:?}",
        dna.seed,
        dna.length,
        dna.rate,
        dna.seeds,
    );
}
