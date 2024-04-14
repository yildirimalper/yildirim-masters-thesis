import pandas as pd
from pathlib import Path
import re
import pickle

PROJECT_DIR = Path().resolve()

# Load the data
data = pd.read_csv(PROJECT_DIR / 'data' / 'ecb_announcements.csv')
dictionary = pd.read_csv(PROJECT_DIR / 'data' / 'LoughranMcDonald_Dictionary.csv')

