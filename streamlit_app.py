import streamlit as st
import leafmap.foliumap as leafmap
import pandas_gbq
from google.oauth2 import service_account
from google.cloud import bigquery
import geopandas as gpd

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Web App URL: <https://template.streamlitapp.com>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("Streamlit for Geospatial Applications")

st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/giswqs/streamlit-multipage-template).
    """
)

st.header("Instructions")

@st.experimental_memo(persist="disk")
def fetch_and_clean_data():
    # Fetch data from URL here, and then clean it up.
    query = """
            SELECT * FROM `dev-ind-geo-01.enriched.data_subdistricts`
            """
    data = pandas_gbq.read_gbq(query, credentials=credentials)
    return data

df=fetch_and_clean_data()
st.dataframe(df)

st.markdown(markdown)

level = st.select_slider(
     'Select a level of the data',
     options=['Country', 'States', 'Districts', 'Subdistricts', 'Parlamentary Constituencies', 'Assembly Consituencies'])
st.write('My favorite Level is', level)

topic = st.radio('Topic', options=['Roads','Habitations','Facilities','Proposals','Buildings','OpenStreetMap PoIs'],horizontal=True)
st.write('Count how many of ',topic,' are available.')


# set level in query
if level == 'Country':

    pass
elif level == 'States':

    pass
elif level == 'Districts':

    pass
elif level == 'Subdistricts':

    pass
elif level == 'Parlamentary Constituencies':
    pass
elif level == 'Assembly Consituencies':
    pass


# set topic in query
if topic == 'Roads':

    pass
elif topic == 'Habitations':

    pass
elif topic == 'Facilities':

    pass
elif topic == 'Proposals':

    pass
elif topic == 'Buildings':

    pass
elif topic == 'OpenStreetMap PoIs':

    pass


# activate map with button ?
m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
