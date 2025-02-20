import os
import docx
import time
import random
import re
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

# ... (Document Generation and Text Extraction functions remain the same) ...

# --- Indexing with Whoosh ---
def build_whoosh_index(extracted_dir, index_dir):
    schema = Schema(path=ID(unique=True, stored=True), content=TEXT())  # Add 'stored=True' for path
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
        ix = create_in(index_dir, schema)
    else:
        ix = open_dir(index_dir)

    writer = ix.writer()
    for filename in os.listdir(extracted_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(extracted_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()  # No need to lowercase here, Whoosh does it
                    writer.add_document(path=filepath, content=text)
            except Exception as e:
                print(f"Error reading extracted text file {filepath}: {e}")
    writer.commit()
    return ix


# --- Searching with Whoosh ---
def whoosh_search(ix, query):
    with ix.searcher() as searcher:
        parser = QueryParser("content", ix.schema)
        try:
            q = parser.parse(query)
            results = searcher.search(q)
            return results
        except Exception as e: # Catch parsing errors
            print(f"Error parsing search query: {e}")
            return None



# --- Main execution ---
if __name__ == "__main__":
    # ... (Directory setup and document generation remain the same) ...

    index_dir = "whoosh_index"  # Directory for Whoosh index

    # 2. Extract Text (same as before)
    # ...

    # 3. Build Whoosh Index
    start_time = time.time()
    ix = build_whoosh_index(extracted_dir, index_dir)
    end_time = time.time()
    print(f"Whoosh index building time: {end_time - start_time:.2f} seconds")

    # 4. Search with Whoosh
    while True:
        query = input("Enter your search query (or type 'exit'): ")
        if query.lower() == "exit":
            break

        start_time = time.time()
        results = whoosh_search(ix, query)
        end_time = time.time()
        print(f"Whoosh search time: {end_time - start_time:.2f} seconds")

        if results:
            print(f"Found {len(results)} results:")
            for hit in results:
                print(f"- {hit['path']} (Score: {hit.score})")  # Access stored path
        else:
            print("No results found.")
