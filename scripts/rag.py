import os 
import pickle
from dotenv import load_dotenv
load_dotenv()
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.cohere import Cohere
from llama_index.embeddings.cohere import CohereEmbedding
# from llama_index.core.response.notebook_utils import display_source_node

# Check if the index file already exists
index_file_path = 'saved_index.pkl'

if os.path.exists(index_file_path):
    # Load the index from a file if it already exists
    with open(index_file_path, 'rb') as f:
        index = pickle.load(f)
else:
    # Create the index if it does not exist
    documents = SimpleDirectoryReader("data").load_data()
    llm = Cohere(model="command-nightly", api_key='iu2IqPJQJ0RFMD06V3IYzqK5ppEgjmSpb8t2dduY')
    embed_model = CohereEmbedding(
        api_key='iu2IqPJQJ0RFMD06V3IYzqK5ppEgjmSpb8t2dduY',
        model_name="embed-english-v3.0",
        input_type="search_document",
        embedding_type="int8",
    )
    index = VectorStoreIndex.from_documents(
        documents=documents, embed_model=embed_model
    )
    # Save the newly created index to a file
    with open(index_file_path, 'wb') as f:
        pickle.dump(index, f)

# Use the index to create a query engine
query_engine = index.as_query_engine()

# Perform a query
response = query_engine.query("What is motion")
print(response)