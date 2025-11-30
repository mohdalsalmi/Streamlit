import streamlit as st
from PIL import Image
import google.generativeai as genai
import pandas as pd
from numpy.random import default_rng as rng


if "summary" not in st.session_state:
    st.session_state.summary = ""


# Hard-code your Gemini API key **only if you're comfortable and understand the risk**
GEMINI_API_KEY = "AIzaSyDpwsxQ8mw7g4KZYburruvHd9Qbx-prQPU"

genai.configure(api_key=GEMINI_API_KEY) # type: ignore
model = genai.GenerativeModel(model_name="gemini-2.5-flash") # type: ignore



st.title("Image Summarizer")

uploaded_file = st.file_uploader("Upload Image", type=(["jpg", "png", "jpeg"]))

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

if st.button("Summarize Image"):
    if uploaded_file:
        image = Image.open(uploaded_file)
        with st.spinner("Summarizing image..."):
            response = model.generate_content(
                [
                    "Summarize the contents of this image: ", image
                ]
            )
        
        st.session_state.summary = response.text
        st.toast("Summary Ready!")
    else:
        st.error("Please upload an image first")

if st.session_state.summary:
    summary = st.session_state.summary
    st.subheader("Summary")
    st.success(summary)
    st.download_button("Download Summary", summary, "Summary.txt", "text/plain")

