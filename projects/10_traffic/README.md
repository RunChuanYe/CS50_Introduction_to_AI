## practice 1

config:

- 1 convolutional layer with 32 filters and a 3x3 kernel
- 1 max-pooling layer with 2x2 pool size,
- 1 hidden layer with 128 units
- 1 0.5 dropout.

res:

```
Epoch 1/10
500/500 [==============================] - 16s 31ms/step - loss: 4.9024 - accuracy: 0.0502
Epoch 2/10
500/500 [==============================] - 16s 32ms/step - loss: 3.5863 - accuracy: 0.0522
Epoch 3/10
500/500 [==============================] - 16s 31ms/step - loss: 3.5363 - accuracy: 0.0557
Epoch 4/10
500/500 [==============================] - 15s 30ms/step - loss: 3.5131 - accuracy: 0.0554
Epoch 5/10
500/500 [==============================] - 15s 30ms/step - loss: 3.5026 - accuracy: 0.0568
Epoch 6/10
500/500 [==============================] - 15s 30ms/step - loss: 3.4976 - accuracy: 0.0568
Epoch 7/10
500/500 [==============================] - 15s 30ms/step - loss: 3.4951 - accuracy: 0.0546
Epoch 8/10
500/500 [==============================] - 15s 31ms/step - loss: 3.4940 - accuracy: 0.0560
Epoch 9/10
500/500 [==============================] - 15s 31ms/step - loss: 3.4933 - accuracy: 0.0557
Epoch 10/10
500/500 [==============================] - 15s 30ms/step - loss: 3.4931 - accuracy: 0.0554
333/333 - 9s - loss: 3.5058 - accuracy: 0.0556 - 9s/epoch - 26ms/step
```

From the result, the accuracy of the current model is very low; And the complexity of the model is also relatively low. It should be that the model is too simple to lead to the above results.

## practice 2


config:

- 2 convolutional layer with 32 filters and a 3x3 kernel
- 2 max-pooling layer with 2x2 pool size,
- 4 hidden layer with 128 units
- 1 0.5 dropout.

res:

```
Epoch 1/10
500/500 [==============================] - 7s 13ms/step - loss: 2.5468 - accuracy: 0.3855
Epoch 2/10
500/500 [==============================] - 7s 14ms/step - loss: 0.7984 - accuracy: 0.7691
Epoch 3/10
500/500 [==============================] - 7s 14ms/step - loss: 0.3964 - accuracy: 0.8875
Epoch 4/10
500/500 [==============================] - 7s 14ms/step - loss: 0.2606 - accuracy: 0.9291
Epoch 5/10
500/500 [==============================] - 7s 13ms/step - loss: 0.2222 - accuracy: 0.9432
Epoch 6/10
500/500 [==============================] - 7s 14ms/step - loss: 0.1715 - accuracy: 0.9580
Epoch 7/10
500/500 [==============================] - 7s 13ms/step - loss: 0.1753 - accuracy: 0.9555
Epoch 8/10
500/500 [==============================] - 7s 14ms/step - loss: 0.1402 - accuracy: 0.9662
Epoch 9/10
500/500 [==============================] - 7s 13ms/step - loss: 0.1190 - accuracy: 0.9717
Epoch 10/10
500/500 [==============================] - 7s 13ms/step - loss: 0.1402 - accuracy: 0.9677
333/333 - 1s - loss: 0.0880 - accuracy: 0.9793 - 1s/epoch - 4ms/step
```

It can be seen from the above results that the accuracy rate has been significantly improved by increasing the complexity of the model, and reached 97%, which is acceptable.And the dropout rate is 0.5, so the generalization ability of the model can also be guaranteed, and there should be no over-fitting.

## practice 3

config:

- 2 convolutional layer with 32 filters and a 3x3 kernel
- 2 max-pooling layer with 2x2 pool size,
- 6 hidden layer with 128 units
- 2 0.5 dropout.

```
Epoch 1/10
500/500 [==============================] - 8s 14ms/step - loss: 3.2565 - accuracy: 0.1572  
Epoch 2/10
500/500 [==============================] - 6s 13ms/step - loss: 1.8309 - accuracy: 0.4460
Epoch 3/10
500/500 [==============================] - 7s 14ms/step - loss: 1.1950 - accuracy: 0.6103
Epoch 4/10
500/500 [==============================] - 7s 14ms/step - loss: 0.8477 - accuracy: 0.7182
Epoch 5/10
500/500 [==============================] - 7s 13ms/step - loss: 0.6928 - accuracy: 0.7757
Epoch 6/10
500/500 [==============================] - 7s 14ms/step - loss: 0.5601 - accuracy: 0.8245
Epoch 7/10
500/500 [==============================] - 7s 14ms/step - loss: 0.4632 - accuracy: 0.8555
Epoch 8/10
500/500 [==============================] - 7s 13ms/step - loss: 0.4322 - accuracy: 0.8750
Epoch 9/10
500/500 [==============================] - 7s 14ms/step - loss: 0.4031 - accuracy: 0.8891
Epoch 10/10
500/500 [==============================] - 7s 13ms/step - loss: 0.3060 - accuracy: 0.9150
333/333 - 1s - loss: 0.2545 - accuracy: 0.9483 - 1s/epoch - 4ms/step

```
The model is more complex than before, but in order to over-fit, I also added a layer of dropout, but the accuracy rate has decreased, which may be the problem of dropout. So I conducted another test and changed the dropout to 1 layer.

## practice 4

config:

- 2 convolutional layer with 32 filters and a 3x3 kernel
- 2 max-pooling layer with 2x2 pool size,
- 6 hidden layer with 128 units
- 1 0.5 dropout.

```
Epoch 1/10
500/500 [==============================] - 7s 12ms/step - loss: 2.3313 - accuracy: 0.3599
Epoch 2/10
500/500 [==============================] - 6s 12ms/step - loss: 0.8935 - accuracy: 0.7180
Epoch 3/10
500/500 [==============================] - 6s 12ms/step - loss: 0.5030 - accuracy: 0.8492
Epoch 4/10
500/500 [==============================] - 6s 12ms/step - loss: 0.3580 - accuracy: 0.8995
Epoch 5/10
500/500 [==============================] - 6s 12ms/step - loss: 0.2514 - accuracy: 0.9314
Epoch 6/10
500/500 [==============================] - 6s 11ms/step - loss: 0.2268 - accuracy: 0.9433
Epoch 7/10
500/500 [==============================] - 6s 12ms/step - loss: 0.1747 - accuracy: 0.9576
Epoch 8/10
500/500 [==============================] - 6s 12ms/step - loss: 0.1184 - accuracy: 0.9713
Epoch 9/10
500/500 [==============================] - 6s 12ms/step - loss: 0.1425 - accuracy: 0.9670
Epoch 10/10
500/500 [==============================] - 6s 12ms/step - loss: 0.1371 - accuracy: 0.9695
333/333 - 1s - loss: 0.1356 - accuracy: 0.9674 - 1s/epoch - 4ms/step
```
This experiment confirmed my guess. After removing one layer of dropout, the accurate drop-out rate is about the same as Practice 2. However, compared with Practice 2, the model here is more complex and prone to the risk of over-fitting, so I finally chose Practice 2 model.

## Finally

As mentioned above, the accuracy of practice 2 and practice 4 are acceptable, but the latter is more complex than the former, so I choose the former model to avoid over-fitting.