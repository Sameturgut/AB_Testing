import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


data1 = pd.read_excel("datasets/ab_testing.xlsx",sheet_name = 'Control Group')
data2 = pd.read_excel("datasets/ab_testing.xlsx",sheet_name = 'Test Group')

df1 = data1.copy()
df2 = data2.copy()

"""
Veri Seti : 

Impression :    Reklam görüntüleme sayısı
Click :         Görüntülenen reklama tıklama sayısı
Purchase :      Tıklanan reklamlar sonrası satın alınan ürün sayısı
Earning Satın : Alınan ürünler sonrası elde edilen kazanç

"""

# Control Group Analiz
df1.head()
df1.shape
df1.describe().T

# Test Group Analiz
df2.head()
df2.shape
df2.describe().T

# Аmaç average bidding test ve maximum bidding test uygulanan iki farklı grubun
# satın alma oranların birbiri arasında anlamlı bir farklılık olup olmadığını bulmaktır.


# Dönüşüm oranı ortalamaları ( Gözlemlemek için )

print( ' Max. bidding donusum orani : %.4f' % (df1["Purchase"].sum() / df1["Impression"].sum()) ) #0.054
print( ' Аvg. bidding donusum orani : %.4f' % (df2["Purchase"].sum() / df2["Impression"].sum()) ) #0.048

# df1 ve df2 isimli dataframeleri birleştirme işlemini gerçekleştiriyoruz. Bunu da df3 olarak tanımlıyoruz.
df3 = pd.concat([df1, df2],keys=["Max.Bidd" , "Avg.Bidd"],names=["Group_Name"])
df3= df3.reset_index()


###########################################
# Adım 1 : Hipotezlerimizi Tanımlayalım
###########################################


# H0 : M1 = M2  ( Satın alma ortalamarı  arasında anlamlı bir farklılık yoktur. )
# H1 : M1 != M2 ( Satın alma ortalamarı   arasında anlamlı bir farklılık vardır. )

df3.groupby("Group_Name").agg({"Purchase" : "mean"})

###########################################
# Adım 2 : Varsayımların kontrolü
###########################################


###### Normallik Varsayımı ######

"""
H0: Normal dağılım varsayımı sağlanmaktadır. 
H1: Normal dağılım varsayımı sağlanmamaktadır.
p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
"""

test_stat, pvalue = shapiro(df3.loc[df3["Group_Name"] == "Max.Bidd", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(df3.loc[df3["Group_Name"] == "Avg.Bidd", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

## !! p-value değerleri 0.05 'ten büyük çıktığı için H0 reddedilemez

###### Varyans Homojenliği Varsayımı ######

"""
H0: Varyanslar homojendir.
H1: Varyanslar homojen Değildir.
p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
"""

test_stat, pvalue = levene(df3.loc[df3["Group_Name"] == "Max.Bidd", "Purchase"],
                           df3.loc[df3["Group_Name"] == "Avg.Bidd", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

## !! p-value değeri 0.05' ten büyük çıktığı için H0 reddedilemez.


###########################################
# Adım 3 : Bağımsız iki Örneklem T-testi uygulaması
###########################################

test_stat, pvalue = ttest_ind(df3.loc[df3["Group_Name"] == "Max.Bidd", "Purchase"],
                              df3.loc[df3["Group_Name"] == "Avg.Bidd", "Purchase"],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

## !! p-value değeri > 0.05 olduğundan H0 reddedilemez.
## !! Yani , Maximum Bidding ve Average Bidding uygulamaları sonrası oluşan satın alma rakamlarının ortalamaları arasında
## !! Anlamlı bir farklılık yoktur...
