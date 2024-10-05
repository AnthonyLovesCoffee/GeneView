from flask import Flask, render_template, request, url_for
import plotly.express as px
import markdown 
import os
import pandas as pd

app = Flask(__name__)

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