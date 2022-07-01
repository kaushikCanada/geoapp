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
    level_query = 'select country_code code,country_name name, geometry from dev-ind-geo-01.geoprocessed.country'
    pass
elif level == 'States':
    level_query = 'select state_code code,state_name name, geometry from dev-ind-geo-01.geoprocessed.states;'
    pass
elif level == 'Districts':
    level_query = 'select district_code code,district_name name, geometry from dev-ind-geo-01.geoprocessed.districts'
    pass
elif level == 'Subdistricts':
    level_query = 'select taluk_code code,taluk_name name, geometry from dev-ind-geo-01.geoprocessed.subdistricts'
    pass
elif level == 'Parlamentary Constituencies':
    level_query = 'select * from Parlamentary Constituencies'
    pass
elif level == 'Assembly Consituencies':
    level_query = 'select * from Assembly Consituencies'
    pass

def get_run_query(topic,level_query):
    run_query = """
    select a.*,t.geometry 
    from (
    select code,name,count(cgeom) cnt
    from(
    select t.code,t.name,t.geometry tgeom,c.geometry cgeom from dev-ind-geo-01.geoprocessed."""+topic+""" c,("""+level_query+""") t
    where ST_CONTAINS(t.geometry,h.geometry)
    )
    group by code,name) a right join ("""+level_query+""") t on t.code = a.code
    """
    return run_query


# set topic in query
if topic == 'Roads':
    run_query = get_run_query(topic,level_query)
    pass
elif topic == 'Habitations':
    run_query = """
    select a.*,t.geometry 
    from (
    select code,name,count(cgeom) cnt
    from(
    select t.code,t.name,t.geometry tgeom,c.geometry cgeom from dev-ind-geo-01.geoprocessed.habitation c,("""+level_query+""") t
    where ST_CONTAINS(t.geometry,h.geometry)
    )
    group by code,name) a right join ("""+level_query+""") t on t.code = a.code
    """
    pass
elif topic == 'Facilities':
    run_query = """
    select a.*,t.geometry 
    from (
    select code,name,count(cgeom) cnt
    from(
    select t.code,t.name,t.geometry tgeom,c.geometry cgeom from dev-ind-geo-01.geoprocessed.facilities c,("""+level_query+""") t
    where ST_CONTAINS(t.geometry,h.geometry)
    )
    group by code,name) a right join ("""+level_query+""") t on t.code = a.code
    """
    pass
elif topic == 'Proposals':
    run_query = """
    select a.*,t.geometry 
    from (
    select code,name,count(cgeom) cnt
    from(
    select t.code,t.name,t.geometry tgeom,c.geometry cgeom from dev-ind-geo-01.geoprocessed.proposal c,("""+level_query+""") t
    where ST_CONTAINS(t.geometry,h.geometry)
    )
    group by code,name) a right join ("""+level_query+""") t on t.code = a.code
    """
    pass
elif topic == 'Buildings':
    run_query = """
    select a.*,t.geometry 
    from (
    select code,name,count(cgeom) cnt
    from(
    select t.code,t.name,t.geometry tgeom,c.geometry cgeom from dev-ind-geo-01.buildings.india c,("""+level_query+""") t
    where ST_CONTAINS(t.geometry,h.geometry)
    )
    group by code,name) a right join ("""+level_query+""") t on t.code = a.code
    """
    pass
elif topic == 'OpenStreetMap PoIs':
    run_query = """
    select a.*,t.geometry 
    from (
    select code,name,count(cgeom) cnt
    from(
    select t.code,t.name,t.geometry tgeom,c.geometry cgeom from dev-ind-geo-01.geoprocessed.road c,("""+level_query+""") t
    where ST_CONTAINS(t.geometry,h.geometry)
    )
    group by code,name) a right join ("""+level_query+""") t on t.code = a.code
    """
    pass

# parse query outputs
# st.write('select * from table where level=',level,' and topic=',topic)
st.write(level_query)
st.write(run_query)

# activate map with button ?
m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
