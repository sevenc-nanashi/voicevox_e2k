use criterion::{criterion_group, criterion_main, Criterion};

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("c2k", |b| {
        let c2k = e2k::C2k::new(32);
        b.iter(|| std::hint::black_box(c2k.infer("constants")))
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
