extern crate ev3dev_lang_rust;

use std::io::{self, Read, Write};
use std::net::TcpStream;


use ev3dev_lang_rust::motors::{MediumMotor, MotorPort, LargeMotor};
use ev3dev_lang_rust::sensors::UltrasonicSensor;
use ev3dev_lang_rust::Ev3Result;


const FOV: f32 = 70.;
const SPEED: i32 = 50;

fn main() -> Ev3Result<()> {
    let mut stream = TcpStream::connect("192.168.43.173:6969")?;
    stream.set_nonblocking(true);


    let ultrasonicsensor = UltrasonicSensor::find()?;

    let radar_motor = MediumMotor::get(MotorPort::OutB)?;

    let l_motor = LargeMotor::get(MotorPort::OutA)?;
    let r_motor = LargeMotor::get(MotorPort::OutD)?;
    
    radar_motor.reset()?;

    radar_motor.run_direct()?;

    r_motor.run_direct()?;

    l_motor.run_direct()?;

    radar_motor.set_duty_cycle_sp(SPEED)?;

   
    let mut steer_r: f32 = 0.0;
    let mut steer_l: f32 = 0.0;

 

    loop { 
        let mut buf = [0; 128];
        match stream.read(&mut buf) {
            Ok(bytes_read) => {
                let response = String::from_utf8_lossy(&buf[..bytes_read]);
                if response == "quit" {
                    break;
                }
                let values: Vec<&str> = response.split_whitespace().collect();

                steer_r = values.get(0)
                    .and_then(|v| v.trim().parse().ok())
                    .unwrap_or_else(|| 0.0);

                steer_l = values.get(1)
                    .and_then(|v| v.trim().parse().ok())
                    .unwrap_or_else(|| 0.0);          
            }
            Err(ref e) if e.kind() == io::ErrorKind::WouldBlock => {
            }
            Err(e) => {
                println!("{}", e);
            }
        }
        
        let distance = ultrasonicsensor.get_distance().unwrap();
        let position: f32 = radar_motor.get_position()? as f32;

        
        
        stream.write_all((" ".to_owned() + &position.to_string().as_str() + " " + &distance.to_string()).as_bytes())?; 

        r_motor.set_duty_cycle_sp((steer_r*100f32) as i32);
        l_motor.set_duty_cycle_sp((steer_l*100f32) as i32);

        
        
        if position >= FOV {
            radar_motor.set_duty_cycle_sp(-SPEED)?;
        } else if position <= -FOV {
            radar_motor.set_duty_cycle_sp(SPEED)?;
        }

    }

    radar_motor.reset()?;

    Ok(())
}
