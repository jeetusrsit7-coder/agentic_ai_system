from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import os

app = Flask(__name__)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

def calculator(query):
    try:
        return str(eval(query))
    except:
        return "Invalid expression"

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Performs math calculations"
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

@app.route("/")
def home():
    return "Agent Running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")

    response = agent.run(message)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
