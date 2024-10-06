from flask import Flask, render_template, request, url_for
from dash import Dash, html,dcc
import plotly.express as px
import plotly.graph_objects as go
import markdown 
import os
import pandas as pd

app = Flask(__name__)

# # Dash instance for visualising
# dash_app = Dash(__name__, server=app, url_base_pathname='/dash/')
# Dash instance for visualising OSD-379
dash_app_379 = Dash(__name__, server=app, url_base_pathname='/dash/379/')

# Dash instance for visualising OSD-665
dash_app_665 = Dash(__name__, server=app, url_base_pathname='/dash/665/')

#Load Samples CSV to extract info for flowchart
csv_file = 'OSD-379-clean.csv'
csv_file_665 = 'OSD-665-clean.csv'
df = pd.read_csv(csv_file)
df_665 = pd.read_csv(csv_file_665)

OSD_665_csv_file = 'OSD-665-samples.csv'
OSD_665_df = pd.read_csv(csv_file)
# Split data into control group and experimental group
control_group = df[df['Sample String'].str.startswith(('BSL', 'GC', 'VIV'))]
experimental_group = df[df['Sample String'].str.startswith('FLT')]

OSD_665_control_group = OSD_665_df[OSD_665_df['Sample String'].str.startswith(('F', 'GC', 'V'))]
OSD_665_df_experimental_group = OSD_665_df[OSD_665_df['Sample String'].str.startswith('FLT')]

# Helper function to create Sankey diagram components from data
def create_sankey_data(df, color_palette):
    nodes = set()  # A set to keep unique nodes
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

    # Assign colors to nodes from the color palette
    node_colors = [color_palette[i % len(color_palette)] for i in range(len(nodes))]

    return nodes, source_indices, target_indices, values, node_colors

# Define color palettes for control and experimental groups
control_color_palette = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
experimental_color_palette = ['#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

# Create Sankey data for control and experimental groups
control_nodes, control_source, control_target, control_values, control_colors = create_sankey_data(control_group, control_color_palette)
experimental_nodes, experimental_source, experimental_target, experimental_values, experimental_colors = create_sankey_data(experimental_group, experimental_color_palette)

OSD_665_control_nodes, OSD_665_control_source, OSD_665_control_target, OSD_665_control_values, OSD_665_control_colors = create_sankey_data(control_group, control_color_palette)
OSD_665_experimental_nodes, OSD_665_experimental_source, OSD_665_experimental_target, OSD_665_experimental_values, OSD_665_experimental_colors = create_sankey_data(experimental_group, experimental_color_palette)

# Define Sankey Diagram for Control Group with grey links
control_flowchart = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=control_nodes,
        color=control_colors
    ),
    link=dict(
        source=control_source,
        target=control_target,
        value=control_values,
        color='rgba(192, 192, 192, 0.4)'#'grey'
    )
))

control_flowchart.update_layout(
    title_text='Control Group Flowchart',
    font_size=10,
    title_font_size=16,
    margin=dict(l=20, r=20, t=40, b=20)
)

# Define Sankey Diagram for Experimental Group with grey links
experimental_flowchart = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=experimental_nodes,
        color=experimental_colors
    ),
    link=dict(
        source=experimental_source,
        target=experimental_target,
        value=experimental_values,
        color='rgba(192, 192, 192, 0.4)'#'grey'
    )
))

# Define Sankey Diagram for Experimental Group for OSD-665 with grey links
experimental_flowchart_665 = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=OSD_665_experimental_nodes,
        color=OSD_665_experimental_colors
    ),
    link=dict(
        source=OSD_665_experimental_source,
        target=OSD_665_experimental_target,
        value=OSD_665_experimental_values,
        color='rgba(192, 192, 192, 0.4)'
    )
))

control_flowchart_665 = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=OSD_665_experimental_nodes,
        color=OSD_665_experimental_colors
    ),
    link=dict(
        source=OSD_665_experimental_source,
        target=OSD_665_experimental_target,
        value=OSD_665_experimental_values,
        color='rgba(192, 192, 192, 0.4)'
    )))

experimental_flowchart_379 = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=OSD_665_experimental_nodes,
        color=OSD_665_experimental_colors
    ),
    link=dict(
        source=OSD_665_experimental_source,
        target=OSD_665_experimental_target,
        value=OSD_665_experimental_values,
        color='rgba(192, 192, 192, 0.4)'
    )
))


experimental_flowchart_379.update_layout(
    title_text='Experimental Group Flowchart (OSD-379)',
    font_size=10,
    title_font_size=16,
    margin=dict(l=20, r=20, t=40, b=20)
)

experimental_flowchart_665.update_layout(
    title_text='Experimental Group Flowchart (OSD-665)',
    font_size=10,
    title_font_size=16,
    margin=dict(l=20, r=20, t=40, b=20)
)

control_flowchart_665.update_layout(
    title_text='Experimental Group Flowchart (OSD-665)',
    font_size=10,
    title_font_size=16,
    margin=dict(l=20, r=20, t=40, b=20)
)

# Dash Layout for Flowchart
# Dash Layout for OSD-379 Flowchart
dash_app_379.layout = html.Div([
    html.Div(style={'display': 'flex', 'justify-content': 'space-between'}, children=[
        html.Div([
            html.H3('OSD-379 Control Group'),
            dcc.Graph(
                id='control-flowchart-379',
                figure=control_flowchart
            )
        ], style={'width': '48%', 'padding': '10px'}),

        html.Div([
            html.H3('OSD-379 Experimental Group'),
            dcc.Graph(
                id='experimental-flowchart-379',
                figure=experimental_flowchart
            )
        ], style={'width': '48%', 'padding': '10px'}),
    ])
])

# Dash Layout for OSD-665 Flowchart
dash_app_665.layout = html.Div([
    html.Div(style={'display': 'flex', 'justify-content': 'space-between'}, children=[
        html.Div([
            html.H3('OSD-665 Control Group'),
            dcc.Graph(
                id='control-flowchart-665',
                figure=control_flowchart_665
            )
        ], style={'width': '48%', 'padding': '10px'}),

        html.Div([
            html.H3('OSD-665 Experimental Group'),
            dcc.Graph(
                id='experimental-flowchart-665',
                figure=experimental_flowchart_665
            )
        ], style={'width': '48%', 'padding': '10px'}),
    ])
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
    if name == 'OSD-379':
        csv_file = f'{name}-samples.csv'
        df = pd.read_csv(csv_file)

        # Load abstract from md file
        abstract_html = load_abstract(name)

        # Render OSD-379 details
        return render_template('OSD-379_details.html', experiment_name=name, experiment=df, abstract=abstract_html)
    
    elif name == 'OSD-665':
        csv_file = 'OSD-665-clean.csv'
        df = pd.read_csv(csv_file)

        # Load abstract from md file
        abstract_html = load_abstract(name)

        # Render OSD-665 details
        return render_template('OSD-665_details.html', experiment_name=name, experiment=df, abstract=abstract_html)

    else:
        return "Template not available for the given experiment", 404


if __name__ == '__main__':
    app.run(debug=True)

    