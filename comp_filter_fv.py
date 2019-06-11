import collections as coll
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import datetime
import time
from time import gmtime, strftime
print(strftime("%Y-%m-%d_%H-%M-%S", gmtime()))

""" ============================================ Importation des fichiers ===================================== """

the_stamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
the_timestamp = os.path.dirname(os.path.realpath(__file__)) + '/figures/' + the_stamp
# plt.savefig(str(the_timestamp) + '_Fig_RotX_cfx.png', format='png', bbox_inches='tight')
# the_timestamp = strftime("%Y-%m-%d_%H-%M-%S", gmtime())

fs = 100.0
dt = 1.0/fs
alpha = 0.02

Sample = coll.namedtuple("Sample","acc_angZ acc_angY acc_angX Rot_Z Rot_Y Rot_X CF_Z CF_Y CF_X G_Z G_Y G_X")

def samples_from_file(fname):
    with open(fname) as f:
        next(f)  # discard header row
        csv_reader = csv.reader(f, dialect='excel')

        for i, row in enumerate(csv_reader, 1):
            try:
                values = [float(x) for x in row]
                yield Sample(*values)
            except Exception:
                lst = list(row)
                print("Bad line %d: len %d '%s'" % (i, len(lst), str(lst)))



theFileName = os.path.dirname(os.path.realpath(__file__)) + "/data/sample_dataBis.csv"
# theFileName = os.path.dirname(os.path.realpath(__file__)) + "/data/data_from_so.csv"
samples = list(samples_from_file(theFileName))

df = pd.read_csv(theFileName, sep=',') #, nrows=1000)  # or your sep in file

""" ================================= Filtre complementaire ============================================= """

cfx = np.zeros(len(samples))
cfy = np.zeros(len(samples))
cfz = np.zeros(len(samples))
x=np.zeros(len(samples))
y=np.zeros(len(samples))
z=np.zeros(len(samples))



cfx[0] = samples[0].acc_angX
cfy[0] = samples[0].acc_angY
cfz[0] = samples[0].acc_angZ

for i, s in enumerate(samples[1:], 1):
    cfx[i] = (1.0 - alpha) * (cfx[i-1] + s.Rot_X*dt) + (alpha * s.acc_angX)
    cfy[i] = (1.0 - alpha) * (cfy[i-1] + s.Rot_Y*dt) + (alpha * s.acc_angY)
    cfz[i] = (1.0 - alpha) * (cfz[i-1] + s.Rot_Z*dt) + (alpha * s.acc_angZ)
    x[i] = s.Rot_X*dt + s.acc_angX
    y[i] = s.Rot_Y*dt + s.acc_angY
    z[i] = s.Rot_Z*dt + s.acc_angZ
    

""" ================================== Trace des courbes ================================================== """
 

""" ======================================= axe x =============================================== """

# df.plot(y='acc_angX', label='non filtrees axe x: acc_angX', color='blue')

# df.plot(y='CF_X', label='filtrees data axe x: CF_X', color='black')

# df.plot(y='G_X', label='non filtrees axe x: G_X', color='red')

# df.plot(y='Rot_X', label='non filtrees axe x: Rot_X', color='green')

plt.plot(x, label='somme des courbes non filtrees axe x', color='yellow')

plt.plot(cfx, label='filtrees calculees cfx', color='black')
 
plt.legend(loc='best')
theFileName = os.path.dirname(os.path.realpath(__file__)) + "/data/sample_dataBis.csv"
plt.savefig(str(the_timestamp) + '_Fig_RotX_cfx.png', format='png', bbox_inches='tight')

# plt.xlabel('index des valeurs')
# plt.ylabel('position angulaire (degre)')
# plt.title("Position angulaire selon l'axe x en fonction de l'index des valeurs")
# plt.show()


""" ======================================= axe y =============================================== """



# df.plot(y='acc_angY', label='non filtrees axe y: acc_angY', color='black')

# df.plot(y='CF_Y', label='filtrees data axe y: CF_Y', color='black')

# df.plot(y='G_Y', label='non filtrees axe y: G_Y', color='black')

# df.plot(y='Rot_Y', label='non filtrees axe y: Rot_y', color='black')

plt.plot(y, label='somme des courbes non filtrees axe y', color='blue')

plt.plot(cfy, label= 'filtrees calculees : cfy', color='red')

plt.legend(loc='best')
plt.savefig(str(the_timestamp) + '_Fig_RotY_cfy.png', format='png', bbox_inches='tight')

# plt.xlabel('index des valeurs')
# plt.ylabel('position angulaire (degre)')
# plt.title("Position angulaire selon l'axe y en fonction de l'index des valeurs")
# plt.show()


""" ======================================= axe z =============================================== """

# df.plot(y='acc_angZ', label='non filtrees axe z: acc_angZ', color='black')

# df.plot(y='CF_Z', label='filtrees data axe z: CF_Z', color='black')

# df.plot(y='G_Z', label='non filtrees axe z: G_Z', color='black')

# df.plot(y='Rot_Z', label='non filtrees axe z: Rot_Z', color='black')

plt.plot(z, label='somme des courbes non filtrees axe z', color='green')

plt.plot(cfz, label= 'filtrees calculees : cfz', color='orange')

plt.legend(loc='best')
plt.savefig(str(the_timestamp) + '_Fig_RotZ_cfz.png', format='png', bbox_inches='tight')
plt.show()

# plt.xlabel('index des valeurs')
# plt.ylabel('position angulaire (degre)')
# plt.title("Position angulaire en fonction de l'index des valeurs")
# plt.show()


