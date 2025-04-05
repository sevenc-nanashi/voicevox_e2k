use criterion::{Criterion, criterion_group, criterion_main};

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("Kanalizer", |b| {
        let kana = kanalizer::Kanalizer::new();
        b.iter(|| std::hint::black_box(kana.convert("kanalizer")))
    });
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
