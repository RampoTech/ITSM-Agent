import streamlit as st
import os
import json
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
# Helper Functions
# ---------------------------------
def get_agent_name_from_function(function_name: str) -> str:
    """Extract agent name from transfer function"""
    agent_map = {
        "transfer_task_to_task_analyzer": "📊 Task Analyzer",
        "transfer_task_to_incident_analyzer": "🔍 Incident Analyzer",
        "transfer_task_to_ticket_creation": "🎫 Ticket Creation",
        "transfer_task_to_root_cause_analysis": "🔬 Root Cause Analysis",
        "transfer_task_to_resolution_discovery": "💡 Resolution Discovery"
    }
    return agent_map.get(function_name, f"🤖 {function_name}")

def format_tool_arguments(arguments: dict) -> str:
    """Format tool arguments for display"""
    formatted = []
    for key, value in arguments.items():
        if isinstance(value, str) and len(value) > 100:
            formatted.append(f"**{key}:** {value[:100]}...")
        else:
            formatted.append(f"**{key}:** {value}")
    return "\n\n".join(formatted)

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
        # Create containers
        status_container = st.container()
        steps_container = st.container()
        final_container = st.container()
        
        with status_container:
            progress_bar = st.progress(0, text="🔄 Initializing agent...")
            status_text = st.empty()
        
        with steps_container:
            st.markdown("## 📋 Real-Time Execution Steps")
            steps_placeholder = st.empty()
        
        try:
            # Track execution steps
            execution_steps = []
            step_count = 0
            current_agent = None
            full_content = ""
            
            # Run agent with stream_intermediate_steps=True
            response_stream = Sister.run(
                user_input, 
                stream=True,
                stream_intermediate_steps=True
            )
            
            # Process each event from the stream
            for response_chunk in response_stream:
                if isinstance(response_chunk, RunResponse):
                    event = response_chunk.event
                    content = response_chunk.content
                    
                    # Handle different events
                    if event == RunEvent.run_started.value:
                        step_count += 1
                        progress_bar.progress(0.1, text="▶️ Agent orchestration started...")
                        status_text.info("🚀 **Status:** Orchestrator analyzing the request...")
                        
                        execution_steps.append({
                            "icon": "🚀",
                            "title": "Orchestrator Started",
                            "content": "Main orchestrator agent is analyzing the incident and determining workflow",
                            "type": "info",
                            "timestamp": response_chunk.created_at
                        })
                    
                    elif event == RunEvent.tool_call_started.value:
                        step_count += 1
                        
                        if response_chunk.tools:
                            tool_info = response_chunk.tools[-1]
                            function_name = tool_info.get('function_name', 'Unknown')
                            arguments = tool_info.get('arguments', {})
                            
                            # Detect agent delegation
                            if 'transfer_task' in function_name:
                                current_agent = get_agent_name_from_function(function_name)
                                progress_bar.progress(min(step_count / 10, 0.9), 
                                                     text=f"🔄 Delegating to {current_agent}...")
                                status_text.info(f"🔄 **Status:** Transferring task to {current_agent}")
                                
                                # Parse task description from arguments
                                task_desc = arguments.get('task_description', 'Processing...')
                                expected_output = arguments.get('expected_output', 'N/A')
                                
                                execution_steps.append({
                                    "icon": "🔄",
                                    "title": f"Delegating to {current_agent}",
                                    "content": f"**Task:** {task_desc}\n\n**Expected Output:** {expected_output}",
                                    "type": "delegation",
                                    "timestamp": response_chunk.created_at,
                                    "details": arguments
                                })
                            else:
                                execution_steps.append({
                                    "icon": "🔧",
                                    "title": f"Tool Call: {function_name}",
                                    "content": format_tool_arguments(arguments),
                                    "type": "tool",
                                    "timestamp": response_chunk.created_at
                                })
                    
                    elif event == RunEvent.tool_call_completed.value:
                        progress_bar.progress(min(step_count / 10, 0.95), text="✅ Processing response...")
                        
                        if content:
                            # Extract meaningful content
                            content_str = str(content)
                            
                            # Check if this is a ticket creation response
                            if 'Ticket' in content_str or 'TKT-' in content_str or 'TICK-' in content_str:
                                status_text.success("🎫 **Status:** ITSM Ticket Created!")
                                execution_steps.append({
                                    "icon": "🎫",
                                    "title": f"{current_agent or 'Agent'} - Ticket Created",
                                    "content": content_str,
                                    "type": "success",
                                    "timestamp": response_chunk.created_at
                                })
                            else:
                                execution_steps.append({
                                    "icon": "✅",
                                    "title": f"{current_agent or 'Agent'} - Completed",
                                    "content": content_str,
                                    "type": "success",
                                    "timestamp": response_chunk.created_at
                                })
                    
                    elif event == RunEvent.updating_memory.value:
                        progress_bar.progress(0.98, text="💾 Saving conversation...")
                        status_text.info("💾 **Status:** Updating memory...")
                        
                        execution_steps.append({
                            "icon": "💾",
                            "title": "Updating Memory",
                            "content": "Saving conversation history and context",
                            "type": "info",
                            "timestamp": response_chunk.created_at
                        })
                    
                    elif event == RunEvent.run_completed.value:
                        progress_bar.progress(1.0, text="✨ Completed!")
                        status_text.success("✨ **Status:** All steps completed successfully!")
                        
                        execution_steps.append({
                            "icon": "✨",
                            "title": "Orchestration Completed",
                            "content": "All agents have completed their tasks successfully",
                            "type": "success",
                            "timestamp": response_chunk.created_at
                        })
                    
                    elif event == RunEvent.run_response.value:
                        # Accumulate the actual response content
                        if isinstance(content, str):
                            full_content += content
                    
                    # Update the steps display in real-time
                    with steps_placeholder.container():
                        for idx, step in enumerate(execution_steps, 1):
                            # Choose expander state based on step type
                            is_expanded = step["type"] in ["delegation", "success"]
                            
                            with st.expander(f"{step['icon']} Step {idx}: {step['title']}", 
                                           expanded=is_expanded):
                                if step["type"] == "info":
                                    st.info(step["content"])
                                elif step["type"] == "success":
                                    st.success(step["content"])
                                elif step["type"] == "delegation":
                                    st.warning(step["content"])
                                    # Show additional details if available
                                    if "details" in step:
                                        with st.expander("📋 View Full Details"):
                                            st.json(step["details"])
                                elif step["type"] == "tool":
                                    st.code(step["content"], language="markdown")
                                
                                # Show timestamp if available
                                if step.get("timestamp"):
                                    st.caption(f"⏱️ Time: {step['timestamp']}")
            
            # Clear progress bar
            status_container.empty()
            
            # Display final response
            with final_container:
                st.markdown("---")
                st.markdown("## ✅ Final ITSM Report")
                
                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📄 Report", "📊 Summary", "🔍 Details"])
                
                with tab1:
                    if full_content:
                        st.markdown(full_content)
                    else:
                        st.info("No content generated")
                
                with tab2:
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Total Steps", len(execution_steps))
                    with col_b:
                        agent_calls = len([s for s in execution_steps if s["type"] == "delegation"])
                        st.metric("Agent Calls", agent_calls)
                    with col_c:
                        successful_steps = len([s for s in execution_steps if s["type"] == "success"])
                        st.metric("Successful Steps", successful_steps)
                
                with tab3:
                    st.json({
                        "total_steps": len(execution_steps),
                        "execution_flow": [s["title"] for s in execution_steps]
                    })
                
                # Add download button
                if full_content:
                    st.download_button(
                        label="📥 Download Report",
                        data=full_content,
                        file_name=f"itsm_report_{response_chunk.run_id}.md",
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
    The orchestrator delegates to specialized agents:
    
    **Sequential Workflow:**
    1. 🔍 **Incident Analysis**
       - Classifies the incident
       - Determines severity
    
    2. 🎫 **Ticket Creation**
       - Generates ITSM ticket
       - Assigns priority
    
    3. 🔬 **Root Cause Analysis**
       - Identifies probable causes
       - Technical analysis
    
    4. 💡 **Resolution Discovery**
       - Suggests fix steps
       - Knowledge base search
    """)
    
    st.markdown("---")
    
    st.markdown("## ⚙️ Configuration")
    st.markdown(f"""
    - **Model:** Groq
    - **Debug Mode:** ✅ Enabled
    - **Stream Steps:** ✅ Enabled
    - **Team Size:** {len(Sister.team)} agents
    """)
    
    st.markdown("---")
    
    with st.expander("💡 Example Input"):
        st.code("""
[2026-02-12 10:00:06] | 203.112.45.67 | GET  | /api/auth | 503 | 0
[2026-02-12 10:00:06] | 203.112.45.68 | GET  | /api/auth | 503 | 0
[2026-02-12 10:00:08] | 91.34.55.201  | POST | /login    | 429 | 0
[2026-02-12 10:00:09] | 91.34.55.202  | POST | /login    | 429 | 0
        """, language="log")
    
    st.markdown("---")
    st.caption("Built with Phidata & Streamlit")