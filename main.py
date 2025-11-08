"""
Main Application Entry Point
LLM Agent that analyzes data from S3 bucket
"""

import os
from dotenv import load_dotenv
from s3_loader import S3DataLoader
from bedrock_agent import BedrockAgent
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main application function"""
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    s3_bucket_name = os.getenv('S3_BUCKET_NAME')
    bedrock_region = os.getenv('BEDROCK_REGION', 'us-east-1')
    bedrock_model = os.getenv('BEDROCK_MODEL', 'cohere.command-r-plus-v1:0')
    
    # Validate configuration
    if not all([aws_access_key_id, aws_secret_access_key, s3_bucket_name]):
        logger.error("Missing required environment variables. Please check your .env file.")
        logger.error("Required: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME")
        return
    
    logger.info("Starting AWS Bedrock Data Analysis Agent")
    logger.info(f"S3 Bucket: {s3_bucket_name}")
    logger.info(f"AWS Region: {aws_region}")
    logger.info(f"Bedrock Model: {bedrock_model}")
    
    # Initialize S3 Loader
    try:
        s3_loader = S3DataLoader(
            bucket_name=s3_bucket_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        logger.info("✓ S3 connection established")
    except Exception as e:
        logger.error(f"Failed to connect to S3: {str(e)}")
        return
    
    # Download files from S3
    try:
        logger.info("Downloading files from S3 bucket...")
        local_files = s3_loader.download_all_files()
        
        if not local_files:
            logger.error("No files found in the S3 bucket")
            return
        
        logger.info(f"✓ Downloaded {len(local_files)} file(s):")
        for file_path in local_files:
            logger.info(f"  - {file_path}")
    except Exception as e:
        logger.error(f"Failed to download files: {str(e)}")
        return
    
    # Initialize Bedrock Agent
    try:
        agent = BedrockAgent(aws_region=bedrock_region, model_id=bedrock_model)
        agent.set_available_files(local_files)
        logger.info("✓ Bedrock Agent initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Bedrock Agent: {str(e)}")
        return
    
    # Interactive chat loop
    print("\n" + "="*60)
    print("AWS BEDROCK DATA ANALYSIS AGENT (Cohere)")
    print("="*60)
    print(f"\nFiles loaded: {len(local_files)}")
    for file_path in local_files:
        print(f"  • {os.path.basename(file_path)}")
    print("\nYou can now ask questions about the data!")
    print("Commands:")
    print("  - Type your question to get answers")
    print("  - Type 'reset' to clear conversation history")
    print("  - Type 'quit' or 'exit' to end the session")
    print("="*60 + "\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for special commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                usage = agent.get_token_usage()
                print(f"\n📊 Final Session Summary:")
                print(f"  Total tokens used: {usage['total_tokens']:,}")
                print(f"  Input tokens: {usage['input_tokens']:,}")
                print(f"  Output tokens: {usage['output_tokens']:,}")
                print(f"  Total cost: ${usage['estimated_cost_usd']:.4f}")
                print("\nThank you for using AWS Bedrock Data Analysis Agent. Goodbye!")
                break
            
            if user_input.lower() == 'reset':
                usage = agent.get_token_usage()
                print(f"\n📊 Session Summary:")
                print(f"  Total tokens used: {usage['total_tokens']:,}")
                print(f"  Total cost: ${usage['estimated_cost_usd']:.4f}")
                agent.reset_conversation()
                print("\n✓ Conversation history cleared.\n")
                continue
            
            # Get response from agent
            print("\nAgent: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            
            # Display token usage
            usage = agent.get_token_usage()
            print(f"\n💰 Tokens: {usage['total_tokens']:,} | Cost: ${usage['estimated_cost_usd']:.4f}\n")
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error during chat: {str(e)}")
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == "__main__":
    main()

