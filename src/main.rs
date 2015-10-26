extern crate num;
extern crate rand;


mod universe;

// TODO
// Move world into universe and rename God into Universe

fn main() {
    let mut universe = universe::Universe::new([123; 4]);
    let mut body = universe.spawn_body();

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

    universe.spawn_population(6);
}
