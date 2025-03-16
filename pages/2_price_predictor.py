import numpy as np
import streamlit as st
import pickle
import pandas as pd


st.set_page_config(page_title="HomeScout")




city=st.selectbox("Select City",["Gurgaon","Kolkata","Mumbai","Chennai","Bangalore"])

if city=="Gurgaon":
    with open("df.pkl","rb") as file:
        df=pickle.load(file)

    with open("pipeline.pkl","rb") as file:
        pipeline=pickle.load(file)


    st.header("Enter the inputs below ")

    # property_type
    property_type = st.selectbox("Property Type", df["property_type"].unique().tolist())

    # sector
    sector = st.selectbox("Sector", df["sector"].unique().tolist())

    # bedRoom
    bedRoom = float(st.selectbox("Bedroom", df["bedRoom"].unique().tolist()))

    # bathroom
    bathroom = float(st.selectbox("Bathroom", df["bathroom"].unique().tolist()))

    # balcony
    balcony = st.selectbox("Balcony", df["balcony"].unique().tolist())

    # agePossession
    agePossession = st.selectbox("Age Possession", df["agePossession"].unique().tolist())

    # built_up_area
    built_up_area = float(st.number_input("Built-up Area (sqft)"))

    # servant room
    option_mapping = {"Yes": 1.0, "No": 0.0}
    selected_option = st.selectbox("Servant Room", list(option_mapping.keys()))
    servant_room = option_mapping[selected_option]

    # store room
    option_mapping = {"Yes": 1.0, "No": 0.0}
    selected_option = st.selectbox("Store Room", list(option_mapping.keys()))
    store_room = option_mapping[selected_option]

    # furnishing_type
    furnishing_type = st.selectbox("Furnishing Type", df["furnishing_type"].unique().tolist())

    # luxury_category
    luxury_category = st.selectbox("Luxury Category", df["luxury_category"].unique().tolist())

    # floor_category
    floor_category = st.selectbox("Floor Category", df["floor_category"].unique().tolist())



    #add a button
    button=st.button("Predict")

    if button:
        # Creating the DataFrame
        data = pd.DataFrame({
            "property_type": [property_type],
            "sector": [sector],
            "bedRoom": [bedRoom],
            "bathroom": [bathroom],
            "balcony": [balcony],
            "agePossession": [agePossession],
            "built_up_area": [built_up_area],
            "servant room": [servant_room],
            "store room": [store_room],
            "furnishing_type": [furnishing_type],
            "luxury_category": [luxury_category],
            "floor_category": [floor_category]
        })

        # Display DataFrame in Streamlit
        st.dataframe(data)

        # Make prediction
        try:
            predicted_price = np.expm1(pipeline.predict(data))[0]
            st.success(f"💰 **Estimated Price: ₹{predicted_price:,.2f} cr**")
        except Exception as e:
            st.error("⚠️ An error occurred while predicting the price.")
            st.text(str(e))


if city!="Gurgaon":
    st.write("Comming Soon !")