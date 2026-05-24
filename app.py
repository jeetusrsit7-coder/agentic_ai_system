from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
import os

app = Flask(__name__)

# OpenAI Model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Simple Tool
def calculator_tool(query):
    try:
        return str(eval(query))
    except:
        return "Invalid math expression"

tools = [
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Useful for solving math calculations"
    )
]

# Initialize Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

@app.route("/")
def home():
    return "AI Agent Running on Render!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")

    response = agent.run(user_input)

    return jsonify({
        "response": response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
