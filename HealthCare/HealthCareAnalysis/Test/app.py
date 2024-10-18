# Import necessary libraries
from flask import Flask, render_template_string
import plotly.express as px
import plotly.io as pio

# Create a Flask app instance
app = Flask(__name__)

# Flask route to render the homepage with the chart
@app.route('/')
def index():
    # Generate the bar chart for COVID-19 Cure and Death Rates
    fig = px.bar(
        top_10_cities,
        x='City',
        y=['Cure Rate (%)', 'Death Rate (%)'],
        title='Top 10 Cities in India: COVID-19 Cure and Death Rates',
        labels={'value': 'Percentage', 'variable': 'Rate'},
        barmode='group'
    )

    # Customize the layout of the chart
    fig.update_layout(
        xaxis_title='City',
        yaxis_title='Percentage (%)',
        legend_title='Rate Type',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )

    # Convert the Plotly figure to HTML
    plot_html = pio.to_html(fig, full_html=False)

    # Render the HTML page
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Top 10 Diseases in India</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                h1 {
                    color: #2c3e50;
                }
            </style>
        </head>
        <body>
            <h1>Top 10 Cities in India: COVID-19 Cure and Death Rates</h1>
            <div>{{ plot_html | safe }}</div>
        </body>
        </html>
    ''', plot_html=plot_html)

# Run the Flask app on a specific port
if __name__ == '__main__':
    app.run(port=5000)
