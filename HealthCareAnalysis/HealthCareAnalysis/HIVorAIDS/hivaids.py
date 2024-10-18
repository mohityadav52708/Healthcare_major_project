from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json

app = Flask(__name__)

# Dummy data for all 36 states and union territories for HIV/AIDS analysis
data = {
    'State': ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
              'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
              'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
              'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh',
              'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Lakshadweep', 'Puducherry', 'Ladakh', 'Jammu and Kashmir'],
    'Cases': [300000, 15000, 120000, 250000, 80000, 20000, 400000, 220000, 100000, 150000, 500000, 
              480000, 400000, 600000, 70000, 90000, 30000, 45000, 180000, 150000, 200000, 25000, 
              350000, 220000, 60000, 300000, 90000, 320000, 5000, 15000, 12000, 250000, 5000, 10000, 
              7000, 20000],
    'Deaths': [80000, 3000, 10000, 20000, 5000, 1000, 20000, 12000, 6000, 8000, 20000, 
               25000, 18000, 30000, 5000, 8000, 3000, 5000, 10000, 8000, 12000, 2000, 
               15000, 10000, 4000, 12000, 5000, 15000, 500, 1500, 1000, 18000, 1000, 3000, 
               2000, 4000],
    'Recovered': [200000, 10000, 80000, 150000, 60000, 15000, 300000, 150000, 70000, 100000, 350000, 
                  320000, 280000, 500000, 60000, 70000, 25000, 30000, 120000, 90000, 120000, 15000, 
                  200000, 120000, 30000, 150000, 40000, 200000, 2000, 10000, 8000, 200000, 3000, 6000, 
                  5000, 12000],
    'Active': [20000, 12000, 32000, 80000, 15000, 5000, 80000, 35000, 30000, 10000, 150000, 
               180000, 140000, 100000, 10000, 10000, 2000, 6000, 60000, 60000, 68000, 2000, 
               20000, 10000, 30000, 150000, 5000, 150000, 1500, 5000, 4000, 50000, 2000, 1000, 
               2000, 8000]
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
        title=f'Top {top_n} States in India: HIV/AIDS Cases',
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
            title=f'Distribution of HIV/AIDS Cases in Top {top_n} States',
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
            title=f'Area Chart for HIV/AIDS Cases in Top {top_n} States',
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

    
    return render_template('hivaids.html', 
                           bar_fig_html=bar_fig_html,
                           pie_fig_html=pie_fig_html,
                           scatter_fig_html=scatter_fig_html,
                           area_fig_html=area_fig_html,
                           top_n=top_n)

if __name__ == '__main__':
    app.run(debug=True)