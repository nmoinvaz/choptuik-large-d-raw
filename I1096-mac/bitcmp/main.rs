//! hp's fastmul::mullow against multidouble's series::mullow on octo-double lanes, bit for bit, on random series
#[allow(dead_code)]
#[path = "/Users/nathan/Source/choptuik-fastmul/hp/src/fastmul.rs"]
mod fastmul;
use multidouble::native::{ODotAcc, OV};
use multidouble::od::OD;

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9e3779b97f4a7c15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xbf58476d1ce4e5b9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94d049bb133111eb);
        z ^ (z >> 31)
    }
    fn u(&mut self) -> f64 {
        (self.next() >> 11) as f64 * (1.0 / (1u64 << 53) as f64)
    }
}

fn series(r: &mut Rng, n: usize, slope: f64, wild: f64) -> Vec<OV> {
    (0..n)
        .map(|i| {
            let l: [OD; 8] = std::array::from_fn(|ln| {
                let e = -slope * i as f64 + ln as f64 + wild * (r.u() - 0.5);
                let mut x = [0.0f64; 8];
                x[0] = if r.next() & 1 == 0 { 1.0 } else { -1.0 } * (1.0 + r.u()) * e.exp2();
                for j in 1..8 {
                    x[j] = (r.u() - 0.5) * x[j - 1].abs() * (-52.0f64).exp2();
                }
                OD::new(x)
            });
            OV::from_lanes(&l)
        })
        .collect()
}

fn main() {
    let mut r = Rng(1);
    let mut cases = 0;
    let mut differ = 0;
    for &(n, sl, w) in &[(128usize, 0.7, 8.0), (251, 0.02, 4.0), (512, 0.3, 60.0), (1000, 1.5, 200.0), (2049, 0.01, 2.0), (300, 3.0, 400.0)] {
        for _ in 0..3 {
            let (a, b) = (series(&mut r, n, sl, w), series(&mut r, n, sl * 0.5, w));
            let mut a1 = vec![ODotAcc::zero(); n];
            let mut a2 = vec![ODotAcc::zero(); n];
            let s1 = fastmul::mullow(&a, &b, n, &fastmul::Cfg::default(), &mut a1);
            let s2 = multidouble::series::mullow(&a, &b, n, &multidouble::series::Cfg::default(), &mut a2);
            let bits = |v: &[ODotAcc]| -> Vec<u64> { v.iter().flat_map(|x| x.finish().c.iter().flat_map(|p| p.to_array().map(f64::to_bits)).collect::<Vec<_>>()).collect() };
            cases += 1;
            if bits(&a1) != bits(&a2) {
                differ += 1;
                println!("n {n} slope {sl}: DIFFER (blocks {:?} vs {:?}, pairs {} vs {})", s1.blocks, s2.blocks, s1.pairs, s2.pairs);
            }
        }
    }
    println!("hp fastmul vs multidouble series, octo-double: {cases} products, {differ} differ in any bit");
    std::process::exit(if differ == 0 { 0 } else { 1 });
}
