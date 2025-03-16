import numpy as np
import streamlit as st
import pickle
import pandas as pd


st.set_page_config(page_title="Recomender System")

with open("datasets/location_distance.pkl", "rb") as file:
    location_df = pickle.load(file)

with open("datasets/cosine_sim1.pkl", "rb") as file:
    cosine_sim1 = pickle.load(file)
with open("datasets/cosine_sim2.pkl", "rb") as file:
    cosine_sim2 = pickle.load(file)
with open("datasets/cosine_sim3.pkl", "rb") as file:
    cosine_sim3 = pickle.load(file)


def recommend_properties_with_scores(property_name, top_n=247):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 +  1* cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df


st.title("Select Location and Radius")

selected_location=st.selectbox("Loaction",sorted(location_df.columns.to_list()))
radius=st.number_input("Radius in Kms")

if st.button("Search"):
    res_series=location_df[location_df[selected_location] <= radius*1000 ][selected_location].sort_values()
    if res_series.empty:
        st.text("❌ No properties within the selected radius.")
    else:
        for key, value in res_series.items():
            st.text(f"{key}     {value / 1000:.2f} Kms")


st.title("Recomend Appartment")
selected_apartment = st.selectbox('Select an apartment', sorted(location_df.index.to_list()))
if st.button('Recommend'):
        recommendation_df = recommend_properties_with_scores(selected_apartment)
        st.dataframe(recommendation_df.head())
