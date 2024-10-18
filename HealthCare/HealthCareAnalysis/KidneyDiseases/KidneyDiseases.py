from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json

app = Flask(__name__)

# Dummy data for all 36 states and union territories for Kidney Diseases analysis
data = {
    'State': ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
              'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
              'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
              'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh',
              'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Lakshadweep', 'Puducherry', 'Ladakh', 'Jammu and Kashmir'],
    'Cases': [400000, 25000, 300000, 600000, 200000, 50000, 600000, 350000, 150000, 250000, 800000, 
              700000, 500000, 1000000, 80000, 120000, 50000, 80000, 300000, 250000, 350000, 30000, 
              450000, 300000, 100000, 400000, 120000, 500000, 10000, 25000, 20000, 400000, 10000, 30000, 
              15000, 80000],
    'Deaths': [50000, 2000, 15000, 25000, 8000, 1000, 15000, 10000, 5000, 8000, 25000, 
               22000, 18000, 40000, 6000, 8000, 4000, 6000, 20000, 15000, 20000, 2000, 
               30000, 20000, 6000, 15000, 5000, 30000, 1000, 1500, 1000, 20000, 500, 1000, 
               800, 5000],
    'Recovered': [200000, 12000, 150000, 350000, 100000, 30000, 400000, 200000, 80000, 120000, 500000, 
                  450000, 350000, 800000, 60000, 80000, 25000, 30000, 120000, 100000, 150000, 20000, 
                  250000, 180000, 60000, 250000, 60000, 300000, 8000, 10000, 8000, 300000, 6000, 20000, 
                  7000, 30000],
    'Active': [150000, 7000, 135000, 250000, 92000, 15000, 350000, 140000, 70000, 100000, 250000, 
               250000, 170000, 200000, 14000, 25000, 10000, 15000, 60000, 40000, 50000, 8000, 
               200000, 120000, 34000, 150000, 50000, 170000, 2000, 5000, 6000, 80000, 3000, 1000, 
               6000, 25000]
}


import plotly.graph_objs as go
import numpy as np

def create_charts(top_states, top_n):
    # Create Colorful Bar Chart for Cases per State
    top_states = top_states.nlargest(top_n, 'Cases')

    # Create Colorful Bar Chart for Cases per State
    bar_fig = px.bar(
        top_states,
        x='State',
        y='Cases',
        title=f'Top {top_n} States in India: Kidney Diseases Cases',
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

    # Create Animated Pie Chart for Distribution of Cases with Fan-Like Effect
    frames = [
        go.Frame(
            data=[
                go.Pie(
                    labels=top_states['State'],
                    values=top_states['Cases'],
                    hole=0.3,
                    sort=False,
                    direction="clockwise",
                    pull=[0.2 if i <= idx else 0 for i in range(len(top_states))]
                )
            ],
            name=str(idx)
        )
        for idx in range(len(top_states))
    ]

    pie_fig = go.Figure(
        data=[go.Pie(labels=top_states['State'], values=top_states['Cases'], hole=0.3)],
        layout=go.Layout(
            title=f'Distribution of Kidney Diseases Cases in Top {top_n} States',
            updatemenus=[{
                'type': 'buttons',
                'buttons': [{
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 500, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 300}
                    }]
                }]
            }]
        ),
        frames=frames
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

    # Create Animated Area Chart
    # Generate animation frames by incrementally increasing the y-values
    frames = [
        go.Frame(
            data=[
                go.Scatter(
                    x=top_states['State'],
                    y=top_states['Cases'] * (i + 1) / (len(top_states)),
                    mode='lines',
                    fill='tozeroy',
                    line=dict(color='rgb(255, 87, 34)')
                )
            ],
            name=str(i)
        )
        for i in range(1, len(top_states) + 1)
    ]

    area_fig = go.Figure(
        data=[go.Scatter(
            x=top_states['State'],
            y=top_states['Cases'] * 1 / (len(top_states)),
            mode='lines',
            fill='tozeroy',
            line=dict(color= 'rgb(255, 87, 34)')
        )],
        layout=go.Layout(
            title=f'Area Chart for Kidney Diseases Cases in Top {top_n} States',
            xaxis_title='State',
            yaxis_title='Number of Cases',
            plot_bgcolor='rgb(245, 222, 179)',
            updatemenus=[
                {
                    'buttons': [
                        {
                            'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                            'label': 'Play',
                            'method': 'animate'
                        },
                        {
                            'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                            'label': 'Pause',
                            'method': 'animate'
                        }
                    ],
                    'direction': 'left',
                    'pad': {'r': 10, 't': 87},
                    'showactive': True,
                    'type': 'buttons',
                    'x': 0.1,
                    'xanchor': 'right',
                    'y': 0,
                    'yanchor': 'top'
                }
            ],
            sliders=[{
                'active': 0,
                'steps': [
                    {'label': str(i + 1), 'method': 'animate', 'args': [[str(i)], {'mode': 'immediate', 'transition': {'duration': 0}}]} 
                    for i in range(len(top_states))
                ],
                'transition': {'duration': 300, 'easing': 'cubic-in-out'}
            }]
        ),
        frames=frames
    )

    area_fig_html = pio.to_html(area_fig, full_html=False)

    return bar_fig_html, pie_fig_html, scatter_fig_html, area_fig_html


@app.route('/')
def index():
    df = pd.DataFrame(data)

    df['Cure Rate (%)'] = (df['Recovered'] / df['Cases']) * 100
    df['Death Rate (%)'] = (df['Deaths'] / df['Cases']) * 100

    top_n = int(request.args.get('top_n', 10))

    top_states = df.sort_values(by='Cases', ascending=False).head(top_n)

    bar_fig_html, pie_fig_html, scatter_fig_html, area_fig_html  = create_charts(top_states, top_n)

    
    return render_template('KidneyDiseases.html', 
                           bar_fig_html=bar_fig_html,
                           pie_fig_html=pie_fig_html,
                           scatter_fig_html=scatter_fig_html,
                           area_fig_html=area_fig_html,
                           top_n=top_n)

if __name__ == '__main__':
    app.run(debug=True)