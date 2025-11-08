"""
AWS Bedrock Agent with Function Calling
Handles questions about data using AWS Bedrock models
"""

import boto3
import json
import logging
from typing import List, Dict, Any
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.file_tools import FileTools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BedrockAgent:
    """AWS Bedrock Agent with function calling capabilities"""
    
    def __init__(self, aws_region: str = "us-east-1", model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0"):
        """
        Initialize the Bedrock Agent
        
        Args:
            aws_region: AWS region for Bedrock
            model_id: Bedrock model ID (default: Claude 3.5 Sonnet)
        """
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=aws_region
        )
        self.model_id = model_id
        self.file_tools = FileTools()
        self.conversation_history = []
        self.available_files = []
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        
    def set_available_files(self, files: List[str]):
        """
        Set the list of available files for the agent
        
        Args:
            files: List of file paths
        """
        self.available_files = files
        logger.info(f"Agent has access to {len(files)} files")
    
    def get_tools_definition(self) -> List[Dict[str, Any]]:
        """
        Get Bedrock tool definitions (function calling)
        
        Returns:
            List of tool definitions in Bedrock format
        """
        return [
            {
                "toolSpec": {
                    "name": "read_excel",
                    "description": "Read an Excel file and get information about its structure, columns, data types, sample data, and summary statistics",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Path to the Excel file"
                                },
                                "sheet_name": {
                                    "type": "string",
                                    "description": "Name of the sheet to read (optional)"
                                },
                                "max_rows": {
                                    "type": "integer",
                                    "description": "Maximum number of rows to read (optional)"
                                }
                            },
                            "required": ["file_path"]
                        }
                    }
                }
            },
            {
                "toolSpec": {
                    "name": "query_excel",
                    "description": "Query an Excel file using pandas query syntax to filter data based on conditions",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Path to the Excel file"
                                },
                                "query": {
                                    "type": "string",
                                    "description": "Pandas query string (e.g., 'age > 25 and city == \"New York\"')"
                                },
                                "sheet_name": {
                                    "type": "string",
                                    "description": "Name of the sheet to query (optional)"
                                }
                            },
                            "required": ["file_path", "query"]
                        }
                    }
                }
            },
            {
                "toolSpec": {
                    "name": "get_excel_column_values",
                    "description": "Get all values from a specific column in an Excel file",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Path to the Excel file"
                                },
                                "column_name": {
                                    "type": "string",
                                    "description": "Name of the column"
                                },
                                "sheet_name": {
                                    "type": "string",
                                    "description": "Name of the sheet (optional)"
                                },
                                "unique": {
                                    "type": "boolean",
                                    "description": "Whether to return only unique values"
                                }
                            },
                            "required": ["file_path", "column_name"]
                        }
                    }
                }
            },
            {
                "toolSpec": {
                    "name": "list_available_files",
                    "description": "List all files available from the S3 bucket",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                }
            }
        ]
    
    def execute_function(self, function_name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute a function call
        
        Args:
            function_name: Name of the function to execute
            arguments: Function arguments
            
        Returns:
            Function result as JSON string
        """
        try:
            if function_name == "read_excel":
                result = self.file_tools.read_excel(**arguments)
            elif function_name == "query_excel":
                result = self.file_tools.query_excel(**arguments)
            elif function_name == "get_excel_column_values":
                result = self.file_tools.get_excel_column_values(**arguments)
            elif function_name == "list_available_files":
                result = {
                    "success": True,
                    "files": self.available_files,
                    "num_files": len(self.available_files)
                }
            else:
                result = {"success": False, "error": f"Unknown function: {function_name}"}
            
            logger.info(f"Executed function: {function_name}")
            return json.dumps(result, default=str)
        except Exception as e:
            logger.error(f"Error executing function {function_name}: {str(e)}")
            return json.dumps({"success": False, "error": str(e)})
    
    def chat(self, user_message: str, max_iterations: int = 10) -> str:
        """
        Chat with the Bedrock agent, allowing multiple function calls if needed
        
        Args:
            user_message: User's question or message
            max_iterations: Maximum number of function calling iterations
            
        Returns:
            Agent's response
        """
        # Add system message on first interaction
        if not self.conversation_history:
            system_prompt = [{
                "text": f"""You are a medical data analysis assistant specializing in Doppler ultrasound studies. 
You have access to Excel files containing Doppler study records from an S3 bucket.

CONTEXT:
- The data contains Doppler ultrasound examination records
- This is medical diagnostic data that may include patient information, study dates, results, and findings
- Data is from July-August 2025 period

Available files: {', '.join(self.available_files)}

YOUR CAPABILITIES:
- Read and analyze Excel files with multiple sheets
- Filter and query data based on specific criteria
- Extract statistics and summaries
- Identify patterns and trends in the medical data

INSTRUCTIONS:
1. First, explore the data structure to understand what columns and information are available
2. Use the appropriate tools to find the requested information
3. Provide clear, accurate answers based on the actual data
4. When analyzing medical data, be precise and professional
5. If asked to calculate statistics or aggregations, explain your methodology
6. Always specify which data you're analyzing (e.g., "Based on the 150 records in the file...")

IMPORTANT: Treat all data as confidential medical information. Focus on data analysis, not medical advice.
"""
            }]
        else:
            system_prompt = None
        
        # Build messages for Converse API
        # For now, start fresh with each query to avoid conversation history issues
        # This ensures we always start with a user message
        messages = [{
            "role": "user",
            "content": [{"text": user_message}]
        }]
        
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            
            # Call Bedrock Converse API
            request_params = {
                "modelId": self.model_id,
                "messages": messages,
                "toolConfig": {
                    "tools": self.get_tools_definition()
                }
            }
            
            if system_prompt:
                request_params["system"] = system_prompt
            
            response = self.bedrock.converse(**request_params)
            
            # Track token usage
            if 'usage' in response:
                self.total_input_tokens += response['usage'].get('inputTokens', 0)
                self.total_output_tokens += response['usage'].get('outputTokens', 0)
                logger.info(f"Tokens - Input: {response['usage'].get('inputTokens', 0)}, "
                          f"Output: {response['usage'].get('outputTokens', 0)}, "
                          f"Total: {response['usage'].get('totalTokens', 0)}")
            
            output_message = response['output']['message']
            
            # Add assistant message to conversation
            messages.append(output_message)
            
            # Check stop reason
            stop_reason = response.get('stopReason')
            
            if stop_reason == 'end_turn':
                # No tool use, return the text response
                text_response = ""
                for content in output_message['content']:
                    if 'text' in content:
                        text_response = content['text']
                
                if text_response:
                    # Don't save to conversation_history for now to avoid API conflicts
                    # Each query starts fresh with system prompt context
                    return text_response
                return "I couldn't generate a response."
            
            elif stop_reason == 'tool_use':
                # Process tool calls
                tool_results = []
                
                for content in output_message['content']:
                    if 'toolUse' in content:
                        tool_use = content['toolUse']
                        tool_name = tool_use['name']
                        tool_input = tool_use['input']
                        tool_use_id = tool_use['toolUseId']
                        
                        logger.info(f"Calling tool: {tool_name} with input: {tool_input}")
                        
                        # Execute the function
                        function_response = self.execute_function(tool_name, tool_input)
                        
                        # Add tool result
                        tool_results.append({
                            "toolResult": {
                                "toolUseId": tool_use_id,
                                "content": [{"text": function_response}]
                            }
                        })
                
                # Add tool results to messages
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
                
                # Continue loop to get final response
                continue
            
            elif stop_reason == 'max_tokens':
                # Max tokens reached
                text_response = ""
                for content in output_message['content']:
                    if 'text' in content:
                        text_response = content['text']
                return text_response or "Response was cut off due to length. Please ask a more specific question."
            
            else:
                # Other stop reasons
                logger.warning(f"Unexpected stop reason: {stop_reason}")
                return f"Conversation stopped: {stop_reason}"
        
        # Max iterations reached - still return any partial response
        logger.warning(f"Max iterations ({max_iterations}) reached")
        return "I've made multiple tool calls but need to continue. Please ask your question again or rephrase it."
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        logger.info("Conversation history reset")
    
    def get_token_usage(self) -> dict:
        """
        Get token usage statistics
        
        Returns:
            Dictionary with token usage information
        """
        # Bedrock Cohere Command R+ pricing (as of 2024)
        # Cohere Command R+: Input $3.00/1M, Output $15.00/1M
        input_cost = (self.total_input_tokens / 1_000_000) * 3.00
        output_cost = (self.total_output_tokens / 1_000_000) * 15.00
        total_cost = input_cost + output_cost
        
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "estimated_cost_usd": round(total_cost, 4),
            "input_cost_usd": round(input_cost, 4),
            "output_cost_usd": round(output_cost, 4)
        }


