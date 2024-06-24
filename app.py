from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import uuid
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.agent_toolkits.load_tools import load_tools
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings
import os

# Load environment variables
load_dotenv()

from langchain.agents import AgentExecutor
from langchain_cohere.chat_models import ChatCohere
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders.text import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.chains.history_aware_retriever import create_history_aware_retriever

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

# Initialize components outside of request handlers to avoid re-running
internet_search = TavilySearchResults()

llm = ChatCohere()
loader = TextLoader('text.txt', encoding='utf8')
text_documents = loader.load()
embeddings = CohereEmbeddings()
vector_store = FAISS.from_documents(text_documents, embeddings)
retrieval = vector_store.as_retriever(search_kwargs={'k': 3})

retreiver_tool = create_retriever_tool(
    retrieval,
    "christian_retriever",
    "Use this tool to look up information if the context of user question is about christianity"
)

prompt = ChatPromptTemplate.from_template("""
You will be my assistant and I will be asking you a couple of questions.
You can refer to our previous conversation for reference and you can also look up on the internet for any
question you don't have access to.
Use the following context if needed: {context}
Question: {question}
chat_history: {chat_history}
""")

agent = create_cohere_react_agent(
    llm=llm,
    tools=[internet_search, retreiver_tool],
    prompt=prompt,
)

agent_executor = AgentExecutor(agent=agent, tools=[internet_search, retreiver_tool], verbose=True)

# Global chat history and session info to maintain state across requests
chat_history = []
session_info = {}

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='chigzeai'
    )
    return conn

def generate_chat_id():
    return str(uuid.uuid4())

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    global session_info
    user_input = request.json.get('message')

    if not chat_history:
        session_info['chat_id'] = generate_chat_id()
        session_info['chat_title'] = f"{user_input[:50]}...".capitalize()

    chat_id = session_info['chat_id']
    chat_title = session_info['chat_title']

    retrieved_docs = retrieval.get_relevant_documents(user_input)
    formatted_docs = format_docs(retrieved_docs)

    chat_history.append(HumanMessage(content=user_input))

    response = agent_executor.invoke({
        "question": user_input,
        "chat_history": chat_history,
        "context": formatted_docs
    })

    chat_history.append(AIMessage(content=response['output']))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (user_id, chat_id, chat_title, human_message, ai_message) VALUES (%s, %s, %s, %s, %s)",
        ("user_1", chat_id, chat_title, user_input, response['output'])
    )
    conn.commit()
    conn.close()

    return jsonify({"response": response['output'], "thinking": False})

@app.route('/clear', methods=['POST'])
def clear():
    global chat_history
    global session_info
    chat_history = []
    session_info = {}
    return jsonify({"status": "success"})

@app.route('/conversations', methods=['GET'])
def get_conversations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT chat_id, chat_title FROM chat_history WHERE user_id = %s", ("user_1",))
    conversations = cursor.fetchall()
    conn.close()
    return jsonify(conversations)

@app.route('/conversation/<chat_id>', methods=['GET'])
def get_conversation(chat_id):
    global chat_history
    global session_info
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT human_message, ai_message, chat_title FROM chat_history WHERE chat_id = %s", (chat_id,))
    chat_history = []
    full_chat_history = []
    chat_title = None
    for human_message, ai_message, chat_title in cursor.fetchall():
        if human_message:
            chat_history.append(HumanMessage(content=human_message))
            full_chat_history.append({"sender": "User", "content": human_message})
        if ai_message:
            chat_history.append(AIMessage(content=ai_message))
            full_chat_history.append({"sender": "Bot", "content": ai_message})
    conn.close()
    session_info['chat_id'] = chat_id
    session_info['chat_title'] = chat_title
    return jsonify({"status": "success", "chat_history": full_chat_history})

@app.route('/delete_conversation/<chat_id>', methods=['DELETE'])
def delete_conversation(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE chat_id = %s", (chat_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

