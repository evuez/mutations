use num::FromPrimitive;
use rand::distributions::{Normal, Sample};


pub struct God {
    pub seed: [u32; 4],
}


impl God {
    pub fn new(seed: [u32; 4]) -> God {
        God {
            seed: seed
        }
    }
}
