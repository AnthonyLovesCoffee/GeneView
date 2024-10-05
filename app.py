from flask import Flask, render_template, request, url_for
import plotly.express as px
import os
import pandas as pd

app = Flask(__name__)

# Function to extract experiment name from the CSV filename
def get_experiment_name(csv_filename):
    return os.path.splitext(csv_filename)[0]  # Remove file extension

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    # Load the CSV file and get the experiment name
    csv_file = 'OSD-379-samples.csv'  # Example CSV file
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

    # Organism Distribution Pie Chart
    organism_distribution = df['Characteristics: Organism'].value_counts().reset_index()
    organism_distribution.columns = ['Organism', 'Count']
    fig_organism = px.pie(organism_distribution, values='Count', names='Organism', title='Organism Distribution')
    organism_pie_html = fig_organism.to_html(full_html=False)

    # Genotype Distribution Bar Chart
    genotype_distribution = df['Characteristics: Genotype'].value_counts().reset_index()
    genotype_distribution.columns = ['Genotype', 'Count']
    fig_genotype = px.bar(genotype_distribution, x='Genotype', y='Count', title='Genotype Distribution')
    genotype_bar_html = fig_genotype.to_html(full_html=False)

    # Pass the visualizations to the template
    return render_template('details.html', experiment_name=name, organism_pie_html=organism_pie_html, genotype_bar_html=genotype_bar_html)

if __name__ == '__main__':
    app.run(debug=True)