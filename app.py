from flask import Flask, render_template, request, url_for
from dash import Dash, html,dcc
import plotly.express as px
import plotly.graph_objects as go
import markdown 
import os
import pandas as pd

app = Flask(__name__)

# Dash instance for visualising
dash_app = Dash(__name__, server=app, url_base_pathname='/dash/')

#Load Samples CSV to extract info for flowchart
csv_file = 'OSD-379-clean.csv'
df = pd.read_csv(csv_file)

# Extract nodes and edges for the Sankey diagram
nodes = set()  # A set to keep unique nodes

# Create edges based on "Sample String"
edges = []

for _, row in df.iterrows():
    stages = row['Sample String'].split('_')  # Split the string to get the stages
    occurrences = row['Occurrences']

    # Add nodes and edges for each transition in the flow
    for i in range(len(stages) - 1):
        source = stages[i]
        target = stages[i + 1]
        
        # Add source and target to the nodes set
        nodes.add(source)
        nodes.add(target)

        # Append edge as a tuple (source, target, value)
        edges.append((source, target, occurrences))

# Convert nodes set to a list and create indices
nodes = list(nodes)
source_indices = [nodes.index(edge[0]) for edge in edges]
target_indices = [nodes.index(edge[1]) for edge in edges]
values = [edge[2] for edge in edges]

# Define a Sankey Diagram for flowchart representation
flowchart = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values
    )
))

# Dash Layout for Flowchart
dash_app.layout = html.Div([
    html.H3('Experiment Flowchart'),
    dcc.Graph(
        id='flowchart',
        figure=flowchart
    )
])

# Function to extract experiment name from the CSV filename
def get_experiment_name(csv_filename):
    return os.path.splitext(csv_filename)[0] 

# Helper function to load the abstract from a markdown file and convert it to HTML
def load_abstract(experiment_name):
    abstract_file = f'abstracts/{experiment_name}.md'
    if os.path.exists(abstract_file):
        with open(abstract_file, 'r') as file:
            md_content = file.read()
        return markdown.markdown(md_content)  # Convert Markdown to HTML
    return "<p>Abstract not available.</p>"

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    csv_file = 'OSD-379-samples.csv'  
    df = pd.read_csv(csv_file)
    experiment_name = get_experiment_name(csv_file)

    # Handle search functionality
    search_query = request.form.get('search')
    samples = df['Sample Name'].tolist()
    if search_query:
        samples = [sample for sample in samples if search_query.lower() in sample.lower()]

    return render_template('index.html', experiment_name=experiment_name, search_query=search_query)

@app.route('/experiment/<name>')
def experiment_detail(name):
    csv_file = f'{name}-samples.csv'
    df = pd.read_csv(csv_file)

    abstract_html = load_abstract(name)

    return render_template('details.html', experiment_name=name, experiment=df, abstract=abstract_html)


if __name__ == '__main__':
    app.run(debug=True)