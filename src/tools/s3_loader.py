"""
S3 Data Loader Module
Handles downloading and caching files from AWS S3 bucket
"""

import os
import boto3
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3DataLoader:
    """Load data from S3 bucket"""
    
    def __init__(self, bucket_name: str, aws_access_key_id: str, 
                 aws_secret_access_key: str, region_name: str = 'us-east-1'):
        """
        Initialize S3 client
        
        Args:
            bucket_name: Name of the S3 bucket
            aws_access_key_id: AWS access key
            aws_secret_access_key: AWS secret key
            region_name: AWS region
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.local_cache_dir = 'data'
        os.makedirs(self.local_cache_dir, exist_ok=True)
        
    def list_files(self, prefix: str = '') -> List[str]:
        """
        List all files in the S3 bucket
        
        Args:
            prefix: Optional prefix to filter files
            
        Returns:
            List of file keys in the bucket
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            if 'Contents' not in response:
                logger.warning(f"No files found in bucket {self.bucket_name}")
                return []
            
            files = [obj['Key'] for obj in response['Contents']]
            logger.info(f"Found {len(files)} files in bucket")
            return files
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return []
    
    def download_file(self, file_key: str) -> Optional[str]:
        """
        Download a file from S3 to local cache
        
        Args:
            file_key: S3 object key
            
        Returns:
            Local file path if successful, None otherwise
        """
        try:
            local_path = os.path.join(self.local_cache_dir, os.path.basename(file_key))
            
            # Check if file already exists locally
            if os.path.exists(local_path):
                logger.info(f"File {file_key} already cached locally")
                return local_path
            
            # Download from S3
            self.s3_client.download_file(self.bucket_name, file_key, local_path)
            logger.info(f"Downloaded {file_key} to {local_path}")
            return local_path
        except Exception as e:
            logger.error(f"Error downloading file {file_key}: {str(e)}")
            return None
    
    def download_all_files(self, prefix: str = '') -> List[str]:
        """
        Download all files from S3 bucket
        
        Args:
            prefix: Optional prefix to filter files
            
        Returns:
            List of local file paths
        """
        files = self.list_files(prefix)
        local_paths = []
        
        for file_key in files:
            local_path = self.download_file(file_key)
            if local_path:
                local_paths.append(local_path)
        
        return local_paths
    
    def get_file_content(self, file_key: str) -> Optional[bytes]:
        """
        Get file content directly from S3 without downloading
        
        Args:
            file_key: S3 object key
            
        Returns:
            File content as bytes if successful, None otherwise
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
            content = response['Body'].read()
            logger.info(f"Retrieved content for {file_key}")
            return content
        except Exception as e:
            logger.error(f"Error getting file content {file_key}: {str(e)}")
            return None

