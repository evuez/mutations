extern crate num;
extern crate rand;

use std::vec::Vec;
use std::f32::consts::PI;
use num::FromPrimitive;
use rand::distributions::{Normal, Sample};
use rand::{Rand, Rng, ThreadRng};

mod functions;
mod things;
mod universe;


fn main() {
    let god = universe::God::new(123);
    let mut body = things::Body::new([13; 4]);

    let mut counter = 0;

    loop {
        body.step();
        println!("Pose: {}, Energy: {}", body.pose, body.energy);

        counter += 1;

        if body.energy < 0f32 {
            break;
        }
    }

    println!("{:?}", counter);
}
