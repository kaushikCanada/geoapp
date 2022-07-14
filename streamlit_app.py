import streamlit as st
import leafmap.foliumap as leafmap
import pandas_gbq
from google.oauth2 import service_account
from google.cloud import bigquery
import geopandas as gpd
import pandas as pd
from shapely import wkt

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

###############################################
## LEVEL + TOPIC MAPPING
###############################################

level_dict = {
    'Country':'country_code',
    'States':'state_code',
    'Districts':'district_code',
    'Subdistricts':'taluk_code',
    'Parlamentary Constituencies':'',
    'Assembly Consituencies':''
}

topic_dict = {
    'Roads':'roadcnt',
    'Habitations':'habcnt',
    'Facilities':'faccnt',
    'Proposals':'propcnt',
    'Buildings':'bldngcnt',
    'OpenStreetMap PoIs':'osmpoicnt'
}

###############################################

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
    country = gpd.GeoDataFrame(country,crs="EPSG:4326",geometry=country['geom_text'].apply(wkt.loads))

    states = pandas_gbq.read_gbq("SELECT state_code,state_name,geom_text FROM dev-ind-geo-01.geoprocessed.states", credentials=credentials)
    states = gpd.GeoDataFrame(states,crs="EPSG:4326",geometry=states['geom_text'].apply(wkt.loads))

    districts = pandas_gbq.read_gbq("SELECT district_code,district_name,geom_text FROM dev-ind-geo-01.geoprocessed.districts", credentials=credentials)
    districts = gpd.GeoDataFrame(districts,crs="EPSG:4326",geometry=districts['geom_text'].apply(wkt.loads))

    subdistricts = pandas_gbq.read_gbq("SELECT taluk_code,taluk_name,geom_text FROM dev-ind-geo-01.geoprocessed.subdistricts", credentials=credentials)
    subdistricts = gpd.GeoDataFrame(subdistricts,crs="EPSG:4326",geometry=subdistricts['geom_text'].apply(wkt.loads))

    return country,states,districts,subdistricts

# AGGREGATE DATA
df=fetch_enriched_data()
st.dataframe(df)
# outdf = gpd.GeoDataFrame()
# st.write(pd.__version__)

# BOUNDARY DATA
level_df_dict={}
level_df_dict['Country'],level_df_dict['States'],level_df_dict['Districts'],level_df_dict['Subdistricts'] = fetch_boundary_data()
level_df_dict['Parlamentary Constituencies'] = None
level_df_dict['Assembly Consituencies'] = None
country_df,states_df,districts_df,subdistricts_df = fetch_boundary_data()

st.markdown(markdown)

level = st.select_slider(
     'Select a level of the data',
     options=list(level_dict.keys())) # ['Country', 'States', 'Districts', 'Subdistricts', 'Parlamentary Constituencies', 'Assembly Consituencies']
st.write('My favorite Level is', level)

topic = st.radio('Topic', options=list(topic_dict.keys()),horizontal=True) # ['Roads','Habitations','Facilities','Proposals','Buildings','OpenStreetMap PoIs']
st.write('Count how many of ',topic,' are available.')


# group_attr = level_dict[level]
# outdf = level_df_dict[level]

# set level in query
if level == 'Country':
    # group by country code
    group_attr = ['country_code']
    outdf = country_df
    pass
elif level == 'States':
    # group by state code
    group_attr = ['state_code']
    outdf = states_df
    pass
elif level == 'Districts':
    # group by district code
    group_attr = ['district_code']
    outdf = districts_df
    pass
elif level == 'Subdistricts':
    # group by subdistrict code
    group_attr = ['taluk_code']
    outdf = subdistricts_df
    pass
elif level == 'Parlamentary Constituencies':
    # group by pc code
    outdf = subdistricts_df
    pass
elif level == 'Assembly Consituencies':
    # group by ac code
    outdf = subdistricts_df
    pass

# outdf1 = df.groupby(group_attr).agg(cnt = (topic_dict[topic],'sum')).reset_index()

# set topic in query
if topic == 'Roads':
    # count number of roads
    outdf1 = df.groupby(group_attr).agg(cnt = ('roadcnt','sum')).reset_index()
    pass
elif topic == 'Habitations':
    # count number of habitations
    outdf1 = df.groupby(group_attr).agg(cnt = ('habcnt','sum')).reset_index()
    pass
elif topic == 'Facilities':
    # count number of facilities
    outdf1 = df.groupby(group_attr).agg(cnt = ('faccnt','sum')).reset_index()
    pass
elif topic == 'Proposals':
    # count number of proposals
    outdf1 = df.groupby(group_attr).agg(cnt = ('propcnt','sum')).reset_index()
    pass
elif topic == 'Buildings':
    # count number of buildings
    outdf1 = df.groupby(group_attr).agg(cnt = ('bldngcnt','sum')).reset_index()
    pass
elif topic == 'OpenStreetMap PoIs':
    # count number of osm pois
    outdf1 = df.groupby(group_attr).agg(cnt = ('osmpoicnt','sum')).reset_index()
    pass

outdf1.columns = group_attr + ['cnt']
outdf = outdf.merge(outdf1,on=group_attr,how='left')

# final geo dataframe for map
# st.dataframe(outdf)
st.write(type(outdf))
# df['geometry'] = df.wkt_geom.apply(wkt.loads)

# activate map with button ?
m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
