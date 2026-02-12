from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
import dotenv
import os
from agents import *


from Constants import *
from knowledge_base import knowledge_base

def orchestrate_agent(input_message):
    # Load the Groq API key from the environment (set this in your .env file as GROQ_API_KEY)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set. Please add it to your environment or .env file.")

   
    Sister =  Agent(
        model=Groq_Clint,
        system_prompt=ITSM_AGENT_SYSTEM_PROMPT,
        team=[Task_Analyzer,Incident_Analyzer,Ticket_Creation,Root_Cause_Analysis,resolution_discovery],
        instructions=[
            "Analyze User input.",
            "Delegate the task to ONLY ONE appropriate team member.",
            "Do not call multiple team members.",
            "After receiving response, return final answer."
        ],
        markdown=True,
        # knowledge=knowledge_base,

        show_tool_calls=True,
        debug_mode=True
        
       
    )
    # Sister.knowledge.load(recreate=True)

    response= Sister.run(input_message, stream=False)
    return response.content

response = orchestrate_agent(DDOS_LOGS)
print(response)

