from langchain_openai import ChatOpenAI
from llama_index.core import ServiceContext
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
import openai

from flask import Flask, render_template, request
app = Flask(__name__)


openai.api_key = ""

api_key = ""

# Read pdf(s) here

documents = SimpleDirectoryReader("./content").load_data()

llm = ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo",
                 api_key=api_key, streaming=True)
service_context = ServiceContext.from_defaults(llm=llm, chunk_size=512)

index = VectorStoreIndex.from_documents(
    documents, service_context=service_context, show_progress=True)

starter_prompt = """
Provide health and wellness advice as a virtual doctor.
Engage users with accurate information on various health topics, 
including common illnesses, nutrition, mental health, diets, fitness, tips to cure any ailment and wellness practices.
Maintain a professional yet approachable demeanor, respecting user privacy and avoiding assumptions. 
Use concise, human-like responses to assist users in managing their health.
Focus on promoting a healthier lifestyle through helpful and positive guidance.

Additional conversation tips you must follow:
    
- Act professional, like a doctor who is treating a patient, always ask for more information and then make your deductions on the ailment the user is suffering through
- Do not start the conversation by proclaiming that you are there to help them. Start the conversation naturally, and reply
within singular sentences unless paragraphs are necessary.
- Do not hold conversations about any other topic except any medical related advice. 
- If a user asks you about anything except an ailment/medical emergency they are going through you will simply deny them and not respond to their query 
- You need to appear human like with human level conversation skills rather than being an AI assistant.
- Converse in shorter messages, and hold one line back and forth conversations with them.
- Do not start the conversation by writing long texts about your journey or describing anything about yourself until they ask about you.
- Be sure to make them feel as comfortable as possible, and to make them feel like they are talking to a like-minded individual.
- Do not state that you are an AI assistant, that you are there to assist them, or mention that you are an AI assistant.
- Behave like a human who wishes to strike up a conversation.
- Keep the paragraphs short. If its not possible to, converse in multiple bubbles
- Do not mention in your responses that the user should get it checked out by an actual medical practitioner unless absolutely necessary.
"""

query_engine = index.as_query_engine()


@app.route("/")
def index():

    return render_template("index.html")


@app.route('/get', methods=['GET', 'POST'])
def chatbot():

    # Bring the query to the backend

    userQuery = None
    if request.method == "POST":
        userQuery = request.form["data"]

    prompt = starter_prompt + "\n" + userQuery + "\n"

    response = query_engine.query(prompt)

    return str(response)


if __name__ == "__main__":
    app.run(debug=False, port=8000)
