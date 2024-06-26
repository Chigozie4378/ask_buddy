import pickle
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')
index_file_path = 'saved_index.pkl'
with open(index_file_path, 'rb') as f:
        index = pickle.load(f)

# query_engine = index.as_query_engine()
query_engine = index.as_retriever()
# response = query_engine.query("what is argon")
response = query_engine.retrieve("what is argon")
# Print only the text content from each TextNode in the response
for result in response:
    print(result.node.text) 