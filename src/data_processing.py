import os
import re
import json
from typing import List
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize  # Ensure NLTK's punkt tokenizer is available


def clean_text(text: str) -> str:
    """
    Cleans the input text by:
      - Removing HTML tags.
      - Removing newline and carriage-return characters.
      - Stripping leading/trailing whitespace.
      - Collapsing multiple whitespace characters into a single space.
    
    Args:
        text (str): The raw text from the document.
    
    Returns:
        str: The cleaned text.
    """
    # Remove HTML tags using BeautifulSoup
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    
    # Remove newline/carriage-return characters and replace them with a space.
    text = text.replace('\"', " ").replace("\r", " ")
    
    # Remove leading/trailing whitespace and collapse extra spaces.
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    
    return text


def segment_text(text: str, chunk_size: int = 200, overlap: int = 20) -> List[str]:
    """
    Segments a text into overlapping chunks using sentence tokenization.

    The text is tokenized into sentences using NLTK, and then these sentences are grouped 
    together until the total word count roughly reaches the specified chunk_size. Consecutive
    chunks will share an overlap of sentences (based on a target word count) so that context
    is preserved across chunks.

    Args:
        text (str): Cleaned text.
        chunk_size (int, optional): Approximate number of words per chunk. Defaults to 200.
        overlap (int, optional): Number of words to overlap between consecutive chunks.
            Defaults to 20.
    
    Returns:
        List[str]: A list containing the text chunks.
    """
    sentences = sent_tokenize(text)
    chunks = []
    start = 0

    while start < len(sentences):
        current_chunk = []
        word_count = 0
        end = start

        # Group sentences until the target word count is met or exceeded.
        while end < len(sentences) and word_count < chunk_size:
            sentence = sentences[end]
            current_chunk.append(sentence)
            word_count += len(sentence.split())
            end += 1
        
        chunks.append(" ".join(current_chunk))
        
        # Determine new start index by overlapping sentences from the current chunk:
        overlap_word_count = 0
        new_start = end  # default if not enough sentences for overlap
        # Iterate backwards through the sentences in the current chunk to accumulate overlap words.
        for i in range(end - 1, start - 1, -1):
            overlap_word_count += len(sentences[i].split())
            if overlap_word_count >= overlap:
                new_start = i
                break
        
        # Prevent the new start from falling behind the current start.
        start = new_start if new_start > start else end

    return chunks


def process_documents(input_dir: str, output_path: str, chunk_size: int = 200, overlap: int = 20):
    """
    Processes all text documents in the specified input directory:
      - Reads and cleans the text.
      - Segments the text into overlapping chunks.
      - Saves the processed data as JSON.
    
    Args:
        input_dir (str): Directory path containing .txt files.
        output_path (str): Path to the output JSON file.
        chunk_size (int, optional): Approximate number of words per chunk for segmentation. Defaults to 200.
        overlap (int, optional): Number of overlapping words between chunks. Defaults to 20.
    """
    processed_docs = []
    
    # Iterate over each file in the directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                raw_text = file.read()
            
            cleaned_text = clean_text(raw_text)
            chunks = segment_text(cleaned_text, chunk_size=chunk_size, overlap=overlap)
            
            doc_entry = {
                "document_id": filename,
                "chunks": chunks
            }
            processed_docs.append(doc_entry)
            print(f"Processed '{filename}' into {len(chunks)} chunks.")
    
    # Write the processed documents to a JSON file.
    with open(output_path, "w", encoding="utf-8") as out_file:
        json.dump(processed_docs, out_file, ensure_ascii=False, indent=2)
    
    print(f"All documents have been processed and saved to '{output_path}'.")


if __name__ == "__main__":
    # Define the directory containing the document files and the output JSON file path.
    DATA_DIR = "data/dirty"
    OUTPUT_JSON = "data/clean/processed_data.json"
    
    # You can adjust the chunk_size and overlap values if needed.
    process_documents(input_dir=DATA_DIR, output_path=OUTPUT_JSON, chunk_size=200, overlap=20)
