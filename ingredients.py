import pandas as pd

def load_ingredients_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df['item'].str.lower().str.strip().unique().tolist()

