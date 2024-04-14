from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import pandas as pd

df = pd.read_csv('ecb_communication.csv')

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

df['sentiment'] = df['text'].apply(lambda x: nlp(x))

print(df['sentiment'])