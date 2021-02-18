import numpy as np
import math


class TempDistSolver():
	def __init__(self):
		pass

	def radial_one_zone(self, kmoist, tcold, thot):
		ri = 0.036
		ro = 0.3
		tdiff = thot - tcold

		step = 0.001
		T_x = []

		power = 2*math.pi*kmoist / math.log(ro/ri) * tdiff
		T_x = []
		for x in np.arange(ri, ro+step, step):
			temp = thot - power / (2*math.pi*kmoist) * math.log(x / ri)
			T_x.append(temp)

		return T_x


	def radial_two_zones(self, dry_zone, kdry, kmoist, tcold, thot):
		ri = 0.036
		ro = 0.3
		tdiff = thot - tcold

		power =

	def onedim_one_zone(self):
		pass

	def onedim_two_zones(self):
		pass



kdry = 0.4
kmoist = 1.3
tcold = 10
thot = 80
dry_zone = 0.05  # Size of dry zone strating form hot end

solver = TempDistSolver()
solver.radial_one_zone(kmoist, tcold, thot)
solver


