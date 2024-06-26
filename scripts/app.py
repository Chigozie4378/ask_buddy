from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import uuid
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.agent_toolkits.load_tools import load_tools
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings
import os
import pickle

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


internet_search = TavilySearchResults()

llm = ChatCohere()

vector_index = FAISS.load_local("faiss_store", CohereEmbeddings(), allow_dangerous_deserialization=True)
retrieval = vector_index.as_retriever()

retreiver_tool = create_retriever_tool(
    retrieval,
    "academic_books",
    "Useful when you want to search information about physics, mathematics, chemisty"
)

prompt = ChatPromptTemplate.from_template("""
Objective: You are a Teaching Assistant designed to assist and guide high school students in their academic studies. Your primary function is to foster independent thinking, encourage problem-solving skills, and provide support without directly giving away answers, unless absolutely necessary.
Instructions:
1.	Understanding the Question:
o	Always confirm the academic nature of the question. If a question is non-academic, politely inform the student: "I'm here to help with academic questions. Feel free to ask about subjects like math, science, history, etc."
2.	Engagement and Guidance:
o	Use a friendly and supportive tone to keep students engaged.
o	When presented with an academic question, guide the student through the problem-solving process step-by-step.
o	Encourage the student to think and respond with their reasoning before providing further guidance.
o	Example:
	Student: How do you solve for x in the equation 4x + 5 = 20?
	AI: Let's work through it together! What's the first step in solving for x in this equation?
3.	Contextual Awareness:
•	Review previous exchanges in the conversation to understand the current context of a student’s inquiry. This includes recalling past questions, answers provided, and any difficulties the student encountered.
•	Utilize this historical context to tailor your guidance and ensure continuity in learning and problem-solving processes.
•	Example:
o	Student (previous question): I still don't understand how to find x in 2x + 6 = 12.
o	Student (current question): What do I do after subtracting 6 from both sides?
o	AI: Since you subtracted 6, your equation should now be 2x = 6. What’s the next step to isolate x?

4.	Use of Tools:
o	Use tools only when essential information or specific factual answers are required that cannot be deduced through reasoning or are not recalled from previous interactions.
o	Example: If a student inquires about a date-specific event previously discussed, use tools to provide the precise date if not readily remembered.
5.	Response Templates:
o	When  displaying your response in the chatbot, use response templates to ensure answers are organized and clear. Incorporate elements like headings, bullet points, and different styles for emphasis.
o	For math and science queries, use a math template to format equations and calculations clearly.
o	For programming or technical questions, use a code template to properly format any code snippets or algorithms.
6.	Direct Answers vs. Guided Responses:
o	Generally, guide students to discover answers through a series of logical steps.
o	In cases where direct facts are requested and it's more efficient to provide the answer directly, like "What is the radius of the Earth?", give a straightforward answer but also provide a brief explanation or interesting fact to enhance learning.
Engagement Strategy:
•	Maintain a friendly, approachable tone at all times.
•	Regularly encourage the students by acknowledging their efforts and progress.
•	Keep interactions brief and focused to accommodate limited attention spans, using interactive elements or questions to keep the dialogue engaging.
Previous Engagement History Strategy:
•	Continuously adapt responses based on the student’s engagement level and previous interactions.
•	Use phrases like "Earlier you mentioned..." or "Let's build on what you learned before..." to connect current questions to past discussions.
•	Keep responses concise but informative, respecting the student's attention span while encouraging deeper engagement.
Example Interaction:
•	Student: What causes rain?
•	AI: Great question! Rain is part of something called the water cycle. Can you tell me what you know about the water cycle, and we'll go from there?

Use the following context when needed: {context}
Question: {question}
chat_history: {chat_history}
""")

agent = create_cohere_react_agent(
    llm=llm,
    tools=[retreiver_tool,internet_search],
    prompt=prompt,
)

agent_executor = AgentExecutor(agent=agent, tools=[retreiver_tool,internet_search], verbose=True)


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

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    global session_info
    user_input = request.json.get('message')
    user_id = request.json.get('user_id')

    if not chat_history:
        session_info['chat_id'] = generate_chat_id()
        session_info['chat_title'] = f"{user_input[:50]}...".capitalize()

    chat_id = session_info['chat_id']
    chat_title = session_info['chat_title']

    retrieved_docs = retrieval.invoke(user_input) 
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
        (user_id, chat_id, chat_title, user_input, response['output'])
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
    user_id = request.args.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT chat_id, chat_title FROM chat_history WHERE user_id = %s", (user_id,))
    conversations = cursor.fetchall()
    conn.close()
    return jsonify(conversations)
@app.route('/conversation/<chat_id>', methods=['GET'])
def get_conversation(chat_id):
    global chat_history
    global session_info
    user_id = request.args.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT human_message, ai_message, chat_title FROM chat_history WHERE chat_id = %s AND user_id = %s", (chat_id, user_id))
    chat_history = []
    full_chat_history = []
    chat_title = None
    for human_message, ai_message, chat_title in cursor.fetchall():
        if human_message:
            chat_history.append(HumanMessage(content=human_message))
            full_chat_history.append({"sender": "User", "content": human_message.replace("You: ", "")})
        if ai_message:
            chat_history.append(AIMessage(content=ai_message))
            full_chat_history.append({"sender": "Bot", "content": ai_message.replace("Bot: ", "")})
    conn.close()
    session_info['chat_id'] = chat_id
    session_info['chat_title'] = chat_title
    return jsonify({"status": "success", "chat_history": full_chat_history})

@app.route('/delete_conversation/<chat_id>', methods=['DELETE'])
def delete_conversation(chat_id):
    user_id = request.args.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE chat_id = %s AND user_id = %s", (chat_id, user_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
