import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import netCDF4 as netcdf
import xarray as xr
from plots import get_coords

DATA_FN = 'hadgem3_gc31_ll_ssp5_8_5_data.nc'
CITY = "Sydney"

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
ncset = netcdf.Dataset(DATA_FN, mode='r')
ncset.set_auto_mask(False)
ds = xr.open_dataset(DATA_FN)

# extract individual variables
temp = ds.variables['ts']
lat, lon = ds.variables['lat'], ds.variables['lon']
time = ds.variables['time']

# get temperatures at closest coords to city
coords = get_coords(CITY)
temp_closest_coords = (ds.ts.sel(lon = coords[0], lat = coords[1], method = 'nearest') - 273.15).values
timevals = time[:]

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="City Temperatures", className="header-title"
                ),
                html.P(
                    children="Analyse the predicted temperature of cities from 2015 to 2099",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": "timevals",
                                    "y": "temp_closest_coords",
                                    "type": "lines",
                                    "hovertemplate": "$%{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Temperature of City",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": False},
                                "yaxis": {"fixedrange": False},

                                "colorway": ["#17B897"],
                            },
                        },
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

'''
@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, avocado_type, start_date, end_date):
    mask = (
        (data.region == region)
        & (data.type == avocado_type)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]

    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["AveragePrice"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Total Volume"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    return price_chart_figure, volume_chart_figure
'''

if __name__ == "__main__":
    app.run_server(debug = True)
