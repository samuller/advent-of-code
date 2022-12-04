# Dev

Compile and lint:
```shell
time cargo run
cargo clippy
```

Generate executable:
```shell
time cargo run --release
time ./target/release/aoc2022

# Use dynamic linking for a smaller executable (e.g. 4Mb -> 40kb).
# See: https://stackoverflow.com/questions/29008127/why-are-rust-executables-so-huge
time cargo rustc --release -- -C prefer-dynamic
# strip target/release/aoc2022
```
