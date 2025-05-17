import os
import pandas as pd

class CSVHandler:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self._load_csv()
        
    def _load_csv(self):
        try:
            self.df = pd.read_csv(self.csv_path)
        except FileNotFoundError:
            self.df = pd.DataFrame()
            self.save()

    def save(self):
        self.df.to_csv(self.csv_path, index=False)

    def get_column_names(self):
        self._load_csv() 
        return list(self.df.columns)
        
    def get_csv_info(self):
        self._load_csv() 
        columns = self.get_column_names()
        num_rows = len(self.df)
        preview = self.df.head(3).to_string()
        return f"CSV has {num_rows} rows and columns: {', '.join(columns)}\nPreview:\n{preview}"

    def remove_column(self, column_name: str):
        self._load_csv() 
        columns = self.get_column_names()
        
        if column_name not in columns:
            matches = [col for col in columns if column_name.lower() in col.lower()]
            if len(matches) == 1:
                column_name = matches[0]
            elif len(matches) > 1:
                return f"Multiple columns match '{column_name}': {', '.join(matches)}. Please be more specific."
            else:
                return f"Column '{column_name}' does not exist. Available columns: {', '.join(columns)}"
                
        self.df.drop(columns=[column_name], inplace=True)
        self.save()
        return f"Column '{column_name}' removed."

    def remove_row(self, index_or_desc: str):
        self._load_csv() 
        try:
            if index_or_desc.lower() == "last":
                index = len(self.df) - 1
            elif index_or_desc.lower() == "first":
                index = 0
            else:
                index = int(index_or_desc)
                
            if index < 0 or index >= len(self.df):
                return f"Row index {index} is out of range (0-{len(self.df)-1})."
                
            removed_row = self.df.iloc[index].to_dict()
            self.df.drop(index=index, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
            self.save()
            return f"Row {index} removed: {removed_row}"
            
        except ValueError:
            return f"Invalid row specifier. Use a number, 'first', or 'last'."

    def add_column(self, input_str: str):
        self._load_csv() 
        parts = [part.strip() for part in input_str.split("with")]
        column_name = parts[0].strip()
        
        if column_name in self.df.columns:
            return f"Column '{column_name}' already exists."
            
        default_value = ""
        if len(parts) > 1 and "values" in parts[1]:
            value_part = parts[1].strip()
            if "=" in value_part:
                default_value = value_part.split("=")[1].strip()
                try:
                    if default_value.isdigit():
                        default_value = int(default_value)
                    else:
                        default_value = float(default_value)
                except:
                    pass
        
        self.df[column_name] = default_value
        self.save()
        return f"Column '{column_name}' added with default value: '{default_value}'."

    def add_row(self, row_dict: dict):
        self._load_csv() 
        missing_cols = [col for col in row_dict if col not in self.df.columns]
        if missing_cols:
            return f"Columns don't exist: {', '.join(missing_cols)}. Available columns: {', '.join(self.df.columns)}"
        for col in self.df.columns:
            if col not in row_dict:
                row_dict[col] = ""
                
        self.df = pd.concat([self.df, pd.DataFrame([row_dict])], ignore_index=True)
        self.save()
        return f"Row added: {row_dict}"

    def set_cell(self, row_spec, column_name, value):
        self._load_csv() 
        try:
            if isinstance(row_spec, str):
                if row_spec.lower() == "last":
                    row_index = len(self.df) - 1
                elif row_spec.lower() == "first":
                    row_index = 0
                else:
                    row_index = int(row_spec)
            else:
                row_index = int(row_spec)
        except ValueError:
            return f"Invalid row specifier '{row_spec}'. Use a number, 'first', or 'last'."
            
        if row_index < 0 or row_index >= len(self.df):
            return f"Row index {row_index} is out of range (0-{len(self.df)-1})."
            
        columns = self.get_column_names()
        if column_name not in columns:
            matches = [col for col in columns if column_name.lower() in col.lower()]
            if len(matches) == 1:
                column_name = matches[0]
            elif len(matches) > 1:
                return f"Multiple columns match '{column_name}': {', '.join(matches)}. Please be more specific."
            else:
                return f"Column '{column_name}' does not exist. Available columns: {', '.join(columns)}"
                
        try:
            if str(value).isdigit():
                value = int(value)
            elif str(value).replace('.', '', 1).isdigit() and str(value).count('.') <= 1:
                value = float(value)
        except:
            pass
            
        self.df.at[row_index, column_name] = value
        self.save()
        return f"Value set at row {row_index}, column '{column_name}' to '{value}'."

    def set_row(self, row_spec, row_dict):
        self._load_csv() 
        try:
            if isinstance(row_spec, str):
                if row_spec.lower() == "last":
                    row_index = len(self.df) - 1
                elif row_spec.lower() == "first":
                    row_index = 0
                else:
                    row_index = int(row_spec)
            else:
                row_index = int(row_spec)
        except ValueError:
            return f"Invalid row specifier '{row_spec}'. Use a number, 'first', or 'last'."
            
        if row_index < 0 or row_index >= len(self.df):
            return f"Row index {row_index} is out of range (0-{len(self.df)-1})."
            
        columns = self.get_column_names()
        for col in row_dict:
            if col not in columns:
                return f"Column '{col}' does not exist. Available columns: {', '.join(columns)}"
                
        for col, val in row_dict.items():
            try:
                if str(val).isdigit():
                    val = int(val)
                elif str(val).replace('.', '', 1).isdigit() and str(val).count('.') <= 1:
                    val = float(val)
            except:
                pass
                
            self.df.at[row_index, col] = val
            
        self.save()
        return f"Row {row_index} updated: {row_dict}"

def parse_kv_string(input_str: str):
    parts = [kv.strip() for kv in input_str.split(",")]
    parsed = {}
    for part in parts:
        if "=" in part:
            k, v = part.split("=", 1)
            parsed[k.strip()] = v.strip()
    return parsed 