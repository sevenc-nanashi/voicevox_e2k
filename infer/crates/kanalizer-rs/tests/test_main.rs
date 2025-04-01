#[test]
fn test_kana() {
    let src = "kanalizer";

    let kana = kanalizer::Kanalizer::new();
    let dst = kana.infer(src);
    assert_eq!(dst, "カナライザー");
}

#[test]
fn test_kana_empty() {
    let src = "";

    let kana = kanalizer::Kanalizer::new();
    let dst = kana.infer(src);
    assert_eq!(dst, "");
}

#[test]
fn test_kana_long() {
    let src = "pneumonoultramicroscopicsilicovolcanoconiosis";

    let unlimited_kana = kanalizer::Kanalizer::new();
    let limited_kana = kanalizer::Kanalizer::new().with_max_length(10);
    let unlimited_dst = unlimited_kana.infer(src);
    let limited_dst = limited_kana.infer(src);
    assert_ne!(unlimited_dst, limited_dst);
    assert_eq!(limited_dst.chars().count(), 10);
}
