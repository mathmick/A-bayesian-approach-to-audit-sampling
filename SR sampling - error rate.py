##########################################################################################################################
# This file demonstrates simple random sampling, estimating an error rate                                                #
# The example loads the SDU data file, computes a number of errors and adds these errors to the account                  #
# After having added the errors, sampling is repeated, and the corresponding histogram is drawn along with the predicted #
# distribution.                                                                                                          #
##########################################################################################################################

import csv
import numpy as np
import matplotlib.pyplot as plt
import pylab

from scipy.stats import norm

# Step 1: Critical parameters

sample_size = 781
number_of_samples = 100000
error_rate = 0.03

# Step 2: Read the data

def readcsv(filename):
    ifile = open(filename, "r")
    reader = csv.reader(ifile, delimiter=",")
    rownum = 0
    a = []
    for row in reader:
        a.append(row)
        rownum += 1
    ifile.close()
    return a

SDU_account=readcsv('clean_account_one_percent_discard.csv')
counter = 0

# Step 3: Introduce errors to the account string.
#         Additional column stores the errors

while counter < len(SDU_account):
    SDU_account[counter][2] = float(SDU_account[counter][2])
    SDU_account[counter].append(0) #Create column to store errors
    counter += 1

num_of_errors=int(error_rate*len(SDU_account))

# First find out which entries should be in error
error_list = np.random.choice(len(SDU_account),num_of_errors,replace=False)
counter = 0
# Then add the error to the entry
while counter < num_of_errors:
    SDU_account[error_list[counter]][4]=1
    counter += 1


# Step 4: Perform the sampling.
#         Extract number_of_samples samples, each of size sample_size

sample_list = []
counter = 0
error_count = 0
while counter < number_of_samples:
    temp_sum = 0
    temp_sample = np.random.choice(len(SDU_account),sample_size,replace=False)

    temp_counter = 0

    while temp_counter < sample_size:
        temp_sum += SDU_account[temp_sample[temp_counter]][4]
        temp_counter += 1

    sample_list.append(temp_sum/sample_size)
    if temp_sum/sample_size>0.04:
        error_count += 1
    if counter/1000 == int(counter/1000):
        print(counter)
    counter +=1
    

# Step 5: Display outcome of sampling to screen

# Compute percentage of samples exceeding materiality limit
print('Percentage of samples indicating an error rate above 4 percent: ',error_count/number_of_samples)


# Print histogram to screen, including predicted pdf of sampling distribution
n, bins, patches = plt.hist(sample_list, 20, density=True, facecolor='g', alpha=0.75)

x = np.arange(0.01,0.07,0.001)
y = norm.pdf(x,0.03,0.006079)
pylab.plot(x,y)

pylab.title('Simple Random Sampling, samples=10.000, sample size=781, bins=20')
pylab.ylabel('Frequency')
pylab.xlabel('Observed error rate, $p$')

plt.show()








