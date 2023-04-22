# 507-Final-Project

This project visualized relationships and features among different characters in the Harry Potter Universe. The data is organized into six graph structures. To quick start, you do not need to run all the scripts/notebooks. You only need to download the visualization.py and the six json files along with it. The visualization will be hosted on http://127.0.0.1:8050/. If you want to start from the beginning, you need to run code in the order of data_collection.ipynb, data_manipulation.ipynb, graph.py, and visualization.py.

For the data_collection.ipynb, you will get an error message when extracting data from the YouTube API. This is because the API only allows 100 search requests per day. You can extract the rest data after 24 hours. The API key is muted in the code, please replace it with your own YouTube API key.

The required libraries for all the code include requests, BeautifulSoup, Google APIs Client Library, Pandas, NetworkX, Plotly, and Dash.
You can click the dropdown menu to select different graphs to interact with the visualization. All bubbles are clickable and will show a more detailed view. The reset button is used to go back to the main view.
