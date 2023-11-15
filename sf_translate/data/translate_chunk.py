class TranslateChunk:
    def __init__(self, chunk, target_lang, source_lang=None):
        self.target_lang = target_lang
        self.source_lang = source_lang
        self.chunk = chunk
