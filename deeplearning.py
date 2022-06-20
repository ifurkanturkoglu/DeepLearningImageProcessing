# -*- coding: utf-8 -*-
"""DeepLearning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EXBBDvvoxScvHGHHZq2O2ZuqvSHSJLG0
"""

from google.colab import drive
drive.mount('/content/drive')

zip_adres = "/content/drive/MyDrive/Pet.zip"
!cp "{zip_adres}" .

!unzip -q Pet.zip
!rm Pet.zip

import os
import cv2
from tqdm import tqdm
import numpy
import tensorflow as tf

KATEGORILER = ["Lion", "Tiger"]
DIR = "Pet"
BOYUT = 128
lionLink = os.path.join(DIR,KATEGORILER[0])
tigerLink = os.path.join(DIR,KATEGORILER[1])
veri = []
test = []

for kategori in KATEGORILER:
  klasor_adresi = os.path.join(DIR,kategori)
  deger = KATEGORILER.index(kategori)
  i = 0
  for resim_adi in tqdm(os.listdir(klasor_adresi)):
    resim_adresi = os.path.join(klasor_adresi,resim_adi)
    resim = cv2.imread(resim_adresi, cv2.IMREAD_COLOR)
    if(resim is None):
      print("Hata")
    elif(i <= len(os.listdir(lionLink))*0.8):
      resim = cv2.resize(resim,(BOYUT,BOYUT))
      flipped = tf.image.flip_left_right(resim).numpy()
      veri.append([resim,deger])
      veri.append([flipped,deger])
      i +=1
    else:
      resim = cv2.resize(resim,(BOYUT,BOYUT))
      flipped = tf.image.flip_left_right(resim).numpy()
      test.append([flipped,deger])
      test.append([resim,deger])
print(len(test))
print(len(veri))

from matplotlib import pyplot
pyplot.imshow(cv2.cvtColor(test[6][0], cv2.COLOR_BGR2RGB))

import random
random.shuffle(veri)

X = []
Y = []
testX = []
testY = []

for x,y in veri:
  X.append(x)
  Y.append(y)

for x,y in test:
  testX.append(x)
  testY.append(y)


del test
del veri

pyplot.imshow(cv2.cvtColor(X[99], cv2.COLOR_BGR2RGB))
print(Y[99])

import numpy

X = numpy.array(X).reshape(-1,BOYUT,BOYUT,3)
Y = numpy.array(Y).reshape(-1,1)

testX = numpy.array(testX).reshape(-1,BOYUT,BOYUT,3)
testY = numpy.array(testY).reshape(-1,1)

pyplot.imshow(cv2.cvtColor(X[2], cv2.COLOR_BGR2RGB),cmap='gray')

X = X / 255.0
testX = testX / 255.0

from tensorflow.keras import optimizers
from tensorflow.keras import Sequential
from tensorflow.keras import layers
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Conv2D, Activation, BatchNormalization, Flatten, Dense, MaxPool2D

model = Sequential()


model.add(Conv2D(filters=16,kernel_size=(3,3),input_shape=X[0].shape,activation='relu'))
model.add(MaxPool2D((2,2)))
model.add(Conv2D(filters=32,kernel_size=(3,3),activation='relu'))
model.add(MaxPool2D((2,2)))
model.add(Conv2D(filters=64,kernel_size=(3,3),activation='relu'))
model.add(MaxPool2D((2,2)))
model.add(Conv2D(filters=128,kernel_size=(3,3),activation='relu'))
model.add(MaxPool2D((2,2)))
model.add(BatchNormalization())
model.add(Flatten())


model.add(Dense(32,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['acc'])

mc = ModelCheckpoint('en_iyi.h5',save_best_only=True,monitor='val_loss',mode='min')

model.fit(X,Y,batch_size=32,epochs=100,shuffle=True,validation_split=0.125,callbacks=[mc])

from matplotlib import pyplot

pyplot.figure(figsize=(4,4))
pyplot.plot(model.history.history['acc'])
pyplot.plot(model.history.history['val_acc'])
pyplot.title('Model Doğruluk Oranı')
pyplot.ylabel('Accuracy')
pyplot.xlabel('Epoch')
pyplot.legend(['Train','Validation'], loc='lower right')
pyplot.savefig('sema.png',dpi=300)
print(max(model.history.history['val_acc']))

model.save('model.h5')

from tensorflow.keras.models import load_model
yuklenen_model = load_model('en_iyi.h5')

from tensorflow import keras


test_model = keras.models.load_model("en_iyi.h5")

test_loss, test_acc = test_model.evaluate(testX,testY) 

print(f"Test accuracy: {test_acc:.3f}")

from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(Y,yuklenen_model.predict(X).round()))
print(classification_report(Y,yuklenen_model.predict(X).round()))

print(confusion_matrix(testY,yuklenen_model.predict(testX).round()))
print(classification_report(testY,yuklenen_model.predict(testX).round()))

print(yuklenen_model.predict(testX)[2])
pyplot.imshow(testX[2])