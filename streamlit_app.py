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

level = st.select_slider(
     'Select a level of the data',
     options=['Country', 'States', 'Districts', 'Subdistricts', 'Parlamentary Constituencies', 'Assembly Consituencies'])
st.write('My favorite Level is', level)

topic = st.radio('Topic', options=['Roads','Habitations','Facilities','Proposals','Buildings','OpenStreetMap PoIs'],horizontal=True)
st.write('Count how many of ',topic,' are available.')


# set level in query
if level == 'Country':
    run_query = 'select * from Country'
    pass
elif level == 'States':
    run_query = 'select * from States'
    pass
elif level == 'Districts':
    run_query = 'select * from Districts'
    pass
elif level == 'Subdistricts':
    run_query = 'select * from Subdistricts'
    pass
elif level == 'Parlamentary Constituencies':
    run_query = 'select * from Parlamentary Constituencies'
    pass
elif level == 'Assembly Consituencies':
    run_query = 'select * from Assembly Consituencies'
    pass

# set topic in query
if topic == 'Roads':
    run_query = run_query + 'where topic=roads'
    pass
elif topic == 'Habitations':
    run_query = run_query + 'where topic=Habitations'
    pass
elif topic == 'Facilities':
    run_query = run_query + 'where topic=Facilities'
    pass
elif topic == 'Proposals':
    run_query = run_query + 'where topic=Proposals'
    pass
elif topic == 'Buildings':
    run_query = run_query + 'where topic=Buildings'
    pass
elif topic == 'OpenStreetMap PoIs':
    run_query = run_query + 'where topic=OpenStreetMap'
    pass

# parse query outputs
st.write('select * from table where level=',level,' and topic=',topic)
st.write(run_query)

# activate map with button ?
m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
