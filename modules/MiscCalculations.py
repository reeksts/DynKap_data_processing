import numpy as np
import math
from scipy.optimize import fsolve


class TempDistSolver():
	def __init__(self):
		self.ri = 0.036
		self.ro = 0.30

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
		rdry = ri + dry_zone
		tdiff = thot - tcold

		T_moist = []
		T_dry = []
		power = 2*math.pi*tdiff / (1/kdry*math.log(rdry/ri) + 1/kmoist*math.log(ro/rdry))

		step = 0.001

		# Dry zone temperature distribution
		for x in np.arange(ri, rdry+step, step):
			temp = thot - power / (2*math.pi*kdry) * math.log(x/ri)
			T_dry.append(temp)

		# Moist zone temperature distribution
		tdry_hot = T_dry[-1]
		for x in np.arange(rdry, ro+step, step):
			temp = tdry_hot - power / (2*math.pi*kmoist) * math.log(x/rdry)
			T_moist.append(temp)

	def two_zone_solver(self, kdry, kmoist, tcold, thot, power):
		tdiff = thot - tcold

		print(type(power))

		def min_max_temp_checker(k, power, tcold, ro, ri):
			res = math.log(ro/ri) / 2*math.pi*k
			thot = power * res + tcold
			return thot

		# Step 0: check if max and min are within the limits
		thot_max_temp = min_max_temp_checker(kdry, power, tcold, self.ro, self.ri)
		thot_min_temp = min_max_temp_checker(kmoist, power, tcold, self.ro, self.ri)

		print(f'thot max is {thot_max_temp}')
		print(f'thot is {thot}')
		print(f'thot min is {thot_min_temp}')
		if thot < thot_min_temp or thot > thot_max_temp:
			print('Hot side temperature is not in range!')

		# Step 1: find radius of the dry zone
		def func(rdry):
			f = 2*math.pi*tdiff / (math.log(rdry/self.ri)/kdry + math.log(self.ro/rdry)/kmoist) - power
			return f
		rdry = float(fsolve(func, np.array(self.ri))[0])

		# Step 2: Generate temperature dry zone
		step = 0.001
		T_dry = []
		for x in np.arange(self.ri, rdry+step, step):
			temp = thot - power / (2*math.pi*kdry) * math.log(x/self.ri)
			T_dry.append(temp)

		# Step 3: Generate temperature moist zone
		T_moist = []
		tdry_hot = T_dry[-1]
		for x in np.arange(rdry, self.ro+step, step):			# Insted of step size put step count somehow
			temp = tdry_hot - power / (2*math.pi*kmoist) * math.log(x/rdry)
			T_moist.append(temp)

		return T_dry + T_moist

	def onedim_one_zone(self):
		pass

	def onedim_two_zones(self):
		pass


class ThermalConductivity:
	def __init__(self, porosity, ks, rhos, w_grav):
		self.porosity = porosity
		self.ks = ks
		self.rhos = rhos
		self.w_grav = w_grav

	def calculate_thermal_conductivity(self):
		kdry = 0
		kmoist = 0

		rhod = (1 - self.porosity) * self.rhos
		Sr = (self.w_grav/100*rhod)/self.porosity

		ksat = self.ks**(1-self.porosity)*0.6**(self.porosity)
		kdry = self.ks**((1-self.porosity)**0.59)*0.024**(self.porosity**0.73)

		kr = (4.7*Sr)/(1+3.7*Sr)

		kmoist = (ksat - kdry) * kr + kdry
		#print(kmoist)
		#print(kdry)

		return kdry, kmoist

porosity = 0.424
ks = 2.66
rhos = 3.02
w_grav = 3

thermal = ThermalConductivity(porosity, ks, rhos, w_grav)
thermal.calculate_thermal_conductivity()