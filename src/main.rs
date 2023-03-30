extern crate ev3dev_lang_rust;

use ev3dev_lang_rust::Ev3Result;
use ev3dev_lang_rust::motors::{LargeMotor, MotorPort, MediumMotor};
use ev3dev_lang_rust::sensors::UltrasonicSensor;
use ev3dev_lang_rust::sound;

use console_engine::pixel;
use console_engine::Color;
use console_engine::KeyCode;

const FOV: f32 = 70f32;

const speed: i32 = 30i32;

fn main() -> Ev3Result<()>{
    let mut engine = console_engine::ConsoleEngine::init(44, 21, 30).unwrap();
     
    let ultrasonicsensor = UltrasonicSensor::find()?;

    let radar_motor = MediumMotor::get(MotorPort::OutB)?;

    sound::speak("RADA!")?.wait()?;
    
    radar_motor.reset();

    radar_motor.run_direct()?;

    radar_motor.set_duty_cycle_sp(speed)?;

    let mut distance: i32 = 0;

    let mut height: f32 = 0f32;
    

    let mut x: i32 = 0;
    loop {
        distance = ultrasonicsensor.get_distance().unwrap();
        engine.wait_frame(); 
        //engine.clear_screen();     
                
        let position: f32 = radar_motor.get_position()? as f32;

        height = 21f32 - (distance as f32 / (2550f32 / 21f32));

        x = ((position / FOV/ 2f32 + 0.5f32) * 44f32) as i32;
        
        engine.line(x, 0, x, 21, pixel::pxl_fg('0', Color::White));
        engine.line(x, ((21f32-height)/2f32) as i32, x, (21f32-((21f32-height)/2f32)) as i32, pixel::pxl_fg('0', Color::Black));
        
        if engine.is_key_pressed(KeyCode::Char('q')) { 
            radar_motor.set_duty_cycle_sp(0)?;
            break; 
        }

        if position >= FOV {
            radar_motor.set_duty_cycle_sp(-speed)?;
        } else if position <= -FOV {
            radar_motor.set_duty_cycle_sp(speed)?;
        }

    
        engine.draw(); 

    }

    Ok(())
}
