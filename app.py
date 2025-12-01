import streamlit as st
from PIL import Image
import google.generativeai as genai
import pandas as pd

GEMINI_API_KEY = "AIzaSyAhDv18duuEzRTW2Y-GuBu574fwcSsRhJo"

genai.configure(api_key=GEMINI_API_KEY) # type: ignore
model = genai.GenerativeModel(model_name="gemini-2.5-flash") # type: ignore

if "data" not in st.session_state:
    st.session_state.data = []


file = st.file_uploader("Upload image of map", type=["png", "jpeg", "jpg"])

if file:
    sat_image = Image.open(file)
    st.image(sat_image)

if st.button("Analyze image"):
    if file:    
        sat_image = Image.open(file)
        with st.spinner("Analyzing image"):
            response = model.generate_content([
                """Analyze the satellite image and return the following:
                [
                {"current_map_state": "the current state of the satellite image place"},
                {"polluted_percentages_after_10_years": [{"oxygen":{"value": value after 10 years, "delta": delta from the last 10 years. can be in minus}, {"CO2": {"value": value after 10 years, "delta": delta from the last 10 years. can be in minus} }, {"greenery": {"value": value after 10 years, "delta": delta from the last 10 years. can be in minus} }]},
                {"advice": "advice for the user"},
                {"non_polluted_percentages_after_10_years": [{"oxygen":{"value": value after 10 years, "delta": delta from the last 10 years. can be in minus}, {"CO2": {"value": value after 10 years, "delta": delta from the last 10 years. can be in minus} }, {"greenery": {"value": value after 10 years, "delta": delta from the last 10 years. can be in minus} }]},
                ]

                the current map state should return the state of the land shown in the uploaded image. it should be simple and describe the pollution and the greenery of the land and the possible causes.
                the dataframes_for_polluted should return the dataframes for the future 10 years of pollution in that placethat show for example oxygen precentages and CO2 and greenery
                the advice should be information on how to reduce pollution on that area
                the dataframes_for_non_polluted should return the dataframes for the future 10 years if you listened for the advice given above that show for example oxygen precentages and CO2 and greenery
                The values should be returned in JSON format only
                """, sat_image
                
            ])
        raw = response.text

            
        import re, json
        match = re.search(r"\[.*\]", raw, flags=re.DOTALL)
        if match:
            json_str = match.group(0)
            st.session_state.data = json.loads(json_str)
            #st.success(str(st.session_state.data))
        else:
            st.error("Model did not return valid JSON.")
            st.write(raw)        
    else:
        st.error("No file found")

if st.session_state.data:
    dictionary = st.session_state.data
    st.header("Current Map State")
    st.write(dictionary[0]["current_map_state"])
    st.header("Polluted Scenario")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Oxygen after 10 years", str(dictionary[1]["polluted_percentages_after_10_years"][0]["oxygen"]["value"]) + "%", delta=dictionary[1]["polluted_percentages_after_10_years"][0]["oxygen"]["delta"])
    with c2:
        st.metric("CO2 after 10 years", str(dictionary[1]["polluted_percentages_after_10_years"][1]["CO2"]["value"]) + "%", delta=dictionary[1]["polluted_percentages_after_10_years"][0]["oxygen"]["delta"])
  

#dictionary[0]["current_map_state"]
