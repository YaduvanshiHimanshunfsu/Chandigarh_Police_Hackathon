import tensorflow as tf

print(tf.__version__)

from tensorflow.keras.applications import MobileNetV2

model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)

print("MobileNetV2 loads successfully!")