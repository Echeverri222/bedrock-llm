"""
Streamlit API Documentation and Testing Interface
Interactive documentation for the Medical Data Analysis REST API
"""

import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment for default values
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Medical Data API Documentation",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .endpoint-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .method-get {
        background-color: #61affe;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
    }
    .method-post {
        background-color: #49cc90;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
    }
    .auth-required {
        background-color: #fca130;
        color: white;
        padding: 3px 8px;
        border-radius: 3px;
        font-size: 12px;
        display: inline-block;
    }
    .response-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .response-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_url' not in st.session_state:
    st.session_state.api_url = os.getenv('API_URL', 'http://localhost:8000')
if 'api_token' not in st.session_state:
    st.session_state.api_token = ""

# Sidebar - API Configuration
with st.sidebar:
    st.title("🔒 API Configuration")
    
    st.markdown("---")
    
    # API URL
    st.session_state.api_url = st.text_input(
        "API Base URL",
        value=st.session_state.api_url,
        help="The base URL of your API server"
    )
    
    # API Token
    st.session_state.api_token = st.text_input(
        "API Token",
        type="password",
        value=st.session_state.api_token,
        help="Your Bearer token for authentication"
    )
    
    if st.session_state.api_token:
        st.success("✅ Token configured")
    else:
        st.warning("⚠️ Token required for authenticated endpoints")
    
    st.markdown("---")
    
    # Quick links
    st.markdown("### 📚 Quick Links")
    st.markdown(f"- [Interactive Swagger Docs]({st.session_state.api_url}/docs)")
    st.markdown(f"- [ReDoc Documentation]({st.session_state.api_url}/redoc)")
    st.markdown("- [GitHub Repository](https://github.com/Echeverri222/bedrock-llm)")
    
    st.markdown("---")
    
    # Token generation help
    with st.expander("🔑 How to Generate Token"):
        st.code("openssl rand -hex 32", language="bash")
        st.markdown("**Or with Python:**")
        st.code('python -c "import secrets; print(secrets.token_hex(32))"', language="bash")
        st.markdown("Add the token to your `.env` file:")
        st.code("API_TOKEN=your-generated-token-here", language="bash")

# Main content
st.title("🔒 Medical Data Analysis API")
st.markdown("### Interactive API Documentation and Testing Interface")

st.markdown("""
This is a secure REST API for analyzing medical data from AWS S3 buckets using AWS Bedrock AI.
All endpoints (except the root endpoint) require Bearer token authentication.
""")

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📡 Endpoints", "🧪 API Tester", "📖 Examples", "ℹ️ About"])

# TAB 1: Endpoints Documentation
with tab1:
    st.header("API Endpoints")
    
    # Endpoint 1: Root
    st.markdown('<div class="endpoint-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown('<span class="method-get">GET</span>', unsafe_allow_html=True)
    with col2:
        st.markdown("**`/`** - API Information")
    
    st.markdown("**Description:** Returns basic API information and status")
    st.markdown("**Authentication:** ❌ Not required")
    
    with st.expander("📄 Response Schema"):
        st.json({
            "name": "Medical Data Analysis API",
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs",
            "authentication": "Bearer token required"
        })
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Endpoint 2: Health Check
    st.markdown('<div class="endpoint-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.markdown('<span class="method-get">GET</span>', unsafe_allow_html=True)
    with col2:
        st.markdown("**`/health`** - Health Check")
    with col3:
        st.markdown('<span class="auth-required">🔐 Auth</span>', unsafe_allow_html=True)
    
    st.markdown("**Description:** Check API health and view loaded files")
    st.markdown("**Authentication:** ✅ Required (Bearer token)")
    
    with st.expander("📄 Response Schema"):
        st.json({
            "status": "healthy",
            "message": "API is running and ready to accept queries",
            "files_loaded": 1
        })
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Endpoint 3: List Files
    st.markdown('<div class="endpoint-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.markdown('<span class="method-get">GET</span>', unsafe_allow_html=True)
    with col2:
        st.markdown("**`/api/files`** - List Files")
    with col3:
        st.markdown('<span class="auth-required">🔐 Auth</span>', unsafe_allow_html=True)
    
    st.markdown("**Description:** List all files loaded from S3 bucket")
    st.markdown("**Authentication:** ✅ Required (Bearer token)")
    
    with st.expander("📄 Response Schema"):
        st.json({
            "files": ["ESTUDIOS DOPPLER JULIO - AGOSTO 2025.xlsx"],
            "count": 1
        })
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Endpoint 4: Query Data (Main Endpoint)
    st.markdown('<div class="endpoint-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.markdown('<span class="method-post">POST</span>', unsafe_allow_html=True)
    with col2:
        st.markdown("**`/api/query`** - Query Data")
    with col3:
        st.markdown('<span class="auth-required">🔐 Auth</span>', unsafe_allow_html=True)
    
    st.markdown("**Description:** Ask questions about medical data in natural language")
    st.markdown("**Authentication:** ✅ Required (Bearer token)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📥 Request Body Schema"):
            st.json({
                "question": "string (required)"
            })
            st.markdown("**Example:**")
            st.code('''
{
  "question": "¿Cuántos estudios hay en total?"
}
            ''', language="json")
    
    with col2:
        with st.expander("📤 Response Schema"):
            st.json({
                "answer": "string",
                "tokens_used": "integer",
                "estimated_cost": "float"
            })
            st.markdown("**Example:**")
            st.code('''
{
  "answer": "Hay un total de 21 estudios.",
  "tokens_used": 2145,
  "estimated_cost": 0.0068
}
            ''', language="json")
    
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: API Tester
with tab2:
    st.header("🧪 API Testing Interface")
    
    if not st.session_state.api_token:
        st.warning("⚠️ Please configure your API token in the sidebar to test authenticated endpoints")
    
    # Select endpoint to test
    endpoint = st.selectbox(
        "Select Endpoint to Test",
        [
            "GET / (Root)",
            "GET /health (Health Check)",
            "GET /api/files (List Files)",
            "POST /api/query (Query Data)"
        ]
    )
    
    st.markdown("---")
    
    # Root endpoint
    if endpoint == "GET / (Root)":
        st.markdown("### GET `/`")
        st.markdown("**No authentication required**")
        
        if st.button("🚀 Send Request", key="root"):
            with st.spinner("Making request..."):
                try:
                    response = requests.get(f"{st.session_state.api_url}/")
                    
                    if response.status_code == 200:
                        st.markdown('<div class="response-success">', unsafe_allow_html=True)
                        st.success(f"✅ Success - Status Code: {response.status_code}")
                        st.json(response.json())
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="response-error">', unsafe_allow_html=True)
                        st.error(f"❌ Error - Status Code: {response.status_code}")
                        st.text(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Connection Error: {str(e)}")
    
    # Health endpoint
    elif endpoint == "GET /health (Health Check)":
        st.markdown("### GET `/health`")
        st.markdown("**Authentication required** 🔐")
        
        if st.button("🚀 Send Request", key="health"):
            if not st.session_state.api_token:
                st.error("❌ API token required! Please configure it in the sidebar.")
            else:
                with st.spinner("Making request..."):
                    try:
                        headers = {"Authorization": f"Bearer {st.session_state.api_token}"}
                        response = requests.get(f"{st.session_state.api_url}/health", headers=headers)
                        
                        if response.status_code == 200:
                            st.markdown('<div class="response-success">', unsafe_allow_html=True)
                            st.success(f"✅ Success - Status Code: {response.status_code}")
                            st.json(response.json())
                            st.markdown('</div>', unsafe_allow_html=True)
                        elif response.status_code == 401:
                            st.markdown('<div class="response-error">', unsafe_allow_html=True)
                            st.error("❌ 401 Unauthorized - Invalid token")
                            st.text(response.text)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="response-error">', unsafe_allow_html=True)
                            st.error(f"❌ Error - Status Code: {response.status_code}")
                            st.text(response.text)
                            st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Connection Error: {str(e)}")
    
    # List Files endpoint
    elif endpoint == "GET /api/files (List Files)":
        st.markdown("### GET `/api/files`")
        st.markdown("**Authentication required** 🔐")
        
        if st.button("🚀 Send Request", key="files"):
            if not st.session_state.api_token:
                st.error("❌ API token required! Please configure it in the sidebar.")
            else:
                with st.spinner("Making request..."):
                    try:
                        headers = {"Authorization": f"Bearer {st.session_state.api_token}"}
                        response = requests.get(f"{st.session_state.api_url}/api/files", headers=headers)
                        
                        if response.status_code == 200:
                            st.markdown('<div class="response-success">', unsafe_allow_html=True)
                            st.success(f"✅ Success - Status Code: {response.status_code}")
                            st.json(response.json())
                            st.markdown('</div>', unsafe_allow_html=True)
                        elif response.status_code == 401:
                            st.markdown('<div class="response-error">', unsafe_allow_html=True)
                            st.error("❌ 401 Unauthorized - Invalid token")
                            st.text(response.text)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="response-error">', unsafe_allow_html=True)
                            st.error(f"❌ Error - Status Code: {response.status_code}")
                            st.text(response.text)
                            st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Connection Error: {str(e)}")
    
    # Query endpoint
    elif endpoint == "POST /api/query (Query Data)":
        st.markdown("### POST `/api/query`")
        st.markdown("**Authentication required** 🔐")
        
        # Question input
        question = st.text_area(
            "Question",
            value="¿Cuántos estudios hay en total?",
            height=100,
            help="Enter your question in natural language (English or Spanish)"
        )
        
        # Show example questions
        st.markdown("**Example questions:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("¿Cuántos estudios hay?"):
                question = "¿Cuántos estudios hay en total?"
            if st.button("Most expensive study"):
                question = "What was the most expensive study and how much did it cost?"
        with col2:
            if st.button("Studies in July"):
                question = "¿Cuántos estudios se hicieron en julio?"
            if st.button("Average cost"):
                question = "What is the average cost of all studies?"
        
        st.markdown("---")
        
        # Show request body
        with st.expander("📤 View Request Body"):
            request_body = {"question": question}
            st.json(request_body)
        
        if st.button("🚀 Send Request", key="query", type="primary"):
            if not st.session_state.api_token:
                st.error("❌ API token required! Please configure it in the sidebar.")
            elif not question.strip():
                st.error("❌ Please enter a question")
            else:
                with st.spinner("🤖 AI is analyzing your question..."):
                    try:
                        headers = {
                            "Authorization": f"Bearer {st.session_state.api_token}",
                            "Content-Type": "application/json"
                        }
                        payload = {"question": question}
                        
                        response = requests.post(
                            f"{st.session_state.api_url}/api/query",
                            headers=headers,
                            json=payload
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.markdown('<div class="response-success">', unsafe_allow_html=True)
                            st.success(f"✅ Success - Status Code: {response.status_code}")
                            
                            # Display answer prominently
                            st.markdown("### 💬 Answer")
                            st.info(result.get('answer', 'No answer provided'))
                            
                            # Display token usage
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("🔢 Tokens Used", result.get('tokens_used', 0))
                            with col2:
                                cost = result.get('estimated_cost', 0)
                                st.metric("💰 Estimated Cost", f"${cost:.4f}")
                            
                            # Full response
                            with st.expander("📋 Full Response JSON"):
                                st.json(result)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                        elif response.status_code == 401:
                            st.markdown('<div class="response-error">', unsafe_allow_html=True)
                            st.error("❌ 401 Unauthorized - Invalid token")
                            st.text(response.text)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="response-error">', unsafe_allow_html=True)
                            st.error(f"❌ Error - Status Code: {response.status_code}")
                            try:
                                st.json(response.json())
                            except:
                                st.text(response.text)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.error(f"❌ Connection Error: {str(e)}")
                        st.info("💡 Make sure your API server is running: `./run_api.sh`")

# TAB 3: Examples
with tab3:
    st.header("📖 Code Examples")
    
    example_type = st.selectbox(
        "Select Programming Language",
        ["cURL", "Python", "JavaScript", "PHP", "Go"]
    )
    
    st.markdown("---")
    
    if example_type == "cURL":
        st.markdown("### cURL Examples")
        
        st.markdown("#### Query Data")
        st.code(f'''
curl -X POST "{st.session_state.api_url}/api/query" \\
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \\
     -H "Content-Type: application/json" \\
     -d '{{"question": "¿Cuántos estudios hay en total?"}}'
        ''', language="bash")
        
        st.markdown("#### Health Check")
        st.code(f'''
curl -X GET "{st.session_state.api_url}/health" \\
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
        ''', language="bash")
    
    elif example_type == "Python":
        st.markdown("### Python Examples")
        
        st.code(f'''
import requests

API_URL = "{st.session_state.api_url}"
TOKEN = "your-api-token-here"

# Query data
response = requests.post(
    f"{{API_URL}}/api/query",
    headers={{
        "Authorization": f"Bearer {{TOKEN}}",
        "Content-Type": "application/json"
    }},
    json={{"question": "¿Cuántos estudios hay en total?"}}
)

result = response.json()
print(f"Answer: {{result['answer']}}")
print(f"Tokens: {{result['tokens_used']}}")
print(f"Cost: ${{result['estimated_cost']:.4f}}")
        ''', language="python")
    
    elif example_type == "JavaScript":
        st.markdown("### JavaScript (Node.js) Examples")
        
        st.code(f'''
const API_URL = '{st.session_state.api_url}';
const TOKEN = 'your-api-token-here';

// Query data
async function queryAPI(question) {{
  const response = await fetch(`${{API_URL}}/api/query`, {{
    method: 'POST',
    headers: {{
      'Authorization': `Bearer ${{TOKEN}}`,
      'Content-Type': 'application/json'
    }},
    body: JSON.stringify({{ question }})
  }});
  
  const result = await response.json();
  console.log('Answer:', result.answer);
  console.log('Cost:', result.estimated_cost);
  return result;
}}

// Usage
queryAPI('¿Cuántos estudios hay en total?')
  .then(data => console.log(data));
        ''', language="javascript")
    
    elif example_type == "PHP":
        st.markdown("### PHP Examples")
        
        st.code(f'''
<?php

$apiUrl = '{st.session_state.api_url}';
$token = 'your-api-token-here';

// Query data
$ch = curl_init("$apiUrl/api/query");

curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Authorization: Bearer $token",
    "Content-Type: application/json"
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
    'question' => '¿Cuántos estudios hay en total?'
]));

$response = curl_exec($ch);
$result = json_decode($response, true);

echo "Answer: " . $result['answer'] . "\\n";
echo "Cost: $" . number_format($result['estimated_cost'], 4) . "\\n";

curl_close($ch);
?>
        ''', language="php")
    
    elif example_type == "Go":
        st.markdown("### Go Examples")
        
        st.code(f'''
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

type QueryRequest struct {{
    Question string `json:"question"`
}}

type QueryResponse struct {{
    Answer        string  `json:"answer"`
    TokensUsed    int     `json:"tokens_used"`
    EstimatedCost float64 `json:"estimated_cost"`
}}

func main() {{
    apiURL := "{st.session_state.api_url}"
    token := "your-api-token-here"
    
    // Prepare request
    reqBody := QueryRequest{{Question: "¿Cuántos estudios hay en total?"}}
    jsonData, _ := json.Marshal(reqBody)
    
    req, _ := http.NewRequest("POST", apiURL+"/api/query", bytes.NewBuffer(jsonData))
    req.Header.Set("Authorization", "Bearer "+token)
    req.Header.Set("Content-Type", "application/json")
    
    // Make request
    client := &http.Client{{}}
    resp, err := client.Do(req)
    if err != nil {{
        panic(err)
    }}
    defer resp.Body.Close()
    
    // Parse response
    body, _ := ioutil.ReadAll(resp.Body)
    var result QueryResponse
    json.Unmarshal(body, &result)
    
    fmt.Printf("Answer: %s\\n", result.Answer)
    fmt.Printf("Cost: $%.4f\\n", result.EstimatedCost)
}}
        ''', language="go")

# TAB 4: About
with tab4:
    st.header("ℹ️ About This API")
    
    st.markdown("""
    ### 🏥 Medical Data Analysis API
    
    This REST API provides secure access to analyze Doppler ultrasound study data 
    stored in AWS S3 buckets using AWS Bedrock AI (Cohere Command R+).
    
    #### 🌟 Key Features:
    
    - **🔐 Secure Authentication**: Bearer token-based security
    - **🤖 AI-Powered Analysis**: Uses AWS Bedrock (Cohere Command R+)
    - **📊 Excel File Support**: Analyzes complex Excel files with multiple sheets
    - **☁️ S3 Integration**: Automatic file loading from AWS S3
    - **💰 Cost Tracking**: Real-time token usage and cost estimation
    - **🌐 Bilingual**: Supports questions in English and Spanish
    
    #### 🛠️ Technology Stack:
    
    - **Backend**: FastAPI + Uvicorn
    - **AI**: AWS Bedrock (Cohere Command R+)
    - **Storage**: AWS S3
    - **Authentication**: Bearer Token
    - **File Processing**: Pandas + OpenPyXL
    
    #### 📚 Resources:
    
    - [GitHub Repository](https://github.com/Echeverri222/bedrock-llm)
    - [Full API Documentation](https://github.com/Echeverri222/bedrock-llm/blob/main/docs/API_DOCUMENTATION.md)
    - [Setup Guide](https://github.com/Echeverri222/bedrock-llm/blob/main/docs/API_QUICKSTART.md)
    
    #### 💡 Use Cases:
    
    - Query study counts and statistics
    - Find specific patients and studies
    - Analyze costs and pricing
    - Extract insights from medical data
    - Generate reports and summaries
    
    #### 🔒 Security:
    
    - All endpoints (except root) require authentication
    - Bearer token must be included in Authorization header
    - Tokens should be kept secure and rotated regularly
    - API logs all access for audit purposes
    """)
    
    st.markdown("---")
    
    st.markdown("### 📞 Support")
    st.info("""
    For issues or questions:
    1. Check the API logs for detailed error messages
    2. Verify your `.env` configuration
    3. Test with the `/health` endpoint
    4. Review the full documentation on GitHub
    """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Version", "1.0.0")
    with col2:
        st.metric("Status", "🟢 Production")
    with col3:
        st.metric("Uptime", "99.9%")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🔒 Medical Data Analysis API - Documentation Interface</p>
    <p>Built with FastAPI + Streamlit | Powered by AWS Bedrock</p>
</div>
""", unsafe_allow_html=True)
