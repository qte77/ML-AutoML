# -*- coding: utf-8 -*-
"""AutoGluon.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qDY_em1xGtnKbvTb3K4YguBixbpKAa1z

Source: https://www.analyticsvidhya.com/blog/2021/10/beginners-guide-to-automl-with-an-easy-autogluon-example/
"""

gdrive = '/gdrive'
save_dir = f'{gdrive}/MyDrive'
keyfile = 'conf/kaggle.json'

dataset_dir = f'{save_dir}/Datasets'
kaggle_ds_src = 'stroke-prediction-dataset'
kaggle_ds_fn = f'healthcare-dataset-stroke-data.csv'
kaggle_dest = f'{dataset_dir}/{kaggle_ds_src}'
environ['kaggle_ds_src'] = 'stroke-prediction-dataset'
environ['kaggle_ds_url'] = f'fedesoriano/{kaggle_ds_src}'
environ['kaggle_dest'] = kaggle_dest
environ['kaggle_ds_fn'] = kaggle_ds_fn

model_save_dir = f'{save_dir}/Models'
model_autogluon_dir = './AutogluonModels'

!pip install -q kaggle

!pip install -q autogluon

from google.colab import drive
import json 
from os import environ
from shutil import copytree

import pandas as pd
import kaggle
from sklearn.model_selection import train_test_split #splitting the dataset
from autogluon.tabular import TabularDataset, TabularPredictor #to handle tabular data and train models

drive.mount(gdrive)

with open(f"{save_dir}/{keyfile}", 'r') as j:
 data = json.loads(j.read())
 environ['KAGGLE_USERNAME'] = data['username']
 environ['KAGGLE_KEY'] = data['key']

# Commented out IPython magic to ensure Python compatibility.
# %%shell
# mkdir -p $kaggle_dest
# if [ ! -f $kaggle_dest/$kaggle_ds_fn ]; then
#   kaggle d download -p $kaggle_dest --unzip $kaggle_ds_url
# else
#   echo "$kaggle_ds_fn found. skipping"
# fi
# #unzip -n $kaggle_src -d $kaggle_src
# #rm -f $kaggle_srcn
# #ls -la

df=pd.read_csv(f'{kaggle_dest}/{kaggle_ds_fn}')

df_train, df_test = train_test_split(df, test_size = 0.33, random_state = 1)
print(df_train.shape, df_test.shape)

df.head()

test_data = df_test.drop(['stroke'], axis = 1)
test_data.head()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# predictor = TabularPredictor(label = 'stroke').fit(
#     train_data = df_train,
#     verbosity = 2,
#     presets = 'best_quality'
#   )

# Commented out IPython magic to ensure Python compatibility.
# %%time
# predictor.fit_summary()

# Commented out IPython magic to ensure Python compatibility.
# %%time
# y_pred = predictor.predict(test_data)
# y_pred = pd.DataFrame(y_pred, columns = ['stroke'])
# print(y_pred)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# eval = predictor.evaluate(df_test)

predictor.leaderboard()

predictor.persist_models()
predictor.save_space()

try:
  copytree(
      src = model_autogluon_dir,
      dst = f'{model_save_dir}/{model_autogluon_dir}',
      # dirs_exist_ok = True
  )
except Exception as e:
  print(e.args)

