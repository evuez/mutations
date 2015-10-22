extern crate num;
extern crate rand;

use std::thread;

mod functions;
mod universe;
mod world;

// TODO
// Move world::{Dna, Body} to world::things
// Move functions to universe

fn main() {
    let mut god = universe::God::new([123; 4]);
    let mut body = god.spawn_body();

    let mut counter = 0;

    loop {
        body.step();
        println!("Pose: {}, Energy: {}", body.pose, body.energy);

        counter += 1;

        if body.energy < 0f32 {
            break;
        }
    }

    println!("Number of steps: {:?}", counter);
}
