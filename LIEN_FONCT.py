#!/usr/bin/env python
# coding: utf-8

# In[1]:


## #################################################################   DEBUT   ##################################################################

import pandas as pd
import numpy as np
from datetime import datetime
import azfr_fsspec_utils as fspath
import warnings

warnings.filterwarnings('ignore')

annee = 2025
mois = 3

##  DTM MidCorp  lu depuis AZURE

DTM_MC = "abfs://data-bi-dt-abr@azfrdatalakeprod.dfs.core.windows.net/data/v2.0.0/202503/"  
PTF_MC = pd.read_parquet(fspath.join(DTM_MC, "mc_ptf/mc_ptf.parquet"))
MVT_MC = pd.read_parquet(fspath.join(DTM_MC, "mc_mvt/mc_mvt.parquet"))

## DTM Flotte  lu depuis AZURE
DTM_FL = "abfs://data-bi-dt-abr@azfrdatalakeprod.dfs.core.windows.net/data/v2.0.0/202503/" 
MVT_FL = pd.read_parquet(fspath.join(DTM_FL, "fl_mvt/fl_mvt.parquet"))

##DMTGARFL = "/sasprod/produits/SASEnterpriseBIServer/segrac/METGTECH/FLOTTES/202403/Expo" ## faire le transfere de la table sur AZUR pour lire ici
##GAR_FL = "ptf_expo_flottes_gar_202403"

##  LIENS IMS  lu depuis AZURE

IMS = "abfs://data-ims@azfrdatalakeprod.dfs.core.windows.net/data/v1.0.0/20250311"
PTF14 = pd.read_parquet(fspath.join(IMS, "INFP_IIA0P6_IPFE14_IPF/INFP_IIA0P6_IPFE14_IPF.parquet"))
PTF34 = pd.read_parquet(fspath.join(IMS, "INFP_IIA0P6_IPFE34_IPF/INFP_IIA0P6_IPFE34_IPF.parquet"))
PTF15 = pd.read_parquet(fspath.join(IMS, "INFP_IIA0P6_IPFE15_IPF/INFP_IIA0P6_IPFE15_IPF.parquet"))
PTF35 = pd.read_parquet(fspath.join(IMS, "INFP_IIA0P6_IPFE35_IPF/INFP_IIA0P6_IPFE35_IPF.parquet"))
PTF1M41 = pd.read_parquet(fspath.join(IMS, "INFP_IIA0P6_IPFE1M41_IPF/INFP_IIA0P6_IPFE1M41_IPF.parquet"))
PTF3M41 = pd.read_parquet(fspath.join(IMS, "INFP_IIA0P6_IPFE3M41_IPF/INFP_IIA0P6_IPFE3M41_IPF.parquet"))
PTF1MPI = pd.read_parquet(fspath.join(IMS, "INFP_IIA0P6_IPFE1MPI_IPF/INFP_IIA0P6_IPFE1MPI_IPF.parquet"))
PTF3MPI = pd.read_parquet(fspath.join(IMS, "INFP_IIA0P6_IPFE3MPI_IPF/INFP_IIA0P6_IPFE3MPI_IPF.parquet"))

# Spécifique au CDPROD */

lien_SEGPROD = "abfs://data-bi-dt-abr@azfrdatalakeprod.dfs.core.windows.net/data/v2.0.0/202503/"  
SEGPROD = pd.read_parquet(fspath.join(lien_SEGPROD, "rf_segprd/rf_segprd.parquet"))



######  Referentiel des codes postaux  lu depuis AZURE  ###################

POSTCD = "abfs://shared@azfrdatalab.dfs.core.windows.net/ABR/P4D/ADC/ETUDES/DataFitness/"

CODE_POSTAL_LIST = pd.read_csv(fspath.join(POSTCD, "LISTE_CODE_POSTAUX_sas.csv"), sep = ";", decimal = ".", encoding ="latin9")  ## je dois revoir la liste de code postaux j'ai fait une erreur en supprimant 


# In[2]:


## JE CREE LE NEW DF LISTE CODE POSTAUX

LISTE_CODE_POSTAUX = pd.DataFrame()
LISTE_CODE_POSTAUX = CODE_POSTAL_LIST
LISTE_CODE_POSTAUX["CODE_POSTAL"] =  CODE_POSTAL_LIST["F1_str"].apply(lambda x:"{:0>5}".format(x))

#LISTE_CODE_POSTAUX


# In[3]:


## filter IMS pour le perimetre Pro MidCord
def FILTRE_PTF(df):
    return  (
        (df['CDRI'] != 'X') &
        (~df['NOINT'].isin(['H90061', '482001', '489090', '102030', 'H90036', 'H90059', 'H99045', 'H99059',
                               '5B2000', '446000', '5R0001', '446118', '4F1004', '4A1400', '4A1500',
                               '4A1600', '4A1700', '4A1800', '4A1900', '482001', '489090', '4L1010'])) &
        (df['CDPROD'] != '01073') &
        (df['CDNATP'].isin(['R', 'O', 'T']))
    )

## NOT IN = ~df[colone].ISIN([i])  pour dire tous ceux qui ne sont pas i on ne prend pas 
## in = df[colone].ISIN([i])  pour dire tou ceux qui ne pas i on ne prend      


# In[4]:


VAR_PTF_GAR = ["MTPRPR1", "MTPRPR2", "MTPRPR3", "MTPRPR4", "MTPRPR5", "MTPRPR6", "MTPRPR7", "MTPRPR8", "MTPRPR9", "MTPRPR10",
		"MTPRPR11", "MTPRPR12", "MTPRPR13", "MTPRPR14", "MTPRPR15", "MTPRPR16", "MTPRPR17", "MTPRPR18", "MTPRPR19", "MTPRPR20",
		"MTPRPR21", "MTPRPR22", "MTPRPR23", "MTPRPR24", "MTPRPR25", "MTPRPR26", "MTPRPR27", "MTPRPR28",
		"LBGAR1", "LBGAR2", "LBGAR3", "LBGAR4", "LBGAR5", "LBGAR6", "LBGAR7", "LBGAR8", "LBGAR9", "LBGAR10",
		"LBGAR11", "LBGAR12", "LBGAR13", "LBGAR14", "LBGAR15", "LBGAR16", "LBGAR17", "LBGAR18", "LBGAR19", "LBGAR20",
		"LBGAR21", "LBGAR22", "LBGAR23", "LBGAR24", "LBGAR25", "LBGAR26", "LBGAR27", "LBGAR28"]


# In[5]:


###################      Implémentation des macros       ####################################

#################   /****** MACRO POUR LA COMPLETENESS ******/       #########################
##  FAITES PLACE A LA VARIABLE pre = PRESENT ET ABS = ABSENT, la variable pre qui represente le nombre d'enregistrement non vide

REFMIDCORP = {
    'CDPOLE' : 'SE-BG-264',
    'CDPROD' : 'SE-BG-534',
    'CDSITP': 'SE-BG-517',
    'COUNT_POLICY_CANCELLED' : 'SE-BG-1283',
    'DTEFSITT' : 'SE-BG-220',
    'DTCREPOL' : 'SE-BG-509',
    'DTEXPIR' : 'SE-BG-219',
    'DTTREVEN' : 'SE-BG-518',
    'DTRESILP' : 'SE-BG-497',
    'NOCLT' : 'SE-BG-901',
    'NOINT' : 'SE-BG-1270',
    'NOPOL' : 'SE-BG-508',
    'PCRABCOM' : 'SE-BG-455',
    'POSRISQ' : 'SE-BG-48',
    'LCI_100_IND' : 'SE-BG-380',
    'SMP_100_IND' : 'SE-BG-591',
    'PRIMES_PTF': 'SE-BG-467',
    'PRIMES_PTF_0': 'SE-BG-467',
    'PRIMES_PTF_MAX': 'SE-BG-467',
    'PRIMES_PTF_MIN': 'SE-BG-467',
    'SITU_POL': 'SE-BG-517',
    'CCC': 'SE-BG-381'
}

REFFLOTTE = {
    'DTCREPOL' : 'SE-BG-509',
    'CDPOLE' : 'SE-BG-264',
    'DIRCOM' : 'SE-BG-264',
    'DTRESILP' : 'SE-BG-497',
    'NOCLT' : 'SE-BG-901',
    'NOINT' : 'SE-BG-1270',
    'DTTREVEN' : 'SE-BG-518',
    'NOPOL' : 'SE-BG-508',
    'SITU_POL': 'SE-BG-517',
    'TYPE': 'SE-BG-534',
    'CCC': 'SE-BG-381',
    'POSRISQ': 'SE-BG-48'
}

def COMPLETENESS(x, y):
    count = f'COMP_{y}'
    # count = f'{Reference[y]}_COMP'
    x[count] = np.where(pd.isna(x[y]) | (x[y] == ""), 0, 1)

    #return x


#######  la variable TECH_VAL_FORMAT_VAR = 1 si le longueur est respecté, si non = 0   ################### 

# ON VEUT QUE DES ELEMENTS ALPHA-NUMERIQUE
def TECH_VAL_FORMAT_VAR(x, y):
    count = f'COMP_{y}'
    x[f'FORMAT_{y}'] = np.where((x[count] == 1) & (x[y].apply(lambda t: str(t).replace(' ', '').isalnum())), 1, 0)


   # print(x[f'FORMAT_{y}'])


#########   MACRO POUR LA TECHNICAL VALIDITY POUR LA LONGUEUR  ########################### 

#######  la variable TECH_VAL_LENGTH_VAR = 1 si le longueur est respecté, si non = 0   ################### 

length_val = {
    'NOPOL': 8,
    'NOCLT': 12,
    'NOINT': 6,
}

def TECH_VALIDITY_LENGTH (x, y):

    count = f'COMP_{y}'
    if y in length_val:
        x[f'LENGTH_{y}'] = np.where((x[count] == 1) & (x[y].apply(lambda t: len(str(t))) == length_val[y]), 1, 0)
    else:
        return None
    #print(x[f'LENGTH_{y}'])


#######################################   MACRO POUR LES BUSINESS VALIDY     #################################################

def BUSINESS_VALIDY (x, y):

    ###########   MIDCORP   #########################
    if (y == "CDSITP"):
        control = x[y].isin(['1', '2', '3', '4', '5', '6'])
    elif (y == "DTEFSITT"):
        control = (x[y] <= x["DTEXPIR"]) | (pd.notna(x[y]) & pd.isna(x["DTEXPIR"]))
    elif (y == "DTEXPIR"):
        control = (x["DTEFSITT"] <= x[y]) | (pd.notna(x["DTEFSITT"]) & pd.isna(x[y]))
    elif (y == "DTTREVEN"):
        control = (((x[y] >= x["DTEFSITT"]) & (x[y] <= x["DTEXPIR"])) | ((x[y] >= x["DTEFSITT"]) & (pd.isna(x["DTEXPIR"]))))
    elif (y == "DTRESILP"):
        control = (x[y] >= x["DTEFSITT"])
    elif (y == "DTCREPOL"):
        control = x[y] <= x["DTEFSITT"]
    elif (y in ["LCI_100", "LCI_100_IND", "SMP_100", "SMP_100_IND"]):
        control = x[y] > 0
    elif (y == "PCRABCOM"):
        control = x[y] >= 0
    elif (y == "CDPOLE"): # même condition dans le périmetre FLOTTE.
        control = x[y].isin(['1', '3', '9'])

    ##################  FLOTTE  ##########################################
    elif (y == "SITU_POL"):
        control = x[y].isin(["ANTICIPEE","EN COURS","EXPIREE","RESILIEE","SUSPENDUE"])
    elif (y == "CMARCH"):
        control = x[y].isin(['1', '2', '3', '4', '5', '6', '7'])
    elif (y == "CSEG"):
        control = x[y].isin(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    elif (y == "CSSSEG"):
        control = x[y].isin(['4', '6', '5', '3', '2', '7', '1', '8', '9'])

    count = f'COMP_{y}'
    x[f'BUS_VAL_{y}'] = np.where((x[count] == 1) & control, 1, 0)

    #print(x[f'BUS_VAL_{y}'])


# In[6]:


def calculate_percentage_difference(df):
    percentage_differences = pd.DataFrame()
    for col in diff.columns.levels[0]:  # Iterate over main columns
        self_col = diff[col]['self']
        other_col = diff[col]['other']
        percentage_diff = ((other_col - self_col) / other_col) * 100
        percentage_differences[(col, 'percentage_difference')] = percentage_diff
    return percentage_differences


# In[7]:


##############################################################              FIN POUR DAMOCLES               #######################################################################

