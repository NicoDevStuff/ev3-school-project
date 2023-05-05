use std::io::{self, Read};
use std::net::TcpStream;
use std::time::Duration;

fn main() -> io::Result<()> {
    let mut stream = TcpStream::connect("127.0.0.1:6969")?;
    stream.set_nonblocking(true);

    loop {
        let mut buf = [0; 128];
        match stream.read(&mut buf) {
            Ok(bytes_read) => {
                let response = String::from_utf8_lossy(&buf[..bytes_read]);
                if response == "quit" {
                    break;
                }
                println!("Received data: {}", response);
            }
            Err(ref e) if e.kind() == io::ErrorKind::WouldBlock => {
            }
            Err(e) => {
                return Err(e);
            }
        }
        // println!("lol");
    }

    Ok(())
}
