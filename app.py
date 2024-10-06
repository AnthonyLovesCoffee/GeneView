from flask import Flask, render_template, request, url_for
from dash import Dash, html,dcc
from transformers import pipeline
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

# Split data into control group and experimental group
control_group = df[df['Sample String'].str.startswith(('BSL', 'GC', 'VIV'))]
experimental_group = df[df['Sample String'].str.startswith('FLT')]

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

experimental_flowchart.update_layout(
    title_text='Experimental Group Flowchart',
    font_size=10,
    title_font_size=16,
    margin=dict(l=20, r=20, t=40, b=20)
)

# Dash Layout for Flowchart
dash_app.layout = html.Div([
    html.Div(style={'display': 'flex', 'justify-content': 'space-between'}, children=[
        html.Div([
            html.H3('1'),
            dcc.Graph(
                id='control-flowchart',
                figure=control_flowchart
            )
        ], style={'width': '48%', 'padding': '10px'}),

        html.Div([
            html.H3('2'),
            dcc.Graph(
                id='experimental-flowchart',
                figure=experimental_flowchart
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

# ### Similar existing experiments matching ###
# # Function to extract experiment name from the CSV filename
# def get_experiment_name(csv_filename):
#     return os.path.splitext(csv_filename)[0] 

# # Helper function to load the abstract from a markdown file and convert it to HTML
# def load_abstract(experiment_name):
#     abstract_file = f'abstracts/{experiment_name}.md'
#     if os.path.exists(abstract_file):
#         with open(abstract_file, 'r') as file:
#             md_content = file.read()
#         return markdown.markdown(md_content)  # Convert Markdown to HTML
#     return "<p>Abstract not available.</p>"

# function to summarize experiment details text
# initialise model once for speed
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
experiment_markdown = 'OSD-379'
def summarize_text(experiment_markdown):
    abstract_file = f'abstracts/{experiment_markdown}.md'
    if os.path.exists(abstract_file):
        with open(abstract_file, 'r') as file:
            text = file.read()

        # Generate summary (truncate text if too long)
        if len(text.split()) > 1024:
            text = ' '.join(text.split()[:1024])  # Reduce to fit model constraints

        summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    return "Abstract not available."

# # Load all experiments metadata into a DataFrame
# def load_metadata():
#     metadata_files = ['OSD-379-samples.csv', 'OSD-665-samples.csv']  # Example files for different experiments
#     metadata_df = pd.DataFrame()

#     for file in metadata_files:
#         if os.path.exists(file):
#             df = pd.read_csv(file)
#             metadata_df = pd.concat([metadata_df, df], ignore_index=True)
    
#     return metadata_df

# metadata_df = load_metadata()

# # Function to find similar experiments based on keywords
# def find_similar_experiments(experiment_name):
#     # Get the row corresponding to the given experiment
#     experiment_row = metadata_df[metadata_df['Experiment Name'] == experiment_name]

#     if experiment_row.empty:
#         return []

#     # Extract relevant information from the current experiment
#     current_samples = experiment_row['Sample Type'].values[0]
#     current_conditions = experiment_row['Experimental Conditions'].values[0]

#     # Find similar experiments based on sample type and conditions
#     similar_experiments = metadata_df[
#         (metadata_df['Sample Type'] == current_samples) |
#         (metadata_df['Experimental Conditions'] == current_conditions)
#     ]

#     # Exclude the current experiment from the results
#     similar_experiments = similar_experiments[similar_experiments['Experiment Name'] != experiment_name]

#     return similar_experiments[['Experiment Name', 'Sample Type', 'Experimental Conditions']].to_dict(orient='records')

# @app.route('/experiment/<name>')
# def experiment_detail(name):
#     # Load the abstract and summary as done previously
#     abstract_html = load_abstract(name)
#     abstract_summary = summarize_abstract(name)

#     # Find similar experiments
#     similar_experiments = find_similar_experiments(name)

#     # Pass the similar experiments to the template
#     return render_template('details.html', experiment_name=name, experiment_summary=abstract_summary, abstract=abstract_html, similar_experiments=similar_experiments)


# Load all experiments metadata into a DataFrame
def load_metadata():
    metadata_files = ['OSD-379-metadata.csv', 'OSD-665-metadata.csv']  # Example files for different experiments
    metadata_df = pd.DataFrame()

    for file in metadata_files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            metadata_df = pd.concat([metadata_df, df], ignore_index=True)
    
    return metadata_df

metadata_df = load_metadata()

# Function to find similar experiments based on keywords
def find_similar_experiments(experiment_name):
    # Get the row corresponding to the given experiment
    experiment_row = metadata_df[metadata_df['Experiment Name'] == experiment_name]

    if experiment_row.empty:
        return []

    # Extract relevant information from the current experiment
    current_samples = experiment_row['Sample Type'].values[0]
    current_conditions = experiment_row['Experimental Conditions'].values[0]

    # Find similar experiments based on sample type and conditions
    similar_experiments = metadata_df[
        (metadata_df['Sample Type'] == current_samples) |
        (metadata_df['Experimental Conditions'] == current_conditions)
    ]

    # Exclude the current experiment from the results
    similar_experiments = similar_experiments[similar_experiments['Experiment Name'] != experiment_name]

    return similar_experiments[['Experiment Name', 'Sample Type', 'Experimental Conditions']].to_dict(orient='records')

#2
# @app.route('/experiment/<name>')
# def experiment_detail(name):
#     # Load the abstract and summary as done previously
#     abstract_html = load_abstract(name)
#     abstract_summary = summarize_abstract(name)

#     # Find similar experiments
#     similar_experiments = find_similar_experiments(name)

#     # Pass the similar experiments to the template
#     return render_template('details.html', experiment_name=name, experiment_summary=abstract_summary, abstract=abstract_html, similar_experiments=similar_experiments)


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

#1
# @app.route('/experiment/<name>')
# def experiment_detail(name):
#     csv_file = f'{name}-samples.csv'
#     df = pd.read_csv(csv_file)

#     abstract_html = load_abstract(name)

#     return render_template('details.html', experiment_name=name, experiment=df, abstract=abstract_html)


## OLD SUMMARY ROUTING
# @app.route('/experiment/<name>')
# def experiment_detail(name):
#     # Load the abstract and summary as done previously
#     abstract_html = load_abstract(name)
#     abstract_summary = summarize_abstract(name)

#     # Load the experiment data from CSV if needed
#     csv_file = f'{name}-samples.csv'
#     if os.path.exists(csv_file):
#         df = pd.read_csv(csv_file)
#     else:
#         df = None

#     # Find similar experiments
#     similar_experiments = find_similar_experiments(name)

#     # Pass the similar experiments, abstract, and other data to the template
#     return render_template(
#         'details.html', 
#         experiment_name=name, 
#         experiment_summary=abstract_summary, 
#         abstract=abstract_html, 
#         experiment=df, 
#         similar_experiments=similar_experiments
#     )

@app.route('/experiment/<name>')
def experiment_detail(name):
    # Load the abstract from Markdown
    abstract_html = load_abstract(name)

    # Generate the summary using summarize_text function
    abstract_summary = summarize_text(name)

    # Pass the abstract, summary, and other data to the template
    return render_template(
        'details.html',
        experiment_name=name,
        experiment_summary=abstract_summary,
        abstract=abstract_html
    )

if __name__ == '__main__':
    app.run(debug=True)