import matplotlib.pyplot as plt
import numpy as np

inch=2.54
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(16/inch, 10/inch))
plt.tight_layout()
for row in range(3):
	ax[row].plot(np.arange(0, 10), np.random.random(10), c='b', lw=1)
	ax[row].set_ylabel('Primary', size=6)
	ax2 = ax[row].twinx()
	ax2.plot(np.arange(0, 10), np.random.random(10), c='r', lw=1)
	ax2.set_ylabel('Secondary', size=6)
	ax[row].tick_params(axis='both', labelsize=6)
	ax2.tick_params(labelsize=6)

plt.savefig('figure', dpi=300, bbox_inches='tight')

