extern crate num;
extern crate rand;

use std::vec::Vec;
use std::f32::consts::PI;
use num::FromPrimitive;
use rand::distributions::{Normal, Sample};
use rand::{Rand, Rng, ThreadRng};

mod things;
mod universe;


fn main() {
    let god = universe::God::new(123);
    let dna = things::Dna::new(123);

    println!("Seed: {}", god.seed);

    println!(
        "Seed: {}\nLength: {}\nRate: {}\nSeeds: {:?}",
        dna.seed,
        dna.length,
        dna.rate,
        dna.seeds,
    );
}
