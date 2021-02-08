import os
import pandas as pd

class ComsolModel:
	def __init__(self, comsol_path):
		self.comsol_path = comsol_path
		self.comsol_models_dfs = []
		for file in os.listdir(comsol_path):
			if file.endswith('csv'):
				df_loc = pd.read_csv(self.comsol_path + file, names=['loc', 'temp'])
				df_loc['loc'] = df_loc['loc'].apply(lambda dist: dist*100)
				self.comsol_models_dfs.append(df_loc)
			else:
				pass

if __name__ == "__main__":
	model = ComsolModel('C:\\Users\\karlisr\\OneDrive - NTNU\\3_PostDoc_Sintef\\01_laboratory_work\\01_large_test\\'
						'07_testing_data\\01_Sample_1_Vassfjell_4%_fines_Pallet_1\\03_comsol_model\\')
	print(model.comsol_models_dfs)
