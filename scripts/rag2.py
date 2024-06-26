import os
import pickle
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# # Check if the index file already exists
# index_file_path = 'saved_index.pkl'

# if os.path.exists(index_file_path):
#     # Load the index from a file if it already exists
#     with open(index_file_path, 'rb') as f:
#         index = pickle.load(f)
# else:
#     documents = SimpleDirectoryReader("data").load_data() 
#     index = VectorStoreIndex.from_documents(documents,show_progress=True)
    
#     # Save the newly created index to a file
#     with open(index_file_path, 'wb') as f:
#         pickle.dump(index, f)

# Use the index to create a query engine
documents = SimpleDirectoryReader("data").load_data() 
index = VectorStoreIndex.from_documents(documents,show_progress=True)
index_file_path = 'saved_index.pkl'
# Save the newly created index to a file
with open(index_file_path, 'wb') as f:
    pickle.dump(index, f)


