from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
import requests
import json

app = Flask(__name__)

def get_covid_data():
    api_url = 'https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise'
    response = requests.get(api_url)
    if response.status_code == 200:
        covid_data = response.json()
        return covid_data['data']['statewise']
    else:
        return []

def create_charts(top_states, top_n):
    # Create Colorful Bar Chart for Cases per State
    bar_fig = px.bar(
        top_states,
        x='State',
        y='Cases',
        title=f'Top {top_n} States in India: COVID-19 Cases',
        labels={'Cases': 'Number of Cases'},
        color='Cases',
        color_continuous_scale='Rainbow'
    )
    bar_fig.update_layout(
        xaxis_title='State',
        yaxis_title='Number of Cases',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    bar_fig_html = pio.to_html(bar_fig, full_html=False)

    # Create Pie Chart for Distribution of Cases
    pie_fig = px.pie(
        top_states,
        names='State',
        values='Cases',
        title=f'Distribution of COVID-19 Cases in Top {top_n} States'
    )
    pie_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    pie_fig_html = pio.to_html(pie_fig, full_html=False)

    # Create Enhanced Scatter Plot
    scatter_fig = px.scatter(
        top_states,
        x='Cure Rate (%)',
        y='Death Rate (%)',
        size='Cases',
        color='State',
        title=f'Distribution of Cure and Death Rates in Top {top_n} States',
        labels={'Cure Rate (%)': 'Cure Rate (%)', 'Death Rate (%)': 'Death Rate (%)'},
        hover_data=['Active'],
        color_continuous_scale='Viridis',
        size_max=60
    )
    scatter_fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))
    scatter_fig.update_layout(
        xaxis_title='Cure Rate (%)',
        yaxis_title='Death Rate (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    scatter_fig_html = pio.to_html(scatter_fig, full_html=False)

    return bar_fig_html, pie_fig_html, scatter_fig_html

@app.route('/')
def index():
    statewise_data = get_covid_data()
    
    states = []
    cases = []
    deaths = []
    recovered = []
    active = []

    for state in statewise_data:
        state_name = state['state']
        states.append(state_name)
        
        confirmed = state['confirmed']
        if isinstance(confirmed, str):
            confirmed = int(confirmed.replace(',', ''))
        cases.append(confirmed)
        
        deaths_val = state['deaths']
        if isinstance(deaths_val, str):
            deaths_val = int(deaths_val.replace(',', ''))
        deaths.append(deaths_val)
        
        recovered_val = state['recovered']
        if isinstance(recovered_val, str):
            recovered_val = int(recovered_val.replace(',', ''))
        recovered.append(recovered_val)
        
        active_val = state['active']
        if isinstance(active_val, str):
            active_val = int(active_val.replace(',', ''))
        active.append(active_val)

    df = pd.DataFrame({
        'State': states,
        'Cases': cases,
        'Deaths': deaths,
        'Recovered': recovered,
        'Active': active
    })

    df['Cure Rate (%)'] = (df['Recovered'] / df['Cases']) * 100
    df['Death Rate (%)'] = (df['Deaths'] / df['Cases']) * 100

    top_n = int(request.args.get('top_n', 10))

    top_states = df.sort_values(by='Cases', ascending=False).head(top_n)

    bar_fig_html, pie_fig_html, scatter_fig_html = create_charts(top_states, top_n)

    # Prepare data for the Apex chart
    apex_chart_data = {
        "categories": top_states['State'].tolist(),
        "cases": top_states['Cases'].tolist(),
    }

    return render_template('covid.html', 
                           bar_fig_html=bar_fig_html,
                           pie_fig_html=pie_fig_html,
                           scatter_fig_html=scatter_fig_html,
                           top_n=top_n,
                           apex_chart_data=json.dumps(apex_chart_data))

if __name__ == '__main__':
    app.run(port=5002, debug=True)
