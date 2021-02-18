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


class ComsolProcessor:
	def __init__(self, sample, comsol_path):
		self.comsol_path = comsol_path
		self.sample = sample

	def generate_comsol_df(self):
		comsol_dfs = []
		wall_loc = 0.26
		core_loc = 0.00
		for comsol_sol in self.sample['comsol_files']:
			df = pd.read_csv(self.comsol_path + comsol_sol, names=['loc', 'mes'])
			index_vals_core = df.index[df['loc'] == core_loc].tolist()
			index_vals_wall = df.index[df['loc'] == wall_loc].tolist()
			for core_ind, wall_ind in zip(index_vals_core, index_vals_wall):
				subset = df.iloc[core_ind:wall_ind+1]
				subset['loc'] = subset['loc'].apply(lambda val: val*100)
				comsol_dfs.append(subset)

		return comsol_dfs


