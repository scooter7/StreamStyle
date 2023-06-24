#structural libraries
import streamlit as st
import io
from PIL import Image
from io import BytesIO
import requests

#model specific libraries
import tensorflow as tf 
import tensorflow_hub as hub
import numpy as np
import pandas as pd 

def load_images():
    content_img = st.file_uploader("Choose the image to paint!")
    style_img = st.file_uploader("Choose the style!")
    if content_img:
            cont = content_img.getvalue()
            content_img = Image.open(io.BytesIO(cont))
            print('p')
    if style_img: 
            styl = style_img.getvalue()   
            style_img = Image.open(io.BytesIO(styl))
            print('p')
    
    return content_img, style_img


def process_input(img):
  
  img = tf.keras.preprocessing.image.img_to_array(img)
  
  # Check if image has 4 channels (RGBA), if so, convert to RGB
  if img.shape[-1] == 4:
    img = img[:,:,:3]

  img = tf.image.convert_image_dtype(img, tf.float32)
  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  
  scale = 1024 / max(shape)
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
  return Image.fromarray(tensor)

def load_model():
    model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    return model

def NST(model, content, style):
    t_content = process_input(content)
    t_style = process_input(style)
    out = model(tf.constant(t_content), tf.constant(t_style))[0]
    result = process_output(out)
    return result

def outputs(style, content, styled_img):
    col1, col2, col3 = st.columns([0.25, 0.25, 0.25])
    with col1:
        st.write('Content image')
        st.image(content)
    with col2:
        st.write('Style image')
        st.image(style)
    with col3:
        st.write('Stylized image')
        st.image(styled_img)

# Create the main app
def main():
    #Title and column
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">StreamStyle</p>', unsafe_allow_html=True)
    

    content, style = load_images()
    if content and style:
        model = load_model()
        styled_img = NST(model, content, style)
        outputs(style, content, styled_img)
        buf = BytesIO()
        styled_img.save(buf, format="JPEG")
        byte_im =buf.getvalue()
        st.download_button(
            label="Download Image",
            data=byte_im,
            file_name="styled_img"+".jpg",
            mime="image/jpg"
            )


if __name__ == "__main__":
    main()
