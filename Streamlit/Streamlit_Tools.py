from langchain.tools import Tool
from streamlit_Csv import CSVHandler, parse_kv_string


SYSTEM_PROMPT = """You are an AI CSV assistant that helps users manage their CSV data.
You can perform the following operations:
1. View information about the CSV including columns and a preview
2. Remove rows or columns
3. Add new rows or columns
4. Set values for specific cells or entire rows"""

def create_tools(csv_handler):
    tools = [
        Tool.from_function(
            name="GetCSVInfo",
            func=lambda _: csv_handler.get_csv_info(),
            description="Gets information about the CSV file including column names, number of rows, and a preview."
        ),

        Tool.from_function(
            name="RemoveColumn",
            func=lambda input_str: csv_handler.remove_column(input_str.strip()),
            description="Removes a column. Input is the column name (string)."
        ),

        Tool.from_function(
            name="RemoveRow",
            func=lambda input_str: csv_handler.remove_row(input_str.strip()),
            description="Removes a row. Input can be a row index (integer) or special values like 'last' or 'first'."
        ),

        Tool.from_function(
            name="AddColumn",
            func=lambda input_str: csv_handler.add_column(input_str),
            description="Adds a new column. Input should be column name with optional default values (e.g., 'salary with values=50000')."
        ),

        Tool.from_function(
            name="AddRow",
            func=lambda input_str: csv_handler.add_row(parse_kv_string(input_str)),
            description="Adds a new row. Input is key=value pairs like 'name=John, age=30'. Keys must match column names."
        ),

        Tool.from_function(
            name="SetCellValue",
            func=lambda input_str: (
                lambda parts: csv_handler.set_cell(parts[0].strip(), parts[1].strip(), parts[2].strip())
            )(input_str.split(",", 2)),
            description="Sets a specific cell. Input: 'row_index/first/last, column_name, value'. Row can be numeric index or 'first'/'last'."
        ),

        Tool.from_function(
            name="SetRow",
            func=lambda input_str: (
                lambda i, kv: csv_handler.set_row(i.strip(), parse_kv_string(kv))
            )(*input_str.split(":", 1)),
            description="Sets an entire row. Input: 'row_index/first/last: key=value, key2=value2'. Row can be numeric or 'first'/'last'."
        ),
    ]
    
    return tools