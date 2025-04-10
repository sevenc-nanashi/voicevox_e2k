class InferenceNotFinishedError(Exception):
    """
    推論が終了しなかった場合に発生するエラー。

    Attributes
    ----------
    incomplete_output : str
        不完全な出力。
    """

    incomplete_output: str

    def __init__(self, incomplete_output: str):
        super().__init__(f"Inference not finished: {incomplete_output}")
        self.incomplete_output = incomplete_output
