import pandas as pd
import tensorflow as tf

from tensorflow.keras.layers import Input, Dropout, Dense
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.metrics import AUC
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.models import load_model
from keras.models import model_from_json

from transformers import BertModel, BertTokenizer, BertConfig, BertForSequenceClassification, TFBertModel
import ast
import re
from Analyze.Preprocessing import preprocess_text



class ModelOperations():
    def __init__(self, text: pd.Series):
        self.text = text
        self.pp_text = preprocess_text(self.text)
        self.pred = None
        self.result = None
        self.polarities = None
        self.aspects = None
        self.review_count = len(self.text)

    def predict(self):
        loaded_model = self.load_configured_model()

        test_dataset = self.get_test_dataset()
        self.pred = loaded_model.predict(test_dataset)
        label_names, labels = self.get_labels()
        self.get_results(test_dataset=test_dataset, label_names=label_names)
        self.edit_results()

        return self.result, self.polarities, self.aspects, self.pp_text, self.review_count

    def load_configured_model(self):
        # load json and create model
        json_file = open('Analyze/Models/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("Analyze/Models/model.h5")
        print("Loaded model from disk")

        return loaded_model

    def get_test_dataset(self):
        MODEL_NAME = 'dbmdz/bert-base-turkish-128k-cased'
        MAX_LENGTH = 39  # We truncate anything after the 200-th word to speed up training

        tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

        test_encodings = tokenizer(self.pp_text, truncation=True, padding='max_length',
                                   max_length=MAX_LENGTH, return_tensors="tf")

        test_dataset = tf.data.Dataset.from_tensor_slices(test_encodings['input_ids']).batch(1)
        return test_dataset

    def get_results(self, test_dataset, label_names):
        result = []
        print("Sample prediction")
        threshold = 0.4
        i = 0
        for prediction, a in zip(self.pred, test_dataset):
            self.pred[self.pred > threshold] = 1
            self.pred[self.pred <= threshold] = 0
            convert_result = str(self.convert(label_names, prediction))
            result.append(convert_result)

        self.result = result

    def convert(self, label_string, label_onehot):
        labels = []
        for i, label in enumerate(label_string):
            if label_onehot[i]:
                labels.append(label)
        if len(labels) == 0:
            labels.append("neutral - RESTAURANT#GENERAL")
        return labels

    def edit_results(self):
        # Removing strings
        self.result = [ast.literal_eval(res) for res in self.result]
        # Merging outer list with inner list
        self.result = [j for i in self.result for j in i]

        # Extracting polarities
        regex_pol = r'[a-z]+\w'
        self.polarities = [re.findall(regex_pol, res) for res in self.result]
        self.polarities = [j for i in self.polarities for j in i]

        # Extracting aspect
        regex_asp = r'[A-Z#]+\w'
        self.aspects = [re.findall(regex_asp, res) for res in self.result]
        self.aspects = [j for i in self.aspects for j in i]

    @staticmethod
    def get_labels(file_name='re-designed_train_df.csv'):
        re_designed_df = pd.read_csv('Analyze/re-designed_train_df.csv')
        re_designed_df.drop('Unnamed: 0', inplace=True, axis=1)
        label_names = re_designed_df.drop(["SID", "lemmatized"], axis=1).columns
        labels = re_designed_df[label_names].values

        return label_names, labels


