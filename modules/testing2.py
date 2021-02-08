import matplotlib.pyplot as plt
import numpy as np

inch=2.54
fig, ax = plt.subplots(figsize=(16/inch, 4/inch))
ax.plot(np.arange(0, 10), np.random.random(10), c='b', lw=1)
ax.set_ylabel('Primary', size=6)
ax2 = ax.twinx()
ax2.plot(np.arange(0, 10), np.random.random(10), c='r', lw=1)
ax2.set_ylabel('Secondary', size=6)
ax.tick_params(axis='both', labelsize=6)
ax2.tick_params(labelsize=6)

plt.savefig('figure2', dpi=300, bbox_inches='tight')