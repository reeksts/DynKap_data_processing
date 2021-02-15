import pandas as pd
import numpy as np



class DataProcessor:
	def __init__(self, filename):
		self.filename = filename
		self.df = pd.read_csv(self.filename, names=['col1', 'col2'])
		print(id(self.df))

	def generate_main_df(self):
		return self.df

filename = 'test_df.csv'

data_processor = DataProcessor(filename)
df = data_processor.generate_main_df()


df['col1'] = df['col1'].apply(lambda val: np.nan)

print(df)