
import pandas as pd
df=pd.read_csv("data/poll_data.csv")
print("Dataset shape:", df.shape)
print(df.head())
print("\nVote Summary")
print(df["Option_Selected"].value_counts())
