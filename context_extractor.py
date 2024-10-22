# /Users/alexclevenger/swe/context_extractor.py

import os
import logging
import tiktoken

logger = logging.getLogger(__name__)

def extract_context(directory):
    """
    Walk through the directory and capture the hierarchy of files along with their
    corresponding content. The file content is also tokenized using tiktoken.

    :param directory: The root directory to start walking through
    :return: A dictionary with file paths as keys and tokenized content as values
    """
    file_hierarchy = {}
    encoding = tiktoken.get_encoding("gpt2")  # Assuming GPT-2 tokenizer; change model if needed.

    logger.info("Starting context extraction from directory: %s", directory)

    # Walk through the directory, recursively
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            try:
                # Only process readable files (skip binary files like images)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    logger.info("Processing file: %s", file_path)

                    # Tokenize the file content
                    tokens = encoding.encode(content)
                    
                    # Store the tokenized content in the dictionary
                    file_hierarchy[file_path] = {
                        "content": content,
                        "tokens": tokens,
                        "token_count": len(tokens)
                    }

            except Exception as e:
                logger.error("Error reading or tokenizing file %s: %s", file_path, e)

    logger.info("Completed context extraction")
    return file_hierarchy

