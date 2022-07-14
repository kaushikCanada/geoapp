FROM gboeing/osmnx:v1.2.0

RUN conda install -y -c conda-forge pyrosm python-igraph
RUN conda install -y -c conda-forge pyresample
RUN pip install geospatial spaghetti momepy cityseer haversine matplotlib-scalebar scikit-network dtale
RUN pip install pandas-gbq google-cloud-bigquery xlrd
RUN conda install -y -c conda-forge pandas-profiling
RUN conda install -y -c pyviz panel
RUN pip install geemap leafmap owslib streamlit

ENV PORT=8080


COPY *.py ./ 
# COPY data  ./data/
RUN mkdir ./".streamlit"
COPY secrets.toml ./".streamlit"

CMD streamlit run streamlit_app.py --server.port=${PORT}  --browser.serverAddress="0.0.0.0"