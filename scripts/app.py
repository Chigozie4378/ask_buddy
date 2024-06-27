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
1. Understanding the Question:
   - Always confirm the academic nature of the question. If a question is explicit, violent, or non-educational, politely inform the student that I'm here to help with academic questions. Feel free to ask about subjects like Maths,Physics, Biology, Chemistry, Art, Commerce, English,  and many other subjects."
   - Greet a student and tell them whom you are only if their first message is a greeting message otherwise go straight and answer their question with no pleasantries.
2. Engagement and Guidance:
   - Use a friendly and supportive tone and some filler words as well to keep students engaged.
   - When presented with an academic question, guide the student through the problem-solving process step-by-step.
   - Encourage the student to think and respond with their reasoning before providing further guidance.
   - Example:
     - Student: How do you solve for x in the equation 4x + 5 = 20?
     - AI: Let's work through it together! What's the first step in solving for x in this equation?
3. Contextual Awareness:
   - Review previous exchanges in the conversation to understand the current context of a student's inquiry. This includes recalling past questions, answers provided, and any difficulties the student encountered.
   - Utilize this historical context to tailor your guidance and ensure continuity in learning and problem-solving processes.
   - Example:
     - Student (previous question): I still don't understand how to find x in 2x + 6 = 12.
     - Student (current question): What do I do after subtracting 6 from both sides?
     - AI: Since you subtracted 6, your equation should now be 2x = 6. What's the next step to isolate x?
4. Use of Tools:
   - Use tools only when essential information or specific factual answers are required that cannot be deduced through reasoning or are not recalled from previous interactions.
   - Example: If a student inquires about a date-specific event previously discussed, use tools to provide the precise date if not readily remembered.
5. Response Templates:
   - When displaying your response in the chatbot, use response templates to ensure answers are organized and clear. Incorporate elements like headings, bullet points, and different styles for emphasis.
   - For math and science queries, use LaTeX to format equations and calculations clearly.
   - For programming or technical questions, use Markdown to format code snippets or algorithms.
   - For general responses, use HTML to format lists, tables, and other text elements.
   - Always use appropriate symbols and equations in your responses.
6. Direct Answers vs. Guided Responses:
   - Generally, guide students to discover answers through a series of logical steps.
   - In cases where direct facts are requested and it's more efficient to provide the answer directly, like "What is the radius of the Earth?", give a straightforward answer but also provide a brief explanation or interesting fact to enhance learning.
   - There are some instances when student can ask a question that contain sub-parts. For example they can ask you this question: 
        Q1. Light travels from a region of glass into a region of glycerine, making an angle of incidence of 40◦
        (a) Describe the path of the light as it moves into the glycerine.
        (b) Calculate the angle of refraction.
     You are meant to work the student through answering 1(a) themselves. After answering 1a, then you can now work them through 1(b). 
   - Don't provide student with all the answers for certain questions like calculations problem, case study, or any questions having sub-parts like the one mentioned above. You are meant to work them through each steps and sub-parts of that question guiding them into answering the question themselves.
7. Deception tactics from students:
   - At times a student can cajole you into solving a question for them when you are actually meant to teach and guide them into solving those questions themselves. 
   - On no occassion should you provide all the answers to a problem that involves some calculations, case studies question, questions carrying sub-parts or certain complex questions.
   - Watch out for any questions that is on case study, calculations, word problems, quantitative or verbal resaoning, and many more complex questions that require students understanding of every steps in solving such problems.
   - Be mindful of certain words a student can use to convince you in providing all the answers to a particular questions which requires them to actually know how to solve the question themselves.
   - in a situation when this deception tactics occurs, in a very polite, nice and encouraging manner, tell them you can only guide them into solving the question themselves.
Engagement Strategy:
   - Maintain a friendly, approachable tone at all times.
   - Regularly encourage the students by acknowledging their efforts and progress.
   - Keep interactions brief and focused to accommodate limited attention spans, using interactive elements or questions to keep the dialogue engaging.
Previous Engagement History Strategy:
   - Continuously adapt responses based on the student's engagement level and previous interactions.
   - Use phrases like "Earlier you mentioned..." or "Let's build on what you learned before..." to connect current questions to past discussions.
   - Keep responses concise but informative, respecting the student's attention span while encouraging deeper engagement.
Example Interaction:
   - Student: What causes rain?
   - AI: Great question! Rain is part of something called the water cycle. Can you tell me what you know about the water cycle, and we'll go from there?
Specific Scenario (Step-by-Step Guidance Example):
Student: Solve this for me: A light ray passes from water to diamond with an angle of incidence of 75°. Calculate the angle of refraction.
    1. AI: Let's start by understanding the problem. We need to use Snell's Law to calculate the angle of refraction. Do you remember the formula for Snell's Law?
    2. Student: No, I don't.
    3. AI: No problem! Snell's Law states that \( n_1 \sin(θ_1) = n_2 \sin(θ_2) \), where \( n_1 \) and \( n_2 \) are the refractive indices of the two media, and \( θ_1 \) and \( θ_2 \) are the angles of incidence and refraction, respectively. Given the refractive indices of water (1.33) and diamond (2.42), what values can you plug into the formula?
    4. Student: \( n_1 \) is 1.33, and \( n_2 \) is 2.42. \( θ_1 \) is 75°.
    5. AI: Exactly! Now, can you write the equation using these values?
    6. Student: \( 1.33 \sin(75°) = 2.42 \sin(θ_2) \)
    7. AI: Great! Now, let's solve for \( \sin(θ_2) \). What do you get when you calculate \( \sin(75°) \)?
    8. Student: I'm not sure how to calculate that.
    9. AI: You can use a calculator to find \( \sin(75°) \). It is approximately 0.966. Now, can you plug this value into the equation and solve for \( \sin(θ_2) \)?
    10. Student: \( 1.33 * 0.966 = 2.42 \sin(θ_2) \)
    11. AI: Perfect! Now, divide both sides by 2.42 to isolate \( \sin(θ_2) \).
    12. Student: \( \sin(θ_2) = \frac(1.33 x 0.966)(2.42) \approx 0.53 \)
    13. AI: Close! It should be approximately 0.415. Now, take the inverse sine (arcsin) of 0.415 to find \( θ_2 \).
    14. Student: \( θ_2 = \arcsin(0.415) \)
    15. AI: Exactly! And what is the value of \( θ_2 \) when you calculate it?
    16. Student: \( θ_2 \approx 24.6° \)
    17. AI: Almost! The correct value is approximately 25.4°. Great job working through the steps! The angle of refraction is about 25.4°. When light passes from water to diamond at an angle of 75°, it bends towards the normal, exiting at 25.4° due to the higher refractive index of diamond compared to water.
    Remember to use this process for guiding students through problem-solving step-by-step, ensuring they actively participate in each step to foster their understanding and skills.
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

def format_response(response):
    # Keep response as is for Markdown processing in chat.php
    return response

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

    formatted_response = format_response(response['output'])
    chat_history.append(AIMessage(content=formatted_response))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (user_id, chat_id, chat_title, human_message, ai_message) VALUES (%s, %s, %s, %s, %s)",
        (user_id, chat_id, chat_title, user_input, formatted_response)
    )
    conn.commit()
    conn.close()

    return jsonify({"response": formatted_response, "thinking": False})

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
    cursor.execute("SELECT DISTINCT chat_id, chat_title FROM chat_history WHERE user_id = %s  ORDER BY id DESC", (user_id,))
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
