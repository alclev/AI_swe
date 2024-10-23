import tiktoken

class Tokenizer:
    def __init__(self, file_dict):
        self.file_dict = file_dict

    def tokenize_files(self):
        tokenizer = tiktoken.get_encoding('cl100k_base')
        tokenized_files = {}
        for filename, content in self.file_dict.items():
            tokens = tokenizer.encode(content)
            tokenized_files[filename] = tokens
        return tokenized_files
