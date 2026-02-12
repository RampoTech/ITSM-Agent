from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
import dotenv
import os
from pprint import pprint


from Constants import ORCHESTRATE_AGENT_SYSTEM_PROMPT ,INPUT ,Addition_Agent ,Tool_Call_Input,Team_Agent

dotenv.load_dotenv()


def SumOfTowNumbers(a: int, b: int):
    """
    Calculate the sum of two integers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    try :
        return str(a + b)
    except:
        return "Your Input is Wrong "
    
def Song_Name_identifier(Lyrics: str):
    """
    Identifies the song name based on the given lyrics.

    Parameters:
        Lyrics (str): A line or portion of song lyrics used to identify the song.

    Returns:
        str: A message indicating whether the song is recognized or not.

    Notes:
        - Currently, this function returns a fixed response.
        - Exception handling is included for future logic expansion.
    """
    # try:
    #     return "This Song IS Begile Movie Song , I Know"
    # except:
    return "sorry Brother I Can't Remember it"

     


def orchestrate_agent(input_message):
    # Load the Groq API key from the environment (set this in your .env file as GROQ_API_KEY)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set. Please add it to your environment or .env file.")

    MathTeacher = Agent(
        markdown=True,
        name="Math Teacher",
        model=Groq(
            id="openai/gpt-oss-120b",
            api_key=api_key,
            ),
        role="Solving mathematic operation ",
        tools=[SumOfTowNumbers],
        show_tool_calls=True,
        
    )
    Spotify = Agent(
        name="Spotify",
        role="Song Lyrics Detecter",
        model=Groq(
            id="openai/gpt-oss-120b",
            api_key=api_key,
            ),
        markdown=True,
        tools=[Song_Name_identifier],
        show_tool_calls=True,
        
    )
    Task_Analyzer = Agent(
        name="Task Analyzer",
        role="categorize The Task and return the type of Task Based on input as a general or song or maths",
        model=Groq(
            id="openai/gpt-oss-120b",
            api_key=api_key,
            ),
        markdown=True,
        show_tool_calls=True,
        
    )
    general_agent= Agent(
    name="General Agent",
        role="answer the generic questions",
        model=Groq(
            id="openai/gpt-oss-120b",
            api_key=api_key,
            ),
        markdown=True,
        show_tool_calls=True,
        
    )
    Sister =  Agent(
        model=Groq(
            id="openai/gpt-oss-120b",
            api_key=api_key,
            ),
        system_prompt=Team_Agent,
        team=[Task_Analyzer,MathTeacher,Spotify,general_agent],
        instructions=[
            "Analyze brother input.",
            "Delegate the task to ONLY ONE appropriate team member.",
            "Do not call multiple team members.",
            "After receiving response, return final answer."
        ],
        markdown=True,
        show_tool_calls=True,
        # debug_mode=True
        
       
    )

    return Sister.run(input_message, stream=False)

response = orchestrate_agent(Tool_Call_Input)
print(response.content)

