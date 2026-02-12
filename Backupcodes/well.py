

import streamlit as st
import os
from dotenv import load_dotenv
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from phi.run.response import RunEvent
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
# Initialize Agent with caching
# ---------------------------------
@st.cache_resource
def get_agent() -> Agent:
    return Agent(
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

Sister = get_agent()

# ---------------------------------
# Streamlit UI
# ---------------------------------
st.set_page_config(page_title="ITSM Agent", layout="wide")
st.title("🎫 ITSM Ticket Orchestrator")

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area(
        "Enter Logs / Incident Details",
        height=150,
        placeholder="Paste your server logs or describe the incident..."
    )

with col2:
    st.markdown("### 🤖 Agent Team")
    st.markdown("""
    1. 🔍 **Incident Analyzer**
    2. 🎫 **Ticket Creation**
    3. 🔬 **Root Cause Analysis**
    4. 💡 **Resolution Discovery**
    """)

if st.button("🚀 Run Agent", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("⚠️ Please enter incident details")
    else:
        # Create containers for different sections
        status_container = st.container()
        steps_container = st.container()
        final_container = st.container()
        
        with status_container:
            progress_bar = st.progress(0, text="🔄 Initializing agent...")
        
        with steps_container:
            st.markdown("## 📋 Real-Time Execution Steps")
            steps_placeholder = st.empty()
        
        try:
            # Track execution steps
            execution_steps = []
            step_count = 0
            total_steps = 4  # Estimated total steps
            
            # Run agent with stream_intermediate_steps=True
            response_stream = Sister.run(
                user_input, 
                stream=True,
                stream_intermediate_steps=True
            )
            
            # Process each event from the stream
            full_content = ""
            for response_chunk in response_stream:
                if isinstance(response_chunk, RunResponse):
                    event = response_chunk.event
                    content = response_chunk.content
                    
                    # Handle different events
                    if event == RunEvent.run_started.value:
                        step_count += 1
                        progress_bar.progress(step_count / total_steps, text="▶️ Agent run started...")
                        execution_steps.append({
                            "icon": "🚀",
                            "title": "Run Started",
                            "content": "Agent execution initiated",
                            "type": "info"
                        })
                    
                    elif event == RunEvent.tool_call_started.value:
                        step_count += 1
                        progress_bar.progress(min(step_count / total_steps, 0.9), text=f"🔧 Tool call started...")
                        if response_chunk.tools:
                            tool_info = response_chunk.tools[-1]
                            execution_steps.append({
                                "icon": "🔧",
                                "title": f"Tool Call: {tool_info.get('function_name', 'Unknown')}",
                                "content": str(tool_info.get('arguments', '')),
                                "type": "tool"
                            })
                    
                    elif event == RunEvent.tool_call_completed.value:
                        progress_bar.progress(min(step_count / total_steps, 0.95), text="✅ Tool call completed...")
                        if content:
                            execution_steps.append({
                                "icon": "✅",
                                "title": "Tool Result",
                                "content": str(content),
                                "type": "success"
                            })
                    
                    elif event == RunEvent.updating_memory.value:
                        progress_bar.progress(0.98, text="💾 Updating memory...")
                        execution_steps.append({
                            "icon": "💾",
                            "title": "Updating Memory",
                            "content": "Saving conversation history",
                            "type": "info"
                        })
                    
                    elif event == RunEvent.run_completed.value:
                        progress_bar.progress(1.0, text="✨ Run completed!")
                        execution_steps.append({
                            "icon": "✨",
                            "title": "Run Completed",
                            "content": "Agent execution finished successfully",
                            "type": "success"
                        })
                    
                    elif event == RunEvent.run_response.value:
                        # Accumulate the actual response content
                        if isinstance(content, str):
                            full_content += content
                    
                    # Update the steps display in real-time
                    with steps_placeholder.container():
                        for idx, step in enumerate(execution_steps, 1):
                            if step["type"] == "info":
                                with st.expander(f"{step['icon']} Step {idx}: {step['title']}", expanded=False):
                                    st.info(step["content"])
                            elif step["type"] == "success":
                                with st.expander(f"{step['icon']} Step {idx}: {step['title']}", expanded=False):
                                    st.success(step["content"])
                            elif step["type"] == "tool":
                                with st.expander(f"{step['icon']} Step {idx}: {step['title']}", expanded=True):
                                    st.code(step["content"], language="json")
            
            # Clear progress bar
            status_container.empty()
            
            # Display final response
            with final_container:
                st.markdown("---")
                st.markdown("## ✅ Final ITSM Report")
                st.success("Processing complete!")
                
                # Display the accumulated content
                if full_content:
                    st.markdown(full_content)
                
                # Add download button
                if full_content:
                    st.download_button(
                        label="📥 Download Report",
                        data=full_content,
                        file_name="itsm_report.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
        
        except Exception as e:
            status_container.empty()
            st.error(f"❌ Error occurred: {str(e)}")
            with st.expander("📋 Error Details"):
                st.exception(e)

# ---------------------------------
# Sidebar
# ---------------------------------
with st.sidebar:
    st.markdown("## 📋 How It Works")
    st.markdown("""
    This orchestrator delegates tasks to specialized agents:
    
    **Workflow:**
    1. 🔍 **Analyze** the incident
    2. 🎫 **Create** ITSM ticket
    3. 🔬 **Identify** root cause
    4. 💡 **Discover** resolution
    """)
    
    st.markdown("---")
    
    st.markdown("## ⚙️ Settings")
    st.markdown(f"""
    - **Debug Mode:** ✅ Enabled
    - **Stream Steps:** ✅ Enabled
    - **Team Size:** {len(Sister.team)} agents
    """)
    
    st.markdown("---")
    
    with st.expander("💡 Example Input"):
        st.code("""
[2026-02-12 10:00:06] | 203.112.45.67 | GET  | /api/auth | 503 | 0
[2026-02-12 10:00:08] | 91.34.55.201  | POST | /login    | 429 | 0
        """, language="log")