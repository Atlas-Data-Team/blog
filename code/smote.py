#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 22:19:35 2021

@author: akate
"""
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import metrics

df = pd.read_csv("creditcard.csv")

feature_columns = df.columns[:-1]
df.columns

"""## Brief description"""

df.head()

#label = df["Class"]
#df.describe()

#df.info()

#print(f"Percentile of fraud transactions : {label.sum() / df.shape[0]}")
'''
ax = sn.countplot(x="Class", data=df)
for p in ax.patches:
  ax.annotate(p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),\
              ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points')
plt.title("Count plot for transactions")
plt.xticks([0, 1], ["Normal", "Fraud"])
plt.show()


fig, ax = plt.subplots(1, 2, figsize=(18,4))

amount_val = df['Amount'].values
time_val = df['Time'].values

sn.displot(amount_val, ax=ax[0], color='r')
ax[0].set_title('Distribution of Transaction Amount', fontsize=14)
ax[0].set_xlim([min(amount_val), max(amount_val)])
ax[0].set_xlabel("Amount($)")

sn.histplot(time_val, ax=ax[1], color='b')
ax[1].set_title('Distribution of Transaction Time', fontsize=14)
ax[1].set_xlim([min(time_val), max(time_val)])
ax[1].set_xlabel("Elapsed time(ms)")

plt.show()

fig = plt.figure(figsize=(12,6))
ax1 = fig.add_axes([0, 0, 1, 1])
sn.distplot(amount_val, ax=ax1, color='r')
ax1.set_xlim([min(amount_val), max(amount_val)])
plt.title("Distribution of Transaction Amount", fontsize=14)
plt.xlabel("Amount($)")
plt.show()

fig = plt.figure(figsize=(12,6))
ax2 = fig.add_axes([0, 0, 1, 1])
sn.distplot(time_val, ax=ax2, color='b')
ax2.set_xlim([min(time_val), max(time_val)])
plt.title("Distribution of Transaction Time", fontsize=14)
plt.xlabel("Elapsed Time(ms)")
plt.show()

plt.figure(figsize=(16, 10))
corr = df.corr()
sn.heatmap(corr, cmap='coolwarm_r', annot_kws={'size':20})
plt.title("Imbalanced Correlation Matrix \n (don't use for reference)", fontsize=14)
plt.show()
'''

def evaluate_result(actual, predict):
  confusion_matrix = metrics.confusion_matrix(actual, predict)
  accuracy_score = metrics.accuracy_score(actual, predict)
  precision_score = metrics.precision_score(actual, predict)
  recall_score = metrics.recall_score(actual, predict)
  f1_score = metrics.f1_score(actual, predict)
  
  sn.heatmap(confusion_matrix,cbar=False,annot=True,square=True,fmt="d")
  plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True)
  plt.xlabel("Predicted")
  plt.ylabel("Actual")

  print("accuracy:",accuracy_score)
  print("precision:",precision_score)
  print("recall:",recall_score)
  print("f1 score:",f1_score)

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

train, test = train_test_split(df, train_size=0.7, random_state=0)
x_train, y_train = train[feature_columns], train["Class"]
x_test, y_test = test[feature_columns], test["Class"]

from  imblearn.over_sampling  import  SMOTE
from collections import Counter

oversample = SMOTE()
X_new , y_new = oversample.fit_resample(df[feature_columns], df["Class"])

counter = Counter(y_new)
print(counter)

ax = sn.countplot(y_new)
plt.title("Count plot for Class after resampling")
for p in ax.patches:
  ax.annotate(p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),\
              ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points')
plt.xlabel("Class")
plt.xticks([0, 1], ["Normal", "Fraud"])
plt.show()

resampled = pd.DataFrame(data=X_new, columns=feature_columns)
resampled["Class"] = y_new

# NEw
new_corr = resampled.corr()

plt.figure(figsize=(16, 10))
sn.heatmap(new_corr, cmap='coolwarm_r', annot_kws={'size':20})
plt.title("Balanced Correlation Matrix", fontsize=14)
plt.show()

corr_class_sr = new_corr["Class"].abs()
corr_class_sr.describe()

filtered = corr_class_sr.where(corr_class_sr>0.1).dropna()
corr_columns = filtered.keys().drop(["Class"])
corr_columns

x2_train, x2_test, y2_train, y2_test = train_test_split(X_new, y_new, test_size=0.3, random_state=0)

print(f"Train shape: {x2_train.shape}, Test shape: {x2_test.shape}")


### Random Forest Classifier

rf_clf = RandomForestClassifier(max_depth=2, random_state=0)
rf_clf.fit(x2_train, y2_train)

y2_pred = rf_clf.predict(x2_test)

evaluate_result(y2_test, y2_pred)

### Logistic Regression"""

lr_clf = LogisticRegression(random_state=0, max_iter=1e5).fit(x2_train, y2_train)

lr_y2_pred = lr_clf.predict(x2_test)

evaluate_result(y2_test, lr_y2_pred)




