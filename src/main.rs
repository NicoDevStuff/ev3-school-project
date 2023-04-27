extern crate ev3dev_lang_rust;

use ev3dev_lang_rust::motors::{MediumMotor, MotorPort};
use ev3dev_lang_rust::sensors::UltrasonicSensor;
use ev3dev_lang_rust::sound;
use ev3dev_lang_rust::Ev3Result;

use console_engine::pixel;
use console_engine::Color;
use console_engine::KeyCode;

const FOV: f32 = 70f32;

const SPEED: i32 = 30i32;

fn main() -> Ev3Result<()> {
    let mut engine = console_engine::ConsoleEngine::init(44, 21, 30).unwrap();

    let ultrasonicsensor = UltrasonicSensor::find()?;

    let radar_motor = MediumMotor::get(MotorPort::OutB)?;

    sound::speak("öööufuihfeufewhufewhjfewfewhufewfiuhw")?.wait()?;
    
    radar_motor.reset()?;

    radar_motor.run_direct()?;

    radar_motor.set_duty_cycle_sp(SPEED)?;

    let mut distance: i32;
    let mut height: f32;
    let mut x: i32;

    let mut prevx: i32 = 0;

    loop {
        distance = ultrasonicsensor.get_distance().unwrap();
        engine.wait_frame();

        let position: f32 = radar_motor.get_position()? as f32;

        height = 21f32 * (1f32 - distance as f32 / 255f32);

        x = ((position / FOV / 2f32 + 0.5f32) * 44f32) as i32;

        if engine.is_key_pressed(KeyCode::Char('q')) {
            radar_motor.set_duty_cycle_sp(0)?;
            break;
        }
        engine.fill_rect(prevx, 0, x, 21, pixel::pxl_fg(' ', Color::White));
        engine.fill_rect(
            prevx,
            ((21f32 - height) / 2f32) as i32,
            x,
            (21f32 - ((21f32 - height) / 2f32)) as i32,
            pixel::pxl_fg('█', Color::Black),
        );

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
