#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 20:59:54 2023

Database for anesthetic gases t/b coeffs, compartment
volumes and fractions of cardiac output

@author: paco
"""
def inh_drugs_data():
    import pandas as pd
    df= pd.DataFrame(
        columns= ['blood','heart','kidney','liver','cns','muscle','fat','vrg']
        )
    df.loc['vols']=[5, 0.28, 0.32, 3.9, 1.43, 30, 13, 7]
    df.loc['co_f']=[1.0,0.04,0.214, 0.24 ,0.124, 0.15 ,0.10, 0.07]
    df.loc['Sevo']=[0.65, 1.3, 2.3, 0.69, 1.7, 3.1, 48, 2]
    df.loc['NO']=[0.47,0.87,0.93, 1.1, 1.1, 1.2,2.3,1.4]
    df.loc['Iso']=[ 1.4,1.3,2.3,2.4,1.5,2.9,45,2]
    df.loc['Des']=[0.45,1.3,1.0,1.4,1.9,2,27,2]
    df.loc['Methoxy']=[12,1.2,2.3,2.5,2,1.6,76,2.3]
    df.loc['Halothane']=[ 2.5,2.9,1.5,2.5,2.7,2.5,65,2.3]
    print(__name__)
    return df

if __name__=='__main__':
    df= inh_drugs_data()
    print(df)
    