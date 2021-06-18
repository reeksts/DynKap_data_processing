import matplotlib.pyplot as plt

def plotter(ax):
	plot_list = []

	plot = ax.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], label='label')
	plot_list.append(plot[0])
	plot = ax.plot([1, 2, 3, 4, 5], [2, 3, 4, 5, 6], label='label')
	plot_list.append(plot[0])
	ax_twin = plt.twinx(ax)
	plot = ax_twin.plot([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], label='label')
	plot_list.append(plot[0])
	ax_twin.set_ylabel('Axis label')

	labels = [plot.get_label() for plot in plot_list]
	legend = ax_twin.legend(
		plot_list,
		labels,
		ncol=3,
		loc='center left',
		bbox_to_anchor=(1.05, 0.5))


fig, axes = plt.subplots(ncols=1, nrows=3, figsize=(28/2.54, 12/2.54), sharex='col')

for ax in axes:
	plotter(ax)

plt.tight_layout(pad=0.2, h_pad=0.2)

plt.show()

fig.savefig('testing',
			dpi=300)


