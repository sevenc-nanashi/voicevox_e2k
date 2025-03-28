#[test]
fn test_c2k() {
    let src = "constants";

    let c2k = e2k::C2k::new(32, Default::default());
    let dst = c2k.infer(src);
    dbg!(dst);
}

#[test]
fn test_c2k_empty() {
    let src = "";

    let c2k = e2k::C2k::new(32, Default::default());
    let dst = c2k.infer(src);
    assert_eq!(dst, "");
}
