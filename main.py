import streamlit as st
import tensorflow as tf 
import tensorflow_hub as hub
import numpy as np
import pd 

# https://en.wikipedia.org/wiki/Andor_(TV_series)

def load_images():
     content = st.file_uploader("Choose the image to paint!")
     style = st.file_uploader("Choose the style!")
    return content, style

def process_input(img):
  max_dim = 1024
  img = tf.keras.preprocessing.image.img_to_array(img)
  img = tf.image.convert_image_dtype(img, tf.float32)
  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim
  new_shape = tf.cast(shape * scale, tf.int32)
  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  img /= 255.0
  return img

def process_output(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)

def load_model():
    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    return model

# Create the main app
def main():
    st.title("Neural Style Transfer")

    content, style = load_images()


if __name__ == "__main__":
    main()