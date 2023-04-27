extern crate ev3dev_lang_rust;

use ev3dev_lang_rust::motors::{MediumMotor, MotorPort, LargeMotor};
use ev3dev_lang_rust::sensors::UltrasonicSensor;
use ev3dev_lang_rust::sound;
use ev3dev_lang_rust::Ev3Result;

use console_engine::pixel;
use console_engine::Color;
use console_engine::KeyCode;

const FOV: f32 = 70f32;

const SPEED: i32 = 30i32;

fn main() -> Ev3Result<()> {
    let w = 134f32;

    let h = 30f32;

    let mut engine = console_engine::ConsoleEngine::init(w as u32, h as u32, 10).unwrap();

    let ultrasonicsensor = UltrasonicSensor::find()?;

    let radar_motor = MediumMotor::get(MotorPort::OutB)?;

    let l_motor = LargeMotor::get(MotorPort::OutA)?;
    let r_motor = LargeMotor::get(MotorPort::OutD)?;
    //sound::speak("öööufuihfeufewhufewhjfewfewhufewfiuhw")?.wait()?;
    
    radar_motor.reset()?;

    radar_motor.run_direct()?;

    r_motor.run_direct()?;

    l_motor.run_direct()?;

    radar_motor.set_duty_cycle_sp(SPEED)?;

    let mut distance: i32;
    let mut height: f32;
    let mut x: i32;

    let mut prevx: i32 = 0;

    let mut steer_r: f32 = 0.;
    let mut steer_l: f32 = 0.;
    
    loop {
        steer_r = 0f32;
        steer_l = 0f32;
        distance = ultrasonicsensor.get_distance().unwrap();
        engine.wait_frame();

        let position: f32 = radar_motor.get_position()? as f32;

        height = h * (1f32-(distance.clamp(0, 1000) as f32 / 1000f32));

        x = ((position / FOV / 2f32 + 0.5f32) * w) as i32;

        if engine.is_key_pressed(KeyCode::Char('q')) {
            radar_motor.set_duty_cycle_sp(0)?;
            break;
        }

        if engine.is_key_held(KeyCode::Up) {
             steer_r += 1f32;
             steer_l += 1f32; 
        }
        if engine.is_key_held(KeyCode::Right) {
            steer_l += 1f32;
            steer_r = 0f32;
        }

        if engine.is_key_held(KeyCode::Left) {
            steer_r += 1f32;
            steer_l = 0f32;
        }

        if engine.is_key_held(KeyCode::Down) {
             steer_r -= 1f32;
             steer_l -= 1f32; 
        }



        r_motor.set_duty_cycle_sp((steer_r*100f32) as i32);
        l_motor.set_duty_cycle_sp((steer_l*100f32) as i32);

        engine.fill_rect(prevx, 0, x, h as i32, pixel::pxl_fg(' ', Color::White));
        engine.fill_rect(
            prevx,
            ((h - height) / 2f32) as i32,
            x,
            (h - ((h - height) / 2f32)) as i32,
            pixel::pxl_fg('█', Color::White),
        );
        
        engine.print(0, 0, &distance.to_string());

        prevx = x;

        if position >= FOV {
            radar_motor.set_duty_cycle_sp(-SPEED)?;
        } else if position <= -FOV {
            radar_motor.set_duty_cycle_sp(SPEED)?;
        }

        engine.draw();
    }

    Ok(())
}
