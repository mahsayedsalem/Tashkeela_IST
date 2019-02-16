#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tensorflow as tf
from keras.models import Model
from keras.models import load_model
from keras.optimizers import Adam
from keras.losses import sparse_categorical_crossentropy
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import glob
import string
import re
import pickle
from nltk.tokenize import sent_tokenize, word_tokenize

harakat   = [1614,1615,1616,1618,1617,1611,1612,1613]
connector = 1617

def save_binary(data, file, folder):
    location  = os.path.join(folder, (file+'.pickle'))
    with open(location, 'wb') as ff:
        pickle.dump(data, ff, protocol=pickle.HIGHEST_PROTOCOL)

def load_binary(file, folder):
    location  = os.path.join(folder, (file+'.pickle'))
    with open(location, 'rb') as ff:
        data = pickle.load(ff)
    return data

def get_sentences(data):

    return [sent for line in re.split("[\n,،]+", data) if line for sent in sent_tokenize(line.strip()) if sent]

def clear_punctuations(text):
    text = "".join(c for c in text if c not in string.punctuation)
    return text

def clear_english_and_numbers(text):
     text = re.sub(r"[a-zA-Z0-9٠-٩]", " ", text);
     return text

def is_tashkel(text):
    return any(ord(ch) in harakat for ch in text)

def clear_tashkel(text):
    text = "".join(c for c in text if ord(c) not in harakat)
    return text

def get_harakat():
    return "".join(chr(item)+"|" for item in harakat)[:-1]

def get_taskel(sentence):

    output = []
    current_haraka = ""
    for ch in reversed(sentence):

        if ord(ch) in harakat:
            if (current_haraka is "") or\
            (ord(ch) == connector and chr(connector) not in current_haraka) or\
            (chr(connector) == current_haraka):
                current_haraka += ch
        else:
            if current_haraka == "":
                current_haraka = "ـ"
            output.insert(0, current_haraka)
            current_haraka = ""
    return output

def combine_text_with_harakat(input_sent, output_sent):

    harakat_stack = Stack()
    #process harakat
    for character, haraka in zip(input_sent, output_sent):

        haraka = haraka.replace("<UNK>","").replace("<PAD>","").replace("ـ","")

        if (character == " " and haraka != "" and ord(haraka) == connector):
            combine = harakat_stack.pop()
            combine += haraka
            harakat_stack.push(combine)
        else:
            harakat_stack.push(haraka)

    #fix combine differences
    input_length  = len(input_sent)
    output_length = harakat_stack.size()
    for index in range(0,(input_length-output_length)):
        harakat_stack.push("")

    #combine with text
    text = ""
    for character, haraka in zip(input_sent, harakat_stack.to_array()):
        text += character + "" + haraka

    return text

class Stack:
    def __init__(self):
        self.stack = []

    def isEmpty(self):
        return self.size() == 0

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        if self.size() == 0:
            return None
        else:
            return self.stack[len(self.stack)-1]

    def size(self):
        return len(self.stack)

    def to_array(self):
        return self.stack


class Shakkala:

    def __init__(self, folder_location):

        assert folder_location != None, "model_location cant be empty, send location of keras model"

        model_folder = os.path.join(folder_location, 'model')
        self.max_sentence = 315
        self.model_location = os.path.join(model_folder, ('second_model6' + '.h5'))

        dictionary_folder = os.path.join(folder_location, 'dictionary')
        input_vocab_to_int  = load_binary('input_vocab_to_int',dictionary_folder)
        output_int_to_vocab = load_binary('output_int_to_vocab',dictionary_folder)

        self.dictionary = {
                "input_vocab_to_int":input_vocab_to_int,
                "output_int_to_vocab":output_int_to_vocab}

    # model
    def get_model(self):
        print('start load model')
        model = load_model(self.model_location)
        print('end load model')
        graph = tf.get_default_graph()

        return model, graph

    # input processing

    def prepare_input(self, input_sent):

        assert input_sent != None and len(input_sent) < self.max_sentence, \
        "max length for input_sent should be {} characters, you can split the sentence into multiple sentecens and call the function".format(self.max_sentence)

        input_sent = [input_sent]

        return self.__preprocess(input_sent)

    def __preprocess(self, input_sent):

        input_vocab_to_int = self.dictionary["input_vocab_to_int"]

        input_letters_ids = [[input_vocab_to_int.get(ch, input_vocab_to_int['<UNK>']) for ch in sent] for sent in input_sent]

        input_letters_ids = self.__pad_size(input_letters_ids, self.max_sentence)

        return input_letters_ids

    # output processing

    def logits_to_text(self, logits):
        text = "".join(self.dictionary['output_int_to_vocab'][prediction] for prediction in np.argmax(logits,1))
        return text.replace('<PAD>','')

    def get_final_text(self,input_sent, output_sent):
        return combine_text_with_harakat(input_sent, output_sent)

    def clean_harakat(self, input_sent):
        return clear_tashkel(input_sent)

    # common
    def __pad_size(self, x, length=None):
        return pad_sequences(x, maxlen=length, padding='post')

