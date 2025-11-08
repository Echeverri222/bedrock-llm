"""
LLM Agent with OpenAI Function Calling
Handles questions about data using tools
"""

from openai import OpenAI
import httpx
from typing import List, Dict, Any, Optional
import json
import logging
from file_tools import FileTools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMAgent:
    """OpenAI Agent with function calling capabilities"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize the LLM Agent
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o-mini)
        """
        import os
        # Set API key in environment as well
        os.environ["OPENAI_API_KEY"] = api_key
        # Create custom httpx client without proxy support
        http_client = httpx.Client(
            timeout=60.0,
            follow_redirects=True
        )
        # Initialize client with custom http client
        self.client = OpenAI(
            api_key=api_key,
            http_client=http_client,
            max_retries=3
        )
        self.model = model
        self.file_tools = FileTools()
        self.conversation_history = []
        self.available_files = []
        self.total_tokens_used = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        
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
        Get OpenAI function calling tool definitions
        
        Returns:
            List of tool definitions
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "read_excel",
                    "description": "Read an Excel file and get information about its structure, columns, data types, sample data, and summary statistics",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the Excel file"
                            },
                            "sheet_name": {
                                "type": "string",
                                "description": "Name of the sheet to read (optional, reads first sheet if not specified)"
                            },
                            "max_rows": {
                                "type": "integer",
                                "description": "Maximum number of rows to read (optional)"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "query_excel",
                    "description": "Query an Excel file using pandas query syntax. Use this to filter data based on conditions.",
                    "parameters": {
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
            },
            {
                "type": "function",
                "function": {
                    "name": "get_excel_column_values",
                    "description": "Get all values from a specific column in an Excel file",
                    "parameters": {
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
                                "description": "Whether to return only unique values (optional, default false)"
                            }
                        },
                        "required": ["file_path", "column_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_json",
                    "description": "Read a JSON file and get its content and structure",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the JSON file"
                            }
                        },
                        "required": ["file_path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_json",
                    "description": "Search for a specific key in a JSON file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the JSON file"
                            },
                            "search_key": {
                                "type": "string",
                                "description": "Key to search for in the JSON"
                            }
                        },
                        "required": ["file_path", "search_key"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_available_files",
                    "description": "List all files available from the S3 bucket",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
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
            elif function_name == "read_json":
                result = self.file_tools.read_json(**arguments)
            elif function_name == "search_json":
                result = self.file_tools.search_json(**arguments)
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
    
    def chat(self, user_message: str, max_iterations: int = 5) -> str:
        """
        Chat with the agent, allowing multiple function calls if needed
        
        Args:
            user_message: User's question or message
            max_iterations: Maximum number of function calling iterations
            
        Returns:
            Agent's response
        """
        # Add system message on first interaction
        if not self.conversation_history:
            system_message = {
                "role": "system",
                "content": f"""You are a medical data analysis assistant specializing in Doppler ultrasound studies. 
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
            }
            self.conversation_history.append(system_message)
        
        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=self.get_tools_definition(),
                tool_choice="auto"
            )
            
            # Track token usage
            if hasattr(response, 'usage') and response.usage:
                self.total_prompt_tokens += response.usage.prompt_tokens
                self.total_completion_tokens += response.usage.completion_tokens
                self.total_tokens_used += response.usage.total_tokens
                logger.info(f"Tokens used - Prompt: {response.usage.prompt_tokens}, "
                          f"Completion: {response.usage.completion_tokens}, "
                          f"Total this request: {response.usage.total_tokens}")
            
            assistant_message = response.choices[0].message
            
            # Add assistant message to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": assistant_message.tool_calls
            })
            
            # Check if there are tool calls
            if not assistant_message.tool_calls:
                # No more tool calls, return the response
                return assistant_message.content or "I couldn't find an answer to your question."
            
            # Execute tool calls
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                logger.info(f"Calling function: {function_name} with args: {function_args}")
                
                # Execute the function
                function_response = self.execute_function(function_name, function_args)
                
                # Add function response to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": function_response
                })
        
        # If we've reached max iterations, make one final call without tools
        final_response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history
        )
        
        # Track final call tokens
        if hasattr(final_response, 'usage') and final_response.usage:
            self.total_prompt_tokens += final_response.usage.prompt_tokens
            self.total_completion_tokens += final_response.usage.completion_tokens
            self.total_tokens_used += final_response.usage.total_tokens
            logger.info(f"Tokens used - Prompt: {final_response.usage.prompt_tokens}, "
                      f"Completion: {final_response.usage.completion_tokens}, "
                      f"Total this request: {final_response.usage.total_tokens}")
        
        return final_response.choices[0].message.content or "I've analyzed the data but couldn't formulate a final answer."
    
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
        # Estimated cost for gpt-4o-mini (as of 2024)
        # Input: $0.150 per 1M tokens, Output: $0.600 per 1M tokens
        input_cost = (self.total_prompt_tokens / 1_000_000) * 0.150
        output_cost = (self.total_completion_tokens / 1_000_000) * 0.600
        total_cost = input_cost + output_cost
        
        return {
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_tokens_used,
            "estimated_cost_usd": round(total_cost, 4),
            "input_cost_usd": round(input_cost, 4),
            "output_cost_usd": round(output_cost, 4)
        }

