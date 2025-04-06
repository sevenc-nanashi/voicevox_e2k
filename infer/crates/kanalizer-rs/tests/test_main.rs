#[test]
fn test_kanalizer() {
    let src = "kanalizer";

    let kanalizer = kanalizer::Kanalizer::new();
    let dst = kanalizer.convert(src, &Default::default());
    assert_eq!(dst, "カナライザー");
}

#[test]
fn test_kanalizer_empty() {
    let src = "";

    let kanalizer = kanalizer::Kanalizer::new();
    let dst = kanalizer.convert(src, &Default::default());
    assert_eq!(dst, "");
}

#[test]
fn test_kanalizer_long() {
    let src = "phosphoribosylaminoimidazolesuccinocarboxamide";

    let kanalizer = kanalizer::Kanalizer::new();
    let unlimited_dst = kanalizer.convert(
        src,
        &kanalizer::ConvertOptions {
            max_length: 32,
            ..Default::default()
        },
    );
    let limited_dst = kanalizer.convert(
        src,
        &kanalizer::ConvertOptions {
            max_length: 10,
            ..Default::default()
        },
    );
    assert_ne!(unlimited_dst, limited_dst);
    assert_eq!(limited_dst.chars().count(), 10);
}
