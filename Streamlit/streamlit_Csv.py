import os
import pandas as pd

class CSVHandler:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = pd.DataFrame()
        self._load_csv()
        
    def _load_csv(self):
        try:
            self.df = pd.read_csv(self.csv_path)
        except:
            self.df = pd.DataFrame()

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
            self.df.to_csv(self.csv_path, index=False)
        except:
            pass

    def get_column_names(self):
        return list(self.df.columns)
        
    def get_csv_info(self):
        return f"CSV has {len(self.df)} rows and columns: {', '.join(self.get_column_names())}\nPreview:\n{self.df.head(3).to_string()}"

    def remove_column(self, column_name: str):
        column_match = next((col for col in self.df.columns if col.lower() == column_name.lower()), None)
        if not column_match:
            return f"Column '{column_name}' does not exist. Available columns: {', '.join(self.df.columns)}"
        
        self.df.drop(columns=[column_match], inplace=True)
        self.save()
        return f"Column '{column_match}' removed."

    def remove_row(self, index_or_desc: str):
        try:
            if index_or_desc.lower() == "first":
                index = 0
            elif index_or_desc.lower() == "last":
                index = len(self.df) - 1
            else:
                index = int(index_or_desc)
            
            if index < 0 or index >= len(self.df):
                return f"Row index {index} is out of bounds. CSV has {len(self.df)} rows."
            
            self.df.drop(index=self.df.index[index], inplace=True)
            self.save()
            return f"Row {index} removed."
        except ValueError:
            return f"Invalid row specifier: '{index_or_desc}'. Use a number or 'first'/'last'."

    def add_column(self, input_str: str):
        parts = [part.strip() for part in input_str.split("with")]
        column_name = parts[0].strip()
        
        if column_name in self.df.columns:
            return f"Column '{column_name}' already exists."
        
        default_value = ""
        if len(parts) > 1 and "values" in parts[1]:
            default_value = parts[1].split("=")[1].strip()
        
        self.df[column_name] = default_value
        self.save()
        return f"Column '{column_name}' added with default value: '{default_value}'."

    def add_row(self, row_dict: dict):
        missing_cols = [col for col in row_dict if col not in self.df.columns]
        if missing_cols:
            return f"Columns not in CSV: {', '.join(missing_cols)}. Available columns: {', '.join(self.df.columns)}"
        
        new_row = {col: row_dict.get(col, "") for col in self.df.columns}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.save()
        return f"Row added: {new_row}"

    def set_cell(self, row_spec, column_name, value):
        try:
            row_idx = {"first": 0, "last": len(self.df) - 1}.get(row_spec.lower(), int(row_spec))
            
            if row_idx < 0 or row_idx >= len(self.df):
                return f"Row index {row_idx} is out of bounds. CSV has {len(self.df)} rows."
            
            if column_name not in self.df.columns:
                return f"Column '{column_name}' does not exist. Available columns: {', '.join(self.df.columns)}"
            
            self.df.at[self.df.index[row_idx], column_name] = value
            self.save()
            return f"Value set at row {row_idx}, column '{column_name}' to '{value}'."
        except ValueError:
            return f"Invalid row specifier: '{row_spec}'. Use a number or 'first'/'last'."

    def set_row(self, row_spec, row_dict):
        try:
            row_idx = {"first": 0, "last": len(self.df) - 1}.get(row_spec.lower(), int(row_spec))
            
            if row_idx < 0 or row_idx >= len(self.df):
                return f"Row index {row_idx} is out of bounds. CSV has {len(self.df)} rows."
            
            missing_cols = [col for col in row_dict if col not in self.df.columns]
            if missing_cols:
                return f"Columns not in CSV: {', '.join(missing_cols)}. Available columns: {', '.join(self.df.columns)}"
            
            for col, val in row_dict.items():
                self.df.at[self.df.index[row_idx], col] = val
            
            self.save()
            return f"Row {row_spec} updated with values: {row_dict}"
        except ValueError:
            return f"Invalid row specifier: '{row_spec}'. Use a number or 'first'/'last'."

def parse_kv_string(input_str: str):
    parts = [kv.strip() for kv in input_str.split(",")]
    parsed = {}
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            parsed[key.strip()] = value.strip()
    return parsed