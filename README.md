# GeneView: NASA Data Visualizer

### Description
The **NASA Data Visualizer** is a tool developed to make complex space experiments more accessible and easier to understand. By displaying experiment data in a simplified, readable format, scientists and users can quickly comprehend key insights from space experiments. 

This application includes several features that enhance the user experience, enabling both accessibility and interactive exploration of data.

### Key Features:
- **Text-to-Speech**: A feature that reads the abstract aloud, improving accessibility for visually impaired users or those who prefer auditory content.
- **AI Chatbot**: A chatbot that allows users to query individual experiments for specific information or clarifications.
- **Flowcharts**: Visual illustrations of experimental setups, showing organisms, controls, and experiment conditions in an easy-to-understand format.
- **Comparative Linking**: The app provides links to Earth-based studies that are similar to the space experiments, allowing for easy comparisons and contextual understanding.

---

## Installation

### Prerequisites
Make sure you have the following installed on your system:
- **Python 3.x**: [Install Python](https://www.python.org/downloads/)
- **pip**: Python's package installer, which usually comes with Python. You can check if pip is installed by running:
```bash 
  pip --version
```
Clone the project to your local machine using the following command:
```bash
  git clone https://github.com/YourUsername/GeneView.git
  cd GeneView
```
Set up a virtual environment to isolate your project dependencies:
```bash
  python -m venv venv
  source venv/bin/activate
```
Install the required Python packages listed in requirements.txt:
```bash
  pip install -r requirements.txt
```
To start the Flask app, simply run:
```python
  python app.py
```

By default, the app will be available at http://127.0.0.1:5000/.
