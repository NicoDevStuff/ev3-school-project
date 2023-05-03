use std::io::{self, prelude::*, BufReader};
use std::net::TcpStream;

fn main() -> io::Result<()> {
    let mut stream = TcpStream::connect("127.0.0.1:6969")?;

    loop {
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        stream.write_all(input.as_bytes())?;

        let mut reader = BufReader::new(&stream);
        let mut buffer = String::new();
        reader.read_line(&mut buffer)?;
        print!("{}", buffer);
    }
}
