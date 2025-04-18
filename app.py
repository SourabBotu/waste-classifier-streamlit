from tensorflow import keras
import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import gdown
import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image

# Categories dictionary (adjust if needed)
categories = {0: 'paper', 1: 'cardboard', 2: 'plastic', 3: 'metal', 4: 'trash', 5: 'battery',
              6: 'shoes', 7: 'clothes', 8: 'green-glass', 9: 'brown-glass', 10: 'white-glass',
              11: 'biological'}

# Streamlit UI
st.title("♻️ Waste Classification using Inception CNN")
st.markdown("Upload a waste image and classify it into one of 12 categories.")

# Load model from Google Drive (only once)
@st.cache_resource
def load_my_model():
    file_id = "YOUR_FILE_ID_HERE"  # replace this
    url = f"https://drive.google.com/uc?id=1Fr52uS7ZpEhXjpCejjYzjD9rIQcjWK2l"
    output = "best_model_inception.keras"
    if not os.path.exists(output):
        with st.spinner("Downloading model..."):
            gdown.download(url, output, quiet=False)
    model = tf.keras.models.load_model(output)
    return model

model = load_my_model()

# Image preprocessing function
def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = img_to_array(img)
    img_array = img_array / 255.0  # rescale
    img_array = np.expand_dims(img_array, axis=0)  # make it (1, 224, 224, 3)
    return img_array

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Predict
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image)
    predicted_class = np.argmax(prediction)
    class_name = categories[predicted_class]
    confidence = np.max(prediction) * 100

    st.success(f"Predicted class: **{class_name}**")
    st.write(f"Confidence: **{confidence:.2f}%**")
