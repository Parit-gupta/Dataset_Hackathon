import pandas as pd
import json

def query_dataset(dataframe, question):
    """
    Main function that processes questions about the dataset using RAG approach.
    
    Args:
        dataframe: pandas DataFrame containing the uploaded dataset
        question: user's question as a string
    
    Returns:
        answer: string response to the user's question
    """
    
    try:
        # Convert question to lowercase for easier matching
        q_lower = question.lower()
        
        # Get dataset information
        dataset_info = get_dataset_summary(dataframe)
        
        # Route to appropriate handler based on question type
        if any(word in q_lower for word in ['column', 'columns', 'fields', 'features']):
            return handle_column_questions(dataframe, question)
        
        elif any(word in q_lower for word in ['row', 'rows', 'records', 'entries', 'how many', 'count']):
            return handle_row_questions(dataframe, question)
        
        elif any(word in q_lower for word in ['top', 'bottom', 'first', 'last', 'show', 'display']):
            return handle_display_questions(dataframe, question)
        
        elif any(word in q_lower for word in ['mean', 'average', 'median', 'sum', 'max', 'min', 'statistics', 'stats']):
            return handle_statistics_questions(dataframe, question)
        
        elif any(word in q_lower for word in ['null', 'missing', 'nan', 'empty']):
            return handle_missing_data_questions(dataframe, question)
        
        elif any(word in q_lower for word in ['unique', 'distinct', 'different']):
            return handle_unique_questions(dataframe, question)
        
        elif any(word in q_lower for word in ['type', 'dtype', 'data type']):
            return handle_datatype_questions(dataframe, question)
        
        elif any(word in q_lower for word in ['correlat', 'relationship']):
            return handle_correlation_questions(dataframe, question)
        
        else:
            # General query - provide dataset overview
            return f"""Based on your dataset:

{dataset_info}

I can help you with:
• Statistical analysis (mean, median, max, min)
• Missing data analysis
• Column information
• Top/bottom records
• Unique values
• Correlations

Please ask a specific question about your data!"""
    
    except Exception as e:
        return f"Error processing your question: {str(e)}\n\nPlease try rephrasing your question."


def get_dataset_summary(df):
    """Generate a summary of the dataset"""
    summary = f"""
📊 **Dataset Overview:**
- Total Rows: {len(df)}
- Total Columns: {len(df.columns)}
- Columns: {', '.join(df.columns.tolist())}
- Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
"""
    return summary


def handle_column_questions(df, question):
    """Handle questions about columns"""
    columns = df.columns.tolist()
    
    return f"""**Column Information:**

Total Columns: {len(columns)}

Column Names:
{chr(10).join([f"• {col}" for col in columns])}

Column Data Types:
{chr(10).join([f"• {col}: {df[col].dtype}" for col in columns])}
"""


def handle_row_questions(df, question):
    """Handle questions about rows/records"""
    return f"""**Row Information:**

Total number of rows: **{len(df)}**
Total number of columns: **{len(df.columns)}**

First few rows:
{df.head().to_string()}
"""


def handle_display_questions(df, question):
    """Handle display requests like 'show top 5', 'show bottom 10'"""
    q_lower = question.lower()
    
    # Extract number if present
    import re
    numbers = re.findall(r'\d+', question)
    n = int(numbers[0]) if numbers else 5
    
    if 'bottom' in q_lower or 'last' in q_lower:
        result = df.tail(n)
        return f"**Bottom {n} records:**\n\n{result.to_string()}"
    else:
        result = df.head(n)
        return f"**Top {n} records:**\n\n{result.to_string()}"


def handle_statistics_questions(df, question):
    """Handle statistical questions"""
    q_lower = question.lower()
    
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if not numeric_cols:
        return "No numeric columns found in the dataset for statistical analysis."
    
    stats = df[numeric_cols].describe()
    
    if 'mean' in q_lower or 'average' in q_lower:
        means = df[numeric_cols].mean()
        return f"**Mean Values:**\n\n{means.to_string()}"
    
    elif 'median' in q_lower:
        medians = df[numeric_cols].median()
        return f"**Median Values:**\n\n{medians.to_string()}"
    
    elif 'max' in q_lower or 'maximum' in q_lower:
        maxs = df[numeric_cols].max()
        return f"**Maximum Values:**\n\n{maxs.to_string()}"
    
    elif 'min' in q_lower or 'minimum' in q_lower:
        mins = df[numeric_cols].min()
        return f"**Minimum Values:**\n\n{mins.to_string()}"
    
    elif 'sum' in q_lower:
        sums = df[numeric_cols].sum()
        return f"**Sum of Values:**\n\n{sums.to_string()}"
    
    else:
        return f"**Statistical Summary:**\n\n{stats.to_string()}"


def handle_missing_data_questions(df, question):
    """Handle questions about missing data"""
    missing = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df)) * 100
    
    missing_info = pd.DataFrame({
        'Missing Count': missing,
        'Percentage': missing_percent
    })
    
    missing_info = missing_info[missing_info['Missing Count'] > 0]
    
    if len(missing_info) == 0:
        return "✅ No missing values found in the dataset!"
    
    return f"""**Missing Data Analysis:**

{missing_info.to_string()}

Total missing values: {missing.sum()}
"""


def handle_unique_questions(df, question):
    """Handle questions about unique values"""
    unique_counts = df.nunique()
    
    return f"""**Unique Value Counts:**

{unique_counts.to_string()}

Columns with all unique values:
{', '.join([col for col in df.columns if df[col].nunique() == len(df)])}
"""


def handle_datatype_questions(df, question):
    """Handle questions about data types"""
    dtypes = df.dtypes
    
    type_counts = dtypes.value_counts()
    
    return f"""**Data Type Information:**

{dtypes.to_string()}

---

**Type Summary:**
{type_counts.to_string()}
"""


def handle_correlation_questions(df, question):
    """Handle correlation questions"""
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 2:
        return "Need at least 2 numeric columns to calculate correlations."
    
    corr = df[numeric_cols].corr()
    
    return f"""**Correlation Matrix:**

{corr.to_string()}

💡 Values close to 1 or -1 indicate strong correlation.
"""