import pandas as pd
import matplotlib.pyplot as plt

SN1_summary = pd.read_excel('sample_summaries\\SN1_summary.xlsx', sheet_name='Sheet1')
SN2_summary = pd.read_excel('sample_summaries\\SN2_summary.xlsx', sheet_name='Sheet1')

fig, ax = plt.subplots()

ax.plot(SN1_summary['power'],
		SN1_summary['core'],
		label='SN1',
		marker='o')
ax.plot(SN2_summary['power'],
		SN2_summary['core'],
		label='SN2',
		marker='o')

ax.set_xlabel('Power, W')
ax.set_ylabel('Core temperature, °C')

ax.legend()

plt.show()