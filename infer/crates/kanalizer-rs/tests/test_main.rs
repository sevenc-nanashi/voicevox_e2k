#[test]
fn test_kanalizer() {
    let src = "kanalizer";

    let kanalizer = kanalizer::Kanalizer::new();
    let dst = kanalizer.convert(src);
    assert_eq!(dst, "カナライザー");
}

#[test]
fn test_kanalizer_empty() {
    let src = "";

    let kanalizer = kanalizer::Kanalizer::new();
    let dst = kanalizer.convert(src);
    assert_eq!(dst, "");
}

#[test]
fn test_kanalizer_long() {
    let src = "pneumonoultramicroscopicsilicovolcanoconiosis";

    let unlimited_kanalizer = kanalizer::Kanalizer::new();
    let limited_kanalizer = kanalizer::Kanalizer::new().with_max_length(10);
    let unlimited_dst = unlimited_kanalizer.convert(src);
    let limited_dst = limited_kanalizer.convert(src);
    assert_ne!(unlimited_dst, limited_dst);
    assert_eq!(limited_dst.chars().count(), 10);
}
