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

    pub fn gaussian<T: FromPrimitive>() -> T {
        FromPrimitive::from_f64(
            Normal::new(2.0, 3.5).sample(&mut rand::thread_rng())
        ).expect("Cannot convert to given type")
    }
}
