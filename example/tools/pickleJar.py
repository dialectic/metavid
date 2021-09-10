# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 22:32:57 2021

@author: pluralize-abenson
"""

import numpy as np
import pickle


for i in range(0,3):
	file_name = open(f'pickle_{i}.pkl','wb')
	pickle.dump(np.random.rand(8,2), file_name)
	
	file_name.close()

