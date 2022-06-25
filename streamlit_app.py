import streamlit as st
import leafmap.foliumap as leafmap
import pandas_gbq
from google.oauth2 import service_account
from google.cloud import bigquery

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

query = """
select * from (
select taluk_code,taluk_name,count(geometry) cnt from(
select sd.taluk_code,sd.taluk_name,po.geometry from `dev-ind-geo-01.geoprocessed.india_osm_pois` po,`dev-ind-geo-01.geoprocessed.subdistricts` sd
where ST_CONTAINS(sd.geometry,po.geometry) 
) 
group by taluk_code,taluk_name) a right join `dev-ind-geo-01.geoprocessed.subdistricts` b on a.taluk_code=b.taluk_code limit 100;

"""
df = pandas_gbq.read_gbq(query, credentials=credentials)
# df = pandas_gbq.read_gbq('SELECT word FROM `bigquery-public-data.samples.shakespeare` LIMIT 10', credentials=credentials)

st.dataframe(df)

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
