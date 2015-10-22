extern crate num;
extern crate rand;

use num::FromPrimitive;
use rand::distributions::{Normal, Sample};


pub struct God {
    pub seed: u32,
}


impl God {
    pub fn new(seed: u32) -> God {
        God {
            seed: seed
        }
    }
}
