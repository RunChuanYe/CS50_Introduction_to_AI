# 10_Traffic

Write an AI to identify which traffic sign appears in a photograph.

## 10.1 guide

dataset:

https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip

smaller dateset:
https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb-small.zip

- `opencv-python` for image processing
- `scikit-learn` for ML-related functions
- `tensorflow` for neural networks.


## 10.2 task

note:

- Once you’ve resized an image img, you can verify its dimensions by printing the value of `img.shape`. If you’ve resized the image correctly, its shape should be (30, 30, 3) (assuming IMG_WIDTH and IMG_HEIGHT are both 30).
- Check out the official Tensorflow Keras overview for some guidelines for the syntax of **building neural network layers**. You may find the lecture source code useful as well.
- The OpenCV-Python documentation may prove helpful for **reading images as arrays and then resizing them.**
- **smaller dataset** for practicing

pkg:

`python -m pip install opencv-python`