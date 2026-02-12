from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from phi.model.ollama import Ollama

import dotenv
import os
from tools import create_ticket ,root_cause ,resolution

from knowledge_base import knowledge_base
dotenv.load_dotenv()

def get_key():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set. Please add it to your environment or .env file.")
    return api_key

def get_ollama():
    OLLAMA_HOST = os.getenv("OLLAMA_HOST")
    if not OLLAMA_HOST:
        raise RuntimeError("GROQ_API_KEY not set. Please add it to your environment or .env file.")
    return OLLAMA_HOST

OLLAMA_HOST= get_ollama()


api_key=get_key()


ollama_Clint= Ollama(id="jewelzufo/Qwen2.5-Coder-0.5B-Instruct-GGUF-Assistant:latest",
                    host=OLLAMA_HOST,
                    
                     )
Groq_Clint= Groq(
            id="moonshotai/kimi-k2-instruct-0905",
            api_key=api_key,
            )

Incident_Analyzer = Agent(
        markdown=True,
        name="Incident_Analyzer",
        model=ollama_Clint,
        role="The AI agent analyzes incoming communication and identifies the intent to understand the nature of the incident.",
        # tools=[SumOfTowNumbers],
        show_tool_calls=True,
        
    )
Ticket_Creation = Agent(
        name="Ticket Creation",
        role="Automatically create an ITSM ticket  based on the analyzed incident information.",
        model=ollama_Clint,
        markdown=True,
        tools=[create_ticket],
        show_tool_calls=True,
        
    )
Root_Cause_Analysis = Agent(
        name="Root Cause Analysis",
        # role="The agent correlates application logs to identify patterns and determine the probable root cause of the incident.",
        role="Retrieve relevant solutions from the Knowledge Base using semantic search to find the best determine the probable root cause of the incident",
        model=ollama_Clint,
        markdown=True,
        tools=[root_cause],
        knowledge=knowledge_base,
        
        search_knowledge=True,
        show_tool_calls=True,
        
    )
resolution_discovery = Agent(
        name="resolution_discovery",
        role="Retrieve relevant solutions from the Knowledge Base using semantic search to find the best resolution steps.",
        # role="Retrieve relevant solutions from resolution tool and return a resolution steps.",
        model= ollama_Clint,
        markdown=True,
        knowledge=knowledge_base,
        
        search_knowledge=True,
        # tools=[resolution],
        show_tool_calls=True,
        
    )
    
Task_Analyzer = Agent(
        name="Task Analyzer",
        role="categorize The Task and return the type of Task Based on input as a general or song or maths",
        model=ollama_Clint,
        markdown=True,
        show_tool_calls=True,
        
    )
general_agent= Agent(
    name="General Agent",
        role="answer the generic questions",
        model=ollama_Clint,
        markdown=True,
        show_tool_calls=True,
        
    )