use criterion::{Criterion, criterion_group, criterion_main};

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("Kanalizer", |b| {
        let kanalizer = kanalizer::Kanalizer::new();
        b.iter(|| std::hint::black_box(kanalizer.convert("kanalizer")))
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
