import os
import docx
import time
import random
import re  # For regular expressions (improved word splitting)

# ... (Document Generation and Text Extraction functions remain the same) ...

# --- Indexing (Improved for phrase search) ---
def build_index(extracted_dir):
    index = {}
    for filename in os.listdir(extracted_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(extracted_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read().lower()

                    # Improved word splitting with regex (handles punctuation better)
                    words = re.findall(r'\b\w+\b', text)  # \b for word boundaries

                    for i, word in enumerate(words):
                        if word:
                            # Index individual words
                            if word not in index:
                                index[word] = [filename]
                            else:
                                index[word].append(filename)

                            # Index phrases (n-grams) - adjust n for phrase length
                            n = 2  # Search for phrases up to 2 words long
                            for j in range(1, n):
                                if i + j < len(words):
                                    phrase = " ".join(words[i:i + j + 1])
                                    if phrase not in index:
                                        index[phrase] = [filename]
                                    else:
                                        index[phrase].append(filename)

            except Exception as e:
                print(f"Error reading extracted text file {filepath}: {e}")
    return index

# --- Searching (Handles phrases) ---
def search(index, query):
    query = query.lower() # Convert query to lowercase once

    results = {}
    search_terms = re.findall(r'"([^"]*)"|\b\w+\b', query) # Find phrases in quotes or individual words

    for term in search_terms:
        if term in index:
            for doc_id in index[term]:
                if doc_id not in results:
                    results[doc_id] = 0
                results[doc_id] += 1

    sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
    return sorted_results


# ... (Main execution remains the same) ...
