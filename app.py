import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import xarray as xr
import netCDF4 as netcdf
from plots import get_coords
import plotly.express as px

data = pd.read_csv("avocado.csv")
data = data.query("type == 'Conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__)
app.title = "City Temperatures"

# retrieve data
DATA_FN = "hadgem3_gc31_ll_ssp5_8_5_data.nc"
CITY = "London"
ncset = netcdf.Dataset(DATA_FN, mode="r")
ncset.set_auto_mask(False)
ds = xr.open_dataset(DATA_FN)

# extract individual variables
temp = ds.variables["ts"]
lat, lon = ds.variables["lat"], ds.variables["lon"]
time = ds.variables["time"]

# get temperatures at closest coords to city
coords = get_coords(CITY)
temp_closest_coords = (
    ds.ts.sel(lon=coords[0], lat=coords[1], method="nearest") - 273.15).values
timevals = time[:]

df = pd.DataFrame({"Year": timevals, "Temperature": temp_closest_coords})
fig = px.line(df, x="Year", y="Temperature",
              title=f"Predicted Temperature for {CITY}")

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

app.layout = html.Div(
    children=[

        # header
        html.Div(
            children=[
                html.H1(
                    children="Predicted Temperature", className="header-title"
                ),
                html.P(
                    children=f"Predicted Temperatures for {CITY}",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div(
            children=[
                dcc.Input(
                    id="city_input",
                    type="text",
                    placeholder="enter city here",
                )
            ],
            className="text-input",
        ),

        html.Div(
            children=[

                # temp chart
                html.Div(
                    children=dcc.Graph(figure=fig),
                    className="card",
                )
            ],
            className="wrapper",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
