
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

#opening the file
# from Tkinter import Tk
# from tkFileDialog import askopenfilename

# Tk().withdraw()

delta = 20

distance = 80

Iarray = []
P11array = []
P12array = []
P13array = []

P21array = []
P22array = []
P23array = []

P31array = []
P32array = []
P33array = []


#Configs for different videos

Videonumber = 2
#Video 
number = ['' , '2' , '3']
threshold = [150, 30, 1]
framestart = [1, 1, 1]
frameend = [348,330,1834]
ClusterPlacement = [0.6,0.5]
ColorFilter= [2, 1, 0]


#Show point placements

rframe = int(frameend[Videonumber - 1] / 2)
index = '%.5d' % rframe
filename = "Video" + number[Videonumber - 1] + "/a" + index + ".jpg"


# Bring the image in graystyle
img = cv2.imread(filename)

placerX = int(img.shape[0]*ClusterPlacement[0])
placerY = int(img.shape[1]*ClusterPlacement[1])

cv2.circle(img, (placerX,placerY) ,3, (255,255,255), -1)
cv2.circle(img, (placerX+delta,placerY) , 1, (255,255,255), -1)
cv2.circle(img, (placerX,placerY+delta) , 1, (255,255,255), -1)

cv2.circle(img, (placerX,placerY-distance) ,3, (255,255,255), -1)
cv2.circle(img, (placerX+delta,placerY-distance) , 1, (255,255,255), -1)
cv2.circle(img, (placerX,placerY+delta - distance) , 1, (255,255,255), -1)

cv2.circle(img, (placerX+distance,placerY-distance) , 3, (255,255,255), -1)
cv2.circle(img, (placerX+delta+distance,placerY-distance) , 1, (255,255,255), -1)
cv2.circle(img, (placerX+distance,placerY+delta - distance) , 1, (255,255,255), -1)


plt.imshow(img)
plt.show()




for i in range(framestart[Videonumber - 1],frameend[Videonumber - 1]):
	index = '%.5d' % i
	Iarray.append(i)
	filename = "Video" + number[Videonumber - 1] + "/a" + index + ".jpg"


	# Bring the image in graystyle
	img = cv2.imread(filename)

	placerX = int(img.shape[0]*ClusterPlacement[0])
	placerY = int(img.shape[1]*ClusterPlacement[1])

	


	p11 = img[placerX,placerY]
	p12 = img[placerX + delta,placerY]
	p13 = img[placerX, placerY - delta]

	p21 = img[placerX,placerY - distance]
	p22 = img[placerX + delta,placerY - distance]
	p23 = img[placerX, placerY - delta - distance]

	p31 = img[placerX + distance,placerY - distance]
	p32 = img[placerX + delta + distance,placerY - distance]
	p33 = img[placerX + distance, placerY - delta - distance]

	filterkey = ColorFilter[Videonumber - 1]

	P11array.append(p11[filterkey])
	P12array.append(p12[filterkey])
	P13array.append(p13[filterkey])

	P21array.append(p21[filterkey])
	P22array.append(p22[filterkey])
	P23array.append(p23[filterkey])

	P31array.append(p31[filterkey])
	P32array.append(p32[filterkey])
	P33array.append(p33[filterkey])


plt.plot(Iarray,P32array)
plt.show()


def PeaksFinder(someArray):
	thre = threshold[Videonumber - 1]
	p1 = 0
	loop = 1
	PeakArray = []
	for p2 in range(0,len(someArray)):
		if someArray[p2] > thre and loop == 1:
			a = p1
			loop = 2
		if someArray[p2] < thre and loop == 2:
			b = p2
			loop = 1
			c = float(a + b) / float(2)
			PeakArray.append(c)
		p1 = p2
	return PeakArray


Peak11 = PeaksFinder(P11array)
Peak12 = PeaksFinder(P12array)
Peak13 = PeaksFinder(P13array)

Peak21 = PeaksFinder(P21array)
Peak22 = PeaksFinder(P22array)
Peak23 = PeaksFinder(P23array)

Peak31 = PeaksFinder(P31array)
Peak32 = PeaksFinder(P32array)
Peak33 = PeaksFinder(P33array)



# plt.plot(Iarray,P11array)
# plt.show()


#Bundling
Passes = []


#Filter Section


#del Peak11[0]
# del Peak12[0]
# del Peak13[0]
#del Peak21[0]
# del Peak22[0]
#del Peak23[0]
# del Peak32[0]
# del Peak33[0]




least = min(len(Peak11),len(Peak12),len(Peak13),len(Peak21),len(Peak22),len(Peak23),len(Peak31),len(Peak32),len(Peak33))
for item in range(0,least):
	mc1 = [Peak11[item],Peak12[item],Peak13[item]]
	mc2 = [Peak21[item],Peak22[item],Peak23[item]]
	mc3 = [Peak31[item],Peak32[item],Peak33[item]]
	Passes.append([mc1,mc2,mc3])


print("\n\n")
print(Passes)
print("\n\n\n")

def TupleCloseness_Variance(sometuple1):
	v1 = sometuple1[0]
	v2 = sometuple1[1]
	v3 = sometuple1[2]
	vavg = float(v1 + v2 + v3)/float(3)
	vVar = (v1 - vavg)**2 + (v2 - vavg)**2 + (v3 - vavg)**2

	return vVar



import operator



def DeletionSuggestor(Array1,nextArray):
	Array2 = Array1[:]

	VarianceData = {}

	#Unchanged    # ID : 0
	VarianceData["0"] = TupleCloseness_Variance(Array2)

	#Deletion     # ID  : 1
	Array2[0] = nextArray[0]
	VarianceData["1"] = TupleCloseness_Variance(Array2)

	#Deletion     # ID  : 2
	Array2 = Array1[:]
	Array2[1] = nextArray[1]
	VarianceData["2"] = TupleCloseness_Variance(Array2)


	#Deletion     # ID  : 3
	Array2 = Array1[:]
	Array2[2] = nextArray[2]
	VarianceData["3"] = TupleCloseness_Variance(Array2)

	#Deletion     # ID  : 4
	Array2 = Array1[:]
	Array2[0] = nextArray[0]
	Array2[1] = nextArray[1]
	VarianceData["4"] = TupleCloseness_Variance(Array2)

	#Deletion     # ID  : 5
	Array2 = Array1[:]
	Array2[0] = nextArray[0]
	Array2[2] = nextArray[2]
	VarianceData["5"] = TupleCloseness_Variance(Array2)

	#Deletion     # ID  : 6
	Array2 = Array1[:]
	Array2[1] = nextArray[1]
	Array2[2] = nextArray[2]
	VarianceData["6"] = TupleCloseness_Variance(Array2)

	SVarianceData = sorted(VarianceData.items(), key=operator.itemgetter(1))

	DeletionParameter = int(SVarianceData[0][0])

	print(SVarianceData)

	if SVarianceData[0][1] == VarianceData.get("0"):
		DeletionParameter = 0

	return DeletionParameter




for c in range(0,3):
	if len(Passes) >= 2:
		b1i = Passes[0][c][0]
		b2i = Passes[0][c][1] 
		b3i = Passes[0][c][2]

		b1f = Passes[1][c][0]
		b2f = Passes[1][c][1] 
		b3f = Passes[1][c][2]

		ituple = [b1i,b2i,b3i]
		ftuple = [b1f,b2f,b3f]

		dP = DeletionSuggestor(ituple,ftuple)

		print(c)

		print(dP)

		if c == 0:
			if dP == 1:
				del Peak11[0]
			if dP == 2:
				del Peak12[0]
			if dP == 3:
				del Peak13[0]
			if dP == 4:
				del Peak11[0]
				del Peak12[0]
			if dP == 5:
				del Peak11[0]
				del Peak13[0]
			if dP == 6:
				del Peak12[0]
				del Peak13[0]
		if c == 1:
			if dP == 1:
				del Peak21[0]
			if dP == 2:
				del Peak22[0]
			if dP == 3:
				del Peak23[0]
			if dP == 4:
				del Peak21[0]
				del Peak22[0]
			if dP == 5:
				del Peak21[0]
				del Peak23[0]
			if dP == 6:
				del Peak22[0]
				del Peak23[0]
		if c == 2:
			if dP == 1:
				del Peak31[0]
			if dP == 2:
				del Peak32[0]
			if dP == 3:
				del Peak33[0]
			if dP == 4:
				del Peak31[0]
				del Peak32[0]
			if dP == 5:
				del Peak31[0]
				del Peak33[0]
			if dP == 6:
				del Peak32[0]
				del Peak33[0]
	 
Passes = []

least = min(len(Peak11),len(Peak12),len(Peak13),len(Peak21),len(Peak22),len(Peak23),len(Peak31),len(Peak32),len(Peak33))
for item in range(0,least):
	mc1 = [Peak11[item],Peak12[item],Peak13[item]]
	mc2 = [Peak21[item],Peak22[item],Peak23[item]]
	mc3 = [Peak31[item],Peak32[item],Peak33[item]]
	Passes.append([mc1,mc2,mc3])


print("\n\n New Passes ")
print(Passes)
print("\n\n\n")




passarray = []

Qvalue = []

Deviationarrayc1 = []
Deviationarrayc2 = []
Deviationarrayc3 = []

xcenterArray = []
ycenterArray = []

for pass1 in range(0,len(Passes)):
	c1 = Passes[pass1][0][0]
	c1p2 = Passes[pass1][0][1] - c1
	c1p3 = Passes[pass1][0][2] - c1

	


	c2 = Passes[pass1][1][0]
	c2p2 = Passes[pass1][1][1] - c2
	c2p3 = Passes[pass1][1][2] - c2

	

	c3 = Passes[pass1][2][0]
	c3p2 = Passes[pass1][2][1] - c3
	c3p3 = Passes[pass1][2][2] - c3

	

	d = distance

	#Distance between Adjacent Probes

	h = delta

	# Init Cluster

	a = 4

	
	#  Probe positions

	# Cluster 1 :
	# Probe 1 : (0,0)
	# Probe 2 : (h,0)
	# Probe 3 : (0,h)

	# Cluster 2 :
	# Probe 1 : (0,d)
	# Probe 2 : (h,d)
	# Probe 3 : (0,h+d)

	# Cluster 3 :
	# Probe 1 : (d,d)
	# Probe 2 : (h+d,d)
	# Probe 3 : (d,h+d)

	

	#Slopes for Cluster 1

	try:

		mc1 = (-1)*float(float(c1p2)/float(c1p3))

		mc2 = (-1)*float(float(c2p2)/float(c2p3))

		mc3 = (-1)*float(float(c3p2)/float(c3p3))


		xcenter = (float(float(mc1*mc2)/float(mc1-mc2)) * d)

		ycenter = (-1)*(float(float(mc2)/float(mc1-mc2)) * d)

		ycenterArray.append(ycenter)
		xcenterArray.append(xcenter)

		#print(" X Center : %f " % xcenter)

		#print(" Y Center : %f " % ycenter)




		mk = float(float(d - ycenter)/float(d - xcenter))

		S = (-1)*float(float(1)/float(mc3))


		p = abs(float(float(S - mk)/float(1 + (S*mk))))

		#print("")
		#print("Q Value")

		#print(np.arctan(p)*180/(np.pi))

		Qvalue.append(np.arctan(p)*2/(np.pi))
		Deviationarrayc1.append(abs(c1p2 + c1p3))
		Deviationarrayc2.append(abs(c2p2 + c2p3))
		Deviationarrayc3.append(abs(c3p2 + c3p3))
		passarray.append(pass1+1)
	except ZeroDivisionError:
		True


print("")
print(" Video Frame Taken : %s" % filename)
print("")
print(" Cluster Placement :          X : %f      Y : %f" % (ClusterPlacement[0],ClusterPlacement[1]))
print("")
print(" Filter Threshold used : %d" % threshold[Videonumber - 1])



Determinant = 0
for c in Qvalue:
	Determinant = Determinant + c


try:
	print("")
	print(" Average Q Value : %f" % (float(Determinant)/float(len(Qvalue))))
except ZeroDivisionError:
	print("\n Couldn't compute Q Value.")
	True


AvgXcenter = 0
for c in xcenterArray:
	AvgXcenter = AvgXcenter + c

AvgYcenter = 0
for c in ycenterArray:
	AvgYcenter = AvgYcenter + c

try:
	print("")
	XC = float(AvgXcenter)/(float(len(xcenterArray)))
	YC = float(AvgYcenter)/(float(len(ycenterArray)))
	print(" Average Xcenter : %f  and Ycenter : %f" % (XC,YC))
except ZeroDivisionError:
	print("\n Couldn't compute Centre Values.")
	True

# plt.plot(passarray,Deviationarrayc1,'ro')
# plt.plot(passarray,Deviationarrayc2,'ro')
# plt.plot(passarray,Deviationarrayc3,'ro')
# plt.show()

plt.plot(passarray,Qvalue,'ro')
plt.show()




