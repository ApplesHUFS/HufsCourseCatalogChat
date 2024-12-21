import os
from datasets import Dataset
import pandas as pd
from main import chatting
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
import tqdm
import ast
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

df = pd.read_csv(r'eval_data.csv')

if 'answer' not in df.columns:
    df['answer'] = ''

for idx, row in tqdm.tqdm(df.iterrows()):
    question = row['question']
    response = chatting(question)
    df.at[idx, 'answer'] = response

print(df[['question', 'answer']].head())

def convert_contexts(x):
    try:
        return ast.literal_eval(x)
    except:
        return [x]

df['contexts'] = df['contexts'].apply(convert_contexts)

df.to_csv('answered_dataset.csv', index=False)

dataset = Dataset.from_pandas(df[['question', 'answer', 'contexts', 'ground_truth']])

result = evaluate(
    dataset=dataset,
    metrics=[
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    ],
)

print(result)

df_result = result.to_pandas()
print(df_result.head())

df_result.to_csv('evaluation_results.csv', index=False)