extern crate num;
extern crate rand;


use std::vec::Vec;
use num::FromPrimitive;
use rand::distributions::{Normal, Sample};
use rand::{Rand, Rng, ThreadRng};


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
