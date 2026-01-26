"""
Utility functions for the portal application.
"""
import pandas as pd
from io import BytesIO
from .models import Record


def import_excel_data(file, tab, user):
    """
    Process and import Excel file data into Record objects.
    
    Purpose:
    - Read .xlsx/.xls files using pandas
    - Auto-generate S.No (serial number) column
    - Convert dataframe rows to Record JSONField format
    - Create database records with creator tracking
    
    Parameters:
        file: Django UploadedFile object from form submission
        tab: Tab object (destination for imported data)
        user: User object (creator tracking)
    
    Process:
    1. Read Excel file into pandas DataFrame
    2. Iterate through each row
    3. Add S.No column (1-indexed serial numbering)
    4. Handle NaN values and type conversions
    5. Create Record with data JSONField
    6. Return count of imported records
    
    Returns:
        int: Number of records successfully imported
    
    Raises:
        Exception: If Excel read fails or record creation fails
    """
    try:
        # Read Excel file into DataFrame
        # BytesIO converts uploaded file to in-memory bytes for pandas
        file_bytes = BytesIO(file.read())
        df = pd.read_excel(file_bytes)
        
        # Track count of successfully created records
        records_created = 0
        
        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            # Initialize data dictionary for this row
            data = {}
            
            # Add S.No field: Serial number starting from 1
            # This matches Excel row numbering (excluding header)
            data['S.No'] = index + 1
            
            # Convert each column value to appropriate type
            for col, value in row.items():
                if pd.isna(value):
                    # Handle missing/null values
                    data[col] = None
                elif isinstance(value, (int, float)):
                    # Keep numeric values as-is
                    data[col] = value
                else:
                    # Convert all other types to string
                    data[col] = str(value)
            
            # Create Record object with JSONField data
            # Stores row data as JSON, tracks creator and timestamps
            record = Record.objects.create(
                tab=tab,
                data=data,
                created_by=user
            )
            records_created += 1
        
        return records_created
        
    except Exception as e:
        raise Exception(f"Failed to import Excel data: {str(e)}")
