import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

# visit http://127.0.0.1:8050/ in your web browser.

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# for check boxes
health_conditions_list = []

# for line chart
adverse_events_years = []
adverse_events_count = []

# for pie chart
category_data = []
category_values = []

line_graph_data = []
pie_graph_data = []

# check list dictionary
checklist_values = {"checkboxes_data":[]}

url = "https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20200717]&count=patient.drug.drugindication.exact"
health_conditions_count = []
response_data = requests.request("GET", url)
drug_indication_data = response_data.json()  # returns a dictionary of keys and values.
print("Drug Indication Data....")

# Commented the creation of lists for the entire set. Create a dictionary for CheckBoxes.
for counter in enumerate(drug_indication_data['results']):
    health_conditions_list.append(drug_indication_data['results'][counter[0]]['term'])
    health_conditions_count.append(drug_indication_data['results'][counter[0]]['count'])
    value_list = {}
    value_list['label'] =  drug_indication_data['results'][counter[0]]['term']
    value_list['value'] = drug_indication_data['results'][counter[0]]['term'][:3]
    checklist_values["checkboxes_data"].append(value_list)


# All adverse events report by year
url = "https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20200718]&count=receivedate"
response_data = requests.get(url)
adverse_events_by_year_data = response_data.json()
print("Type : ", type(adverse_events_by_year_data))

for years in range(2004, 2020, 1):
    # print("Year :", years)
    total_value_for_year = [data['count'] for data in adverse_events_by_year_data['results'] if str(years) in data['time']]
    total_value_for_year = sum(total_value_for_year)
    # print("Value : ", total_value_for_year)
    adverse_events_years.append(years)
    adverse_events_count.append(total_value_for_year)

# Pie chart data
print("Death Rate...")
url = "https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20200717]&count=seriousnessdeath"
response_data = requests.get(url)
death_rate_data = response_data.json()
for counter in enumerate(death_rate_data['results']):
    print("Event : ", death_rate_data['results'][counter[0]]['term'])
    print("Count : ", death_rate_data['results'][counter[0]]['count'])
    category_data.append('Death')
    category_values.append(death_rate_data['results'][counter[0]]['count'])

print("Hospitalization Data")
url = "https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20200717]&count=seriousnesshospitalization"
response_data = requests.get(url)
hospitalization_rate = response_data.json()
for counter in enumerate(hospitalization_rate['results']):
    print("Event : ", hospitalization_rate['results'][counter[0]]['term'])
    print("Count : ", hospitalization_rate['results'][counter[0]]['count'])
    category_data.append('Hospitalization')
    category_values.append(hospitalization_rate['results'][counter[0]]['count'])

print("Other data")
url = "https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20200717]&count=seriousnessother"
response_data = requests.get(url)
other_data = response_data.json()
for counter in enumerate(other_data['results']):
    print("Event : ", other_data['results'][counter[0]]['term'])
    print("Count : ", other_data['results'][counter[0]]['count'])
    category_data.append('Other')
    category_values.append(other_data['results'][counter[0]]['count'])

print("Total count for events..")
url = "https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20200717]&count=serious"
response_data = requests.get(url)
total_count = response_data.json()
for counter in enumerate(total_count['results']):
    print("Event : ", total_count['results'][counter[0]]['term'])
    print("Count : ", total_count['results'][counter[0]]['count'])

line_graph_data = zip(adverse_events_years, adverse_events_count)
line_graph_data = list(line_graph_data)

# dataframe created with the above data array
df = pd.DataFrame(line_graph_data, columns=["Year", "Number of Drug Reports"])

# Line chart for the data
fig_line = px.line(df, x="Year", y="Number of Drug Reports")
# fig_line.show()

# Pie chart for the events data - Death, Hospitalization, Others and Total.. Use `hole` to create a donut-like pie chart
fig_pie = go.Figure(data=[go.Pie(labels=category_data, values=category_values, hole=.6)])
# fig.show()

dictionary = [{'label': health_conditions_list[0], 'value': "HYP"}, {'label': health_conditions_list[1], 'value': 'RHT'}]
app.layout = html.Div(children=[html.H6(children='Drug Adverse Events by Type of Seriousness'),
                                html.Div([
                                          dcc.Graph(id='pie-graph', figure=fig_pie)
                                         ], style={'width': '29%', 'display': 'inline-block', 'padding': '0 20'}),
                                html.Div([
                                          dcc.Graph(id='line-graph', figure=fig_line)
                                          ], style={'width': '69%', 'display': 'inline-block', 'padding': '0 20'}),
                                html.Div([
                                            dcc.Checklist(
                                            options= checklist_values["checkboxes_data"],
                                            value=['HYP', 'SEF']
                                            )
                                        ], style={'height':'100px', 'border':'2px solid #ccc','width': '39%',
                                                  'display': 'inline-block',
                                                  'padding': '0 20','overflow-y': 'scroll','position':'relative'
                                                  ,'left':'700px'})
                                ])

if __name__ == '__main__':
    app.run_server(debug=True)
