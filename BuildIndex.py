
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

def create_index(indexdir, files_to_index):
    # Define the schema for the index
    schema = Schema(path=ID(stored=True), content=TEXT)

    # Create the index directory if it doesn't exist
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)

    # Create the index
    ix = create_in(indexdir, schema)

    # Add documents to the index
    writer = ix.writer()
    for filepath in files_to_index:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            writer.add_document(path=filepath, content=content)
    writer.commit()

    return ix

def search_index(indexdir, query_str):
    # Open the index
    ix = open_dir(indexdir)

    # Create a query parser
    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(query_str)

    # Search the index
    with ix.searcher() as s:
        results = s.search(q)
        for hit in results:
            print(hit["path"], hit.score)  # Print the path and score of each hit

if __name__ == "__main__":
    indexdir = "indexdir"
    files_to_index = ["file1.txt", "file2.txt", "file3.txt"]  # Replace with your file paths

    # Create the index
    ix = create_index(indexdir, files_to_index)

    # Search the index
    search_index(indexdir, "example query")
