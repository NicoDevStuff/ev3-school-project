cargo build --release

scp ../target/armv5te-unknown-linux-musleabi/release/ev3dev-lang-rust-template robot@$1:/home/robot/Schoolproject/executable
