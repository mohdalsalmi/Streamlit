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
                {"dataframes_for_polluted": [{"oxygen":"dataframe for oxygen ,example: {"2025": 12, "2026", 14}"}, {"CO2": "dataframe for CO2"}, {"greenery": "dataframe"}]},
                {"advice": "advice for the user"},
                {"dataframes_for_non_polluted": [{"oxygen":"dataframe for oxygen ,example: {"2025": 12, "2026", 14}"}, {"CO2": "dataframe for CO2"}, {"greenery": "dataframe"}]},
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

    st.header("Dataframes for Polluted Scenario")
    st.subheader("Oxygen Levels Over 10 Years")
    oxygen_polluted_dfs = pd.DataFrame.from_dict(dictionary[1]["dataframes_for_polluted"][0]["oxygen"], orient='index', columns=['Oxygen Level (%)'])
    st.line_chart(oxygen_polluted_dfs)



#dictionary[0]["current_map_state"]
