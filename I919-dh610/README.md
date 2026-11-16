# I919-dh610: the octo-double dot-product benchmark (multidouble's ODotAcc against integer-limb and Ozaki prototypes) on dh610's AVX2

Machine dh610 (Fedora 45, i7-12700, 20 threads, AVX2), issue https://github.com/nmoinvaz/choptuik-large-d/issues/919.
Code: the standalone crate the coordinator wrote to `~/scratch-dotbench` (`Cargo.toml` 165 bytes, `src/main.rs` 9654,
`src/ozaki.rs` 3975; multidouble 4.7.0 from crates.io), not a repository; it is read before the run and unchanged.
Command: `cd ~/scratch-dotbench && RUSTFLAGS="-C target-cpu=native" cargo build --release && taskset -c <core>
./target/release/dotbench | tee dotbench.log`, single-threaded at normal priority beside the #842 and #903 chains
(`build.log`, `dotbench.log`, `cpu_busy.log` with the busy percent of the core and its hyper-thread sibling during the run).
