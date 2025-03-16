import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import ast
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# Load the dataset
df = pd.read_csv("datasets/data_viz1.csv")

# Set the page configuration with a wider layout and title
st.set_page_config(page_title="Property Analytics Dashboard", layout="wide")


city=st.sidebar.selectbox("Select City",["Gurgaon","Kolkata","Mumbai","Chennai","Bangalore"])

# Add a stylish title
st.markdown(f"<h1 style='text-align: center; color: #1E8449;'>{city} Real Estate Analysis</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 2px solid #1E8449;'>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select an Analysis Feature:",
                        ["Price Geomap", "Feature Wordcloud", "Built-up Area Analysis",
                         "Sector-wise Price Trends","View Property"])

# Sidebar Filters
st.sidebar.subheader("Filters")

# Property Type Filter
property_types = ['All'] + list(df['property_type'].unique())
property_type = st.sidebar.selectbox("Select Property Type:", property_types, index=0)

if city=="Gurgaon":

    # Display Different Analysis Based on Selection
    if page == "Price Geomap":
        # BHK Filter (conditional on property type)
        bhk = None  # Initialize bhk outside the conditional block

        bhk_options = ['All'] + sorted(
            df['bedRoom'].dropna().astype(int).unique().tolist())  # Extract bhk options from data
        bhk = st.selectbox("Select BHK for Flat and Bedrooms for House:", bhk_options)

        # Filter the DataFrame based on selections
        filtered_df = df.copy()  # Start with a copy of the original DataFrame

        if property_type == "All":
            filtered_df = filtered_df
        else:
            filtered_df = filtered_df[filtered_df['property_type'] == property_type]

        # Apply BHK filter ONLY for Flats and ONLY if BHK is selected.
        if bhk == "All":
            filtered_df = filtered_df
        else:
            filtered_df = filtered_df[filtered_df['bedRoom'] == bhk]

        # Group the filtered DataFrame
        group_df = filtered_df.groupby('sector')[
            ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()

        # Display the filtered DataFrame (optional)
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

        # Create and display the map
        st.subheader("Property Distribution Map")
        fig = px.scatter_mapbox(
            group_df,
            lat="latitude",
            lon="longitude",
            color="price_per_sqft",
            size='built_up_area',
            color_continuous_scale=px.colors.cyclical.IceFire,
            zoom=10,
            mapbox_style="open-street-map",
            width=1200,
            height=700,
            hover_name=group_df.index,
            title="Average Property Metrics by Sector"  # Title for the plot
        )

        st.plotly_chart(fig, use_container_width=True)



    #Wordcloud
    elif page == "Feature Wordcloud":
        st.subheader("Wordcloud of fetures")
        with open("datasets/wordcloud_df.pkl", "rb") as f:
            # Dump the dictionary to the file
            wordcloud_df=pickle.load(f)

        if property_type=="All":
            wordcloud_df = wordcloud_df
        else:
            wordcloud_df = wordcloud_df[wordcloud_df['property_type'] == property_type]

        # sector
        sector_list=["Overall"] + sorted(df["sector"].unique().tolist())
        sector = st.selectbox("Sector", sector_list)
        if sector=="Overall":
            wordcloud_df=wordcloud_df
        else:
            wordcloud_df=wordcloud_df[wordcloud_df["sector"]==sector]

        main = []
        for item in wordcloud_df['features'].dropna().apply(ast.literal_eval):
            main.extend(item)

        feature_text = ' '.join(main)

        # Generate WordCloud
        wordcloud = WordCloud(
            width=800, height=800,
            background_color='white',
            stopwords=set(['s']),  # Exclude unwanted words
            min_font_size=10
        ).generate(feature_text)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        plt.tight_layout(pad=0)

        # Display in Streamlit
        st.pyplot(fig)


    elif page == "Built-up Area Analysis":
        st.subheader("Built-up Area vs. Price")
        fig = px.scatter(df, x="built_up_area", y="price", color="price_per_sqft",
                         title="Built-up Area vs Price", size="price_per_sqft")
        st.plotly_chart(fig, use_container_width=True)

    elif page == "Sector-wise Price Trends":
        st.subheader("Sector-wise Price Trends")
        sector_price_trends = df.groupby("sector")["price"].mean().reset_index()
        fig = px.line(sector_price_trends, x="sector", y="price", title="Average Price by Sector")
        st.plotly_chart(fig, use_container_width=True)

    elif page == "View Property":
        import streamlit as st
        import pandas as pd
        import ast

        # Load data
        df = pd.read_csv("datasets/gurgaon_properties.csv")


        # Function to safely convert list-like columns
        def parse_list(value):
            if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
                return ast.literal_eval(value)
            return value


        # Convert list-like columns
        df["features"] = df["features"].apply(parse_list)
        df["furnishDetails"] = df["furnishDetails"].apply(parse_list)
        df["rating"] = df["rating"].apply(parse_list)

        st.title("Property View Page")


        # Function to display property details
        def show_property_details(property_name):
            property_details = df[df["property_name"] == property_name].iloc[0]

            # Display property details
            st.header(property_details["property_name"])
            st.write(f"**Type:** {property_details['property_type']}")
            st.write(f"**Price:** ₹{property_details['price']} Lakhs")
            st.write(f"**Price per Sqft:** ₹{property_details['price_per_sqft']}")
            st.write(f"**Area:** {property_details['areaWithType']} sqft")
            st.write(f"**BHK:** {property_details['bedRoom']}")
            st.write(f"**Bathrooms:** {property_details['bathroom']}")
            st.write(f"**Balcony:** {property_details['balcony']}")
            st.write(f"**Floor Number:** {property_details['floorNum']}")
            st.write(
                f"**Facing:** {property_details['facing'] if pd.notna(property_details['facing']) else 'Information not available'}")
            st.write(f"**Age of Property:** {property_details['agePossession']}")
            st.write(f"**Description:** {property_details['description']}")

            # Display Features & Furnishings
            st.subheader("Furnishings")
            st.write("\n".join(property_details["furnishDetails"]) if isinstance(property_details["furnishDetails"],
                                                                                 list) else "Information not available")

            st.subheader("Features")
            st.write("\n".join(property_details["features"]) if isinstance(property_details["features"],
                                                                           list) else "Information not available")

            # Display Ratings
            st.subheader("Ratings")
            if isinstance(property_details["rating"], list):
                for rating in property_details["rating"]:
                    st.write(f"- {rating}")
            else:
                st.write("Information not available")


        # Property selection logic
        property_names = df["property_name"].unique()

        if "selected_property" not in st.session_state or st.session_state.selected_property not in property_names:
            st.session_state.selected_property = property_names[0]  # Default property

        # Dropdown for property selection
        selected_index = list(property_names).index(
            st.session_state.selected_property) if st.session_state.selected_property in property_names else 0
        selected_property = st.selectbox("Select a Property", property_names, index=selected_index)

        # Update session state if selection changes
        if st.session_state.selected_property != selected_property:
            st.session_state.selected_property = selected_property
            st.rerun()

        # Show selected property details
        show_property_details(st.session_state.selected_property)



else:
    st.write("Coming Soon")