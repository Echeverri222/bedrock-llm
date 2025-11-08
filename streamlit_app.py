"""
Streamlit Web Interface for AWS Bedrock Data Analysis Agent
"""

import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tools.s3_loader import S3DataLoader
from agents.bedrock_agent import BedrockAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Medical Data Analysis Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
        st.session_state.messages = []
        st.session_state.agent = None
        st.session_state.s3_loader = None
        st.session_state.available_files = []
        st.session_state.total_tokens = 0
        st.session_state.total_cost = 0


def initialize_agent():
    """Initialize the Bedrock agent and S3 loader"""
    try:
        # Get environment variables
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION', 'sa-east-1')
        bedrock_region = os.getenv('BEDROCK_REGION', 'us-east-1')
        bedrock_model = os.getenv('BEDROCK_MODEL', 'cohere.command-r-plus-v1:0')
        s3_bucket = os.getenv('S3_BUCKET_NAME')

        # Validate required environment variables
        missing_vars = []
        if not aws_access_key:
            missing_vars.append('AWS_ACCESS_KEY_ID')
        if not aws_secret_key:
            missing_vars.append('AWS_SECRET_ACCESS_KEY')
        if not s3_bucket:
            missing_vars.append('S3_BUCKET_NAME')
        
        if missing_vars:
            st.error(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
            st.info("💡 Please create a `.env` file with your AWS credentials. See `config/env.example` for reference.")
            st.stop()

        # Initialize S3 loader
        with st.spinner("🔄 Connecting to AWS S3..."):
            st.session_state.s3_loader = S3DataLoader(
                bucket_name=s3_bucket,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
            files = st.session_state.s3_loader.list_files()
            st.session_state.available_files = files

        # Initialize Bedrock agent
        with st.spinner("🤖 Initializing AI Agent..."):
            st.session_state.agent = BedrockAgent(
                aws_region=bedrock_region,
                model_id=bedrock_model
            )
            st.session_state.agent.set_available_files(files)

        st.session_state.initialized = True
        return True

    except Exception as e:
        st.error(f"❌ Error initializing: {str(e)}")
        logger.error(f"Initialization error: {e}")
        return False


def display_sidebar():
    """Display sidebar with configuration and stats"""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Model info
        model = os.getenv('BEDROCK_MODEL', 'cohere.command-r-plus-v1:0')
        region = os.getenv('BEDROCK_REGION', 'us-east-1')
        
        st.info(f"""
        **Model**: {model.split('.')[1] if '.' in model else model}  
        **Region**: {region}
        """)
        
        # Files in S3
        st.markdown("### 📁 Available Files")
        if st.session_state.available_files:
            for file in st.session_state.available_files:
                st.text(f"📄 {file}")
        else:
            st.text("No files found")
        
        if st.button("🔄 Refresh Files", use_container_width=True):
            with st.spinner("Refreshing..."):
                files = st.session_state.s3_loader.list_files()
                st.session_state.available_files = files
                st.session_state.agent.set_available_files(files)
                st.rerun()
        
        st.markdown("---")
        
        # Token usage
        if st.session_state.agent:
            usage = st.session_state.agent.get_token_usage()
            st.markdown("### 💰 Usage Statistics")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Input Tokens", f"{usage['input_tokens']:,}")
            with col2:
                st.metric("Output Tokens", f"{usage['output_tokens']:,}")
            
            st.metric("Total Cost", f"${usage['estimated_cost_usd']:.4f}", 
                     help="Approximate cost based on Cohere Command R+ pricing")
        
        st.markdown("---")
        
        # Reset conversation
        if st.button("🗑️ Reset Conversation", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            if st.session_state.agent:
                st.session_state.agent.reset_conversation()
            st.rerun()
        
        # Info
        st.markdown("---")
        st.markdown("""
        <div style='font-size: 0.8rem; color: #666;'>
        🤖 Powered by AWS Bedrock<br>
        💡 Ask questions about your data<br>
        🔒 Data stays in your AWS account
        </div>
        """, unsafe_allow_html=True)


def display_chat_history():
    """Display chat message history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    """Main application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<p class="main-header">🏥 Medical Data Analysis Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ask questions about Doppler ultrasound studies from your S3 bucket</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize agent if not done
    if not st.session_state.initialized:
        if not initialize_agent():
            st.stop()
        st.success("✅ Connected successfully! You can start asking questions.")
    
    # Display sidebar
    display_sidebar()
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your data... (e.g., '¿Cuántos estudios hay en total?')"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Analyzing data..."):
                try:
                    response = st.session_state.agent.chat(prompt)
                    st.markdown(response)
                    
                    # Add assistant message
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Update token usage in sidebar
                    st.rerun()
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    logger.error(f"Chat error: {e}")


if __name__ == "__main__":
    main()

