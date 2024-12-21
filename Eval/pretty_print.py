import pandas as pd

file_path = r"Eval\evaluation_results.csv"

df = pd.read_csv(file_path)

selected_columns = ['question', 'faithfulness', 'answer_relevancy']
df_selected = df[selected_columns]

print(df_selected.head)

average_relevancy = df['answer_relevancy'].mean()

print(f"Answer Relevancy Mean: {average_relevancy:.3f}")