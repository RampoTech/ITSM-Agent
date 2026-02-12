import streamlit as st
import os
from dotenv import load_dotenv
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from phi.utils.pprint import pprint_run_response
from agents import *
from Constants import *

# ---------------------------------
# Load env
# ---------------------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not set")
    st.stop()

# ---------------------------------
# Initialize Agent
# ---------------------------------
Sister = Agent(
    model=Groq_Clint,
    system_prompt=ITSM_AGENT_SYSTEM_PROMPT,
    team=[
        Task_Analyzer,
        Incident_Analyzer,
        Ticket_Creation,
        Root_Cause_Analysis,
        resolution_discovery
    ],
    instructions=[
        "Analyze User input.",
        "Delegate the task to ONLY ONE appropriate team member.",
        "Do not call multiple team members.",
        "After receiving response, return final answer."
    ],
    markdown=True,
    show_tool_calls=True,
    debug_mode=True
)

# ---------------------------------
# Streamlit UI
# ---------------------------------
st.set_page_config(page_title="ITSM Agent", layout="wide")
st.title("🎫 ITSM Ticket Orchestrator")

user_input = st.text_area("Enter Logs / Incident Details", height=150)

if st.button("Run Agent", type="primary"):
    if not user_input.strip():
        st.warning("Please enter input")
    else:
        # Create containers for different sections
        status_container = st.container()
        steps_container = st.container()
        final_container = st.container()
        
        with status_container:
            st.markdown("## 🔄 Processing Request...")
        
        with steps_container:
            st.markdown("## 🔍 Execution Steps")
            
            # Create placeholder for streaming updates
            response_container = st.empty()
        
        try:
            # Use streaming to show real-time updates
            run_response = Sister.run(user_input, stream=True)
            
            # Variables to accumulate the response
            full_response = ""
            step_number = 0
            
            # Process each chunk from the stream
            for chunk in run_response:
                # Chunk can be a string or have content attribute
                if hasattr(chunk, 'content'):
                    content = chunk.content
                else:
                    content = str(chunk)
                
                if content:
                    full_response += content
                    step_number += 1
                    
                    # Update the container with accumulated response
                    with response_container.container():
                        st.markdown(f"**Stream Chunk {step_number}:**")
                        st.write(content)
                        st.write("---")
            
            # Clear status
            status_container.empty()
            
            # Get the final response object
            # Note: After streaming, we need to run again to get the full RunResponse
            final_response: RunResponse = Sister.run(user_input, stream=False)
            
            # ----------------------------
            # Display execution flow
            # ----------------------------
            with steps_container:
                st.markdown("### 📊 Agent Execution Flow")
                
                for idx, message in enumerate(final_response.messages, 1):
                    with st.expander(f"Step {idx}: {message.role.upper()}", expanded=True):
                        if message.role == "user":
                            st.info(f"**User Input**")
                        elif message.role == "assistant":
                            st.success(f"**Assistant Response**")
                        elif message.role == "tool":
                            st.warning(f"**Tool Execution**")
                        
                        st.markdown(message.content)
                        
                        # Show tool calls if any
                        if hasattr(message, 'tool_calls') and message.tool_calls:
                            st.json(message.tool_calls)
            
            # ----------------------------
            # Final Answer
            # ----------------------------
            with final_container:
                st.markdown("---")
                st.markdown("## ✅ Final Response")
                st.success("Processing complete!")
                st.markdown(final_response.content)
            
            # ----------------------------
            # Detailed Information
            # ----------------------------
            with st.expander("🧠 Detailed Execution Information", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🔹 Run ID")
                    st.code(final_response.run_id)
                
                with col2:
                    if final_response.metrics:
                        st.markdown("### 🔹 Metrics")
                        metrics = final_response.metrics
                        st.metric("Total Time", f"{metrics.get('time', 'N/A')}s" if metrics.get('time') else 'N/A')
                        st.metric("Total Tokens", metrics.get('total_tokens', 'N/A'))
                
                st.markdown("### 🔹 Complete Message History")
                for idx, msg in enumerate(final_response.messages, 1):
                    st.markdown(f"**Message {idx} - Role: {msg.role}**")
                    st.text_area(
                        f"Content {idx}",
                        msg.content,
                        height=150,
                        key=f"msg_detail_{idx}",
                        disabled=True
                    )
                    st.write("---")
                
                if final_response.tool_calls:
                    st.markdown("### 🔹 Tool Calls")
                    for idx, tool in enumerate(final_response.tool_calls, 1):
                        st.markdown(f"**Tool Call {idx}:**")
                        st.json(tool)
        
        except Exception as e:
            status_container.empty()
            st.error(f"❌ Error occurred: {str(e)}")
            st.exception(e)

# ---------------------------------
# Sidebar with Instructions
# ---------------------------------
with st.sidebar:
    st.markdown("## 📋 How to Use")
    st.markdown("""
    1. Enter your incident details or logs in the text area
    2. Click **Run Agent** to process
    3. Watch the execution steps in real-time
    4. View the final response and detailed execution info
    """)
    
    st.markdown("## 🤖 Agent Team")
    st.markdown("""
    - **Task Analyzer**
    - **Incident Analyzer**
    - **Ticket Creation**
    - **Root Cause Analysis**
    - **Resolution Discovery**
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    st.markdown(f"**Debug Mode:** Enabled")
    st.markdown(f"**Show Tool Calls:** Enabled")