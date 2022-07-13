import streamlit as st
import leafmap.foliumap as leafmap
import pandas_gbq
from google.oauth2 import service_account
from google.cloud import bigquery
import geopandas as gpd
import pandas as pd

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
def fetch_enriched_data():
    # Fetch data from URL here, and then clean it up.
    query = """
            SELECT * FROM `dev-ind-geo-01.enriched.data_subdistricts`
            """
    data = pandas_gbq.read_gbq(query, credentials=credentials)
    return data

@st.experimental_memo(persist="disk")
def fetch_boundary_data():
    country = pandas_gbq.read_gbq("SELECT country_code,country_name,geom_text FROM dev-ind-geo-01.geoprocessed.country", credentials=credentials)
    states = pandas_gbq.read_gbq("SELECT state_code,state_name,geom_text FROM dev-ind-geo-01.geoprocessed.states", credentials=credentials)
    districts = pandas_gbq.read_gbq("SELECT district_code,district_name,geom_text FROM dev-ind-geo-01.geoprocessed.districts", credentials=credentials)
    subdistricts = pandas_gbq.read_gbq("SELECT taluk_code,taluk_name,geom_text FROM dev-ind-geo-01.geoprocessed.subdistricts", credentials=credentials)
    return country,states,districts,subdistricts

df=fetch_enriched_data()
st.dataframe(df)
outdf = pd.DataFrame()
st.write(pd.__version__)

country_df,states_df,districts_df,subdistricts_df = fetch_boundary_data()

st.markdown(markdown)

level = st.select_slider(
     'Select a level of the data',
     options=['Country', 'States', 'Districts', 'Subdistricts', 'Parlamentary Constituencies', 'Assembly Consituencies'])
st.write('My favorite Level is', level)

topic = st.radio('Topic', options=['Roads','Habitations','Facilities','Proposals','Buildings','OpenStreetMap PoIs'],horizontal=True)
st.write('Count how many of ',topic,' are available.')


# set level in query
if level == 'Country':
    # group by country code
    group_attr = ['country_code']
    pass
elif level == 'States':
    # group by state code
    group_attr = ['state_code']
    pass
elif level == 'Districts':
    # group by district code
    group_attr = ['district_code']
    pass
elif level == 'Subdistricts':
    # group by subdistrict code
    group_attr = ['taluk_code']
    pass
elif level == 'Parlamentary Constituencies':
    # group by pc code
    pass
elif level == 'Assembly Consituencies':
    # group by ac code
    pass


# set topic in query
if topic == 'Roads':
    # count number of roads
    outdf = df.groupby(group_attr).agg(cnt = ('roadcnt','sum')).reset_index()
    pass
elif topic == 'Habitations':
    # count number of habitations
    outdf = df.groupby(group_attr).agg(cnt = ('habcnt','sum')).reset_index()
    pass
elif topic == 'Facilities':
    # count number of facilities
    outdf = df.groupby(group_attr).agg(cnt = ('faccnt','sum')).reset_index()
    pass
elif topic == 'Proposals':
    # count number of proposals
    outdf = df.groupby(group_attr).agg(cnt = ('propcnt','sum')).reset_index()
    pass
elif topic == 'Buildings':
    # count number of buildings
    outdf = df.groupby(group_attr).agg(cnt = ('bldngcnt','sum')).reset_index()
    pass
elif topic == 'OpenStreetMap PoIs':
    # count number of osm pois
    outdf = df.groupby(group_attr).agg(cnt = ('osmpoicnt','sum')).reset_index()
    pass

outdf.columns = group_attr + ['cnt']

# final geo dataframe for map
st.dataframe(outdf)
st.write(outdf.info())

# activate map with button ?
m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
