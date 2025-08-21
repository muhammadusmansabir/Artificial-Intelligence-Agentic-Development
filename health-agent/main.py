import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load ENV

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize FastAPI
app = FastAPI(title="Health Chatbot with Memory")

# -------------------------
# Define Tools
# -------------------------
def calculate_bmi(weight: float, height: float) -> str:
    """Calculate BMI given weight (kg) and height (cm)."""
    h_m = height / 100
    bmi = weight / (h_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return f"Your BMI is {bmi:.2f} ({category})"

def daily_calories(age: int, weight: float, height: float) -> str:
    """Estimate daily calorie needs using Mifflin-St Jeor equation (sedentary)."""
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    calories = bmr * 1.2
    return f"Estimated daily calorie needs: {calories:.0f} kcal"

# -------------------------
# Setup LLM + Tools
# -------------------------
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY)
llm_with_tools = llm.bind_tools([calculate_bmi, daily_calories])

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build Graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([calculate_bmi, daily_calories]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm", tools_condition)
builder.add_edge("tools", END)
graph = builder.compile()

# -------------------------
# Global Conversation Memory
# -------------------------
conversation_history: list[AnyMessage] = []

# -------------------------
# FastAPI Endpoint
# -------------------------
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    global conversation_history

    # Append user input
    conversation_history.append(HumanMessage(content=req.message))

    # Run graph with history
    result = graph.invoke({"messages": conversation_history})

    # Save AI/tool outputs to history
    for m in result["messages"]:
        if m not in conversation_history:
            conversation_history.append(m)

    # Collect last non-empty response (AI or tool output)
    responses = [str(m.content) for m in result["messages"] if getattr(m, "content", None)]
    return {"response": responses[-1] if responses else "No response generated."}

