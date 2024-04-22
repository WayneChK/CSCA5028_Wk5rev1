import json
import pandas as pd
import pytest
import os


def test_fetch_data_integration(test_client, test_db):
    # Simulate sending data as JSON
    data = {'send_ticker': 'AAPL'}
    response = test_client.post('/endpoint_data', json=data)

    # Assertions
    assert response.status_code == 200
    json_dict = response.json 
    # Alternatively, we can use response.data, and json.load(response.data).

    # Check for plot data and basic validation
    assert 'plot' in json_dict

    plotly_json = json_dict['plot']
    plot_in_dict = json.loads(plotly_json)
    assert 'data' in plot_in_dict  # At least 5 columns (including datetime)
    assert 'layout' in plot_in_dict

    assert 'open' in plot_in_dict['data'][0]  # Check for expected columns
    assert 'close' in plot_in_dict['data'][0]
    