"""
File Processing Tools
Tools for reading and analyzing Excel, CSV and JSON files
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileTools:
    """Tools for processing Excel, CSV and JSON files"""
    
    @staticmethod
    def read_excel(file_path: str, sheet_name: Optional[str] = None, max_rows: Optional[int] = None) -> Dict[str, Any]:
        """
        Read Excel file and return information about it
        
        Args:
            file_path: Path to Excel file
            sheet_name: Name of the sheet to read (None for first sheet)
            max_rows: Maximum number of rows to read (None for all)
            
        Returns:
            Dictionary with Excel information
        """
        try:
            # Get all sheet names
            excel_file = pd.ExcelFile(file_path)
            all_sheets = excel_file.sheet_names
            
            # Read the specified sheet or the first one
            if sheet_name is None:
                sheet_name = all_sheets[0]
            
            df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=max_rows)
            
            result = {
                "success": True,
                "file_path": file_path,
                "sheet_name": sheet_name,
                "all_sheets": all_sheets,
                "num_rows": len(df),
                "num_columns": len(df.columns),
                "columns": df.columns.tolist(),
                "data_types": df.dtypes.astype(str).to_dict(),
                "sample_data": df.head(5).to_dict(orient='records'),
                "summary_stats": df.describe().to_dict() if not df.empty else {}
            }
            
            logger.info(f"Successfully read Excel file: {file_path}, sheet: {sheet_name}")
            return result
        except Exception as e:
            logger.error(f"Error reading Excel file {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
    
    @staticmethod
    def query_excel(file_path: str, query: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Query Excel file using pandas query syntax
        
        Args:
            file_path: Path to Excel file
            query: Pandas query string (e.g., "age > 25 and city == 'New York'")
            sheet_name: Name of the sheet to query (None for first sheet)
            
        Returns:
            Dictionary with query results
        """
        try:
            if sheet_name is None:
                excel_file = pd.ExcelFile(file_path)
                sheet_name = excel_file.sheet_names[0]
            
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            result_df = df.query(query)
            
            return {
                "success": True,
                "file_path": file_path,
                "sheet_name": sheet_name,
                "query": query,
                "num_results": len(result_df),
                "results": result_df.to_dict(orient='records')
            }
        except Exception as e:
            logger.error(f"Error querying Excel file {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path,
                "query": query
            }
    
    @staticmethod
    def get_excel_column_values(file_path: str, column_name: str, sheet_name: Optional[str] = None, unique: bool = False) -> Dict[str, Any]:
        """
        Get values from a specific column in Excel
        
        Args:
            file_path: Path to Excel file
            column_name: Name of the column
            sheet_name: Name of the sheet (None for first sheet)
            unique: Whether to return only unique values
            
        Returns:
            Dictionary with column values
        """
        try:
            if sheet_name is None:
                excel_file = pd.ExcelFile(file_path)
                sheet_name = excel_file.sheet_names[0]
            
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            if column_name not in df.columns:
                return {
                    "success": False,
                    "error": f"Column '{column_name}' not found",
                    "available_columns": df.columns.tolist()
                }
            
            values = df[column_name].tolist()
            if unique:
                values = df[column_name].unique().tolist()
            
            return {
                "success": True,
                "file_path": file_path,
                "sheet_name": sheet_name,
                "column_name": column_name,
                "num_values": len(values),
                "values": values
            }
        except Exception as e:
            logger.error(f"Error getting column values from {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
    
    @staticmethod
    def read_csv(file_path: str, max_rows: Optional[int] = None) -> Dict[str, Any]:
        """
        Read CSV file and return information about it
        
        Args:
            file_path: Path to CSV file
            max_rows: Maximum number of rows to read (None for all)
            
        Returns:
            Dictionary with CSV information
        """
        try:
            df = pd.read_csv(file_path, nrows=max_rows)
            
            result = {
                "success": True,
                "file_path": file_path,
                "num_rows": len(df),
                "num_columns": len(df.columns),
                "columns": df.columns.tolist(),
                "data_types": df.dtypes.astype(str).to_dict(),
                "sample_data": df.head(5).to_dict(orient='records'),
                "summary_stats": df.describe().to_dict() if not df.empty else {}
            }
            
            logger.info(f"Successfully read CSV file: {file_path}")
            return result
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
    
    @staticmethod
    def query_csv(file_path: str, query: str) -> Dict[str, Any]:
        """
        Query CSV file using pandas query syntax
        
        Args:
            file_path: Path to CSV file
            query: Pandas query string (e.g., "age > 25 and city == 'New York'")
            
        Returns:
            Dictionary with query results
        """
        try:
            df = pd.read_csv(file_path)
            result_df = df.query(query)
            
            return {
                "success": True,
                "file_path": file_path,
                "query": query,
                "num_results": len(result_df),
                "results": result_df.to_dict(orient='records')
            }
        except Exception as e:
            logger.error(f"Error querying CSV file {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path,
                "query": query
            }
    
    @staticmethod
    def get_csv_column_values(file_path: str, column_name: str, unique: bool = False) -> Dict[str, Any]:
        """
        Get values from a specific column in CSV
        
        Args:
            file_path: Path to CSV file
            column_name: Name of the column
            unique: Whether to return only unique values
            
        Returns:
            Dictionary with column values
        """
        try:
            df = pd.read_csv(file_path)
            
            if column_name not in df.columns:
                return {
                    "success": False,
                    "error": f"Column '{column_name}' not found",
                    "available_columns": df.columns.tolist()
                }
            
            values = df[column_name].tolist()
            if unique:
                values = df[column_name].unique().tolist()
            
            return {
                "success": True,
                "file_path": file_path,
                "column_name": column_name,
                "num_values": len(values),
                "values": values
            }
        except Exception as e:
            logger.error(f"Error getting column values from {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
    
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """
        Read JSON file and return its content
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Dictionary with JSON content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            result = {
                "success": True,
                "file_path": file_path,
                "data": data,
                "data_type": type(data).__name__,
            }
            
            # Add additional info based on data type
            if isinstance(data, list):
                result["num_items"] = len(data)
                if data and isinstance(data[0], dict):
                    result["sample_keys"] = list(data[0].keys())
            elif isinstance(data, dict):
                result["keys"] = list(data.keys())
            
            logger.info(f"Successfully read JSON file: {file_path}")
            return result
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }
    
    @staticmethod
    def search_json(file_path: str, search_key: str) -> Dict[str, Any]:
        """
        Search for a specific key in JSON data
        
        Args:
            file_path: Path to JSON file
            search_key: Key to search for
            
        Returns:
            Dictionary with search results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            def find_key(obj, key, path=""):
                """Recursively find all occurrences of a key"""
                results = []
                
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        new_path = f"{path}.{k}" if path else k
                        if k == key:
                            results.append({"path": new_path, "value": v})
                        results.extend(find_key(v, key, new_path))
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        new_path = f"{path}[{i}]"
                        results.extend(find_key(item, key, new_path))
                
                return results
            
            results = find_key(data, search_key)
            
            return {
                "success": True,
                "file_path": file_path,
                "search_key": search_key,
                "num_occurrences": len(results),
                "results": results
            }
        except Exception as e:
            logger.error(f"Error searching JSON file {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "file_path": file_path
            }

