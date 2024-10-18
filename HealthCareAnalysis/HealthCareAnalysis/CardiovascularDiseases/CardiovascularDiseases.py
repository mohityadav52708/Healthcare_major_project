from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json

app = Flask(__name__)

# Dummy data for all 36 states and union territories for Cardiovascular Diseases analysis
data = {
    'State': ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
              'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
              'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
              'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh',
              'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Lakshadweep', 'Puducherry', 'Ladakh', 'Jammu and Kashmir'],
    'Cases': [1800000, 95000, 1200000, 1900000, 1100000, 150000, 3500000, 1600000, 750000, 1200000, 3200000, 
              3000000, 2500000, 5500000, 600000, 850000, 350000, 450000, 2000000, 1600000, 2300000, 200000, 
              3700000, 2000000, 800000, 2500000, 700000, 2700000, 100000, 200000, 170000, 2600000, 85000, 300000, 
              90000, 700000],
    'Deaths': [60000, 2500, 20000, 45000, 28000, 4000, 70000, 42000, 18000, 28000, 58000, 
               55000, 48000, 100000, 12000, 18000, 9000, 14000, 40000, 35000, 50000, 6000, 
               70000, 45000, 13000, 52000, 16000, 60000, 3500, 5000, 3500, 50000, 2000, 8000, 
               2500, 20000],
    'Recovered': [1200000, 75000, 850000, 1400000, 800000, 120000, 2300000, 1200000, 600000, 850000, 2200000, 
                  2000000, 1800000, 4000000, 450000, 600000, 270000, 350000, 1500000, 1200000, 1700000, 150000, 
                  2600000, 1600000, 500000, 1800000, 500000, 2000000, 75000, 150000, 120000, 1800000, 60000, 220000, 
                  75000, 500000],
    'Active': [540000, 17000, 330000, 455000, 270000, 24000, 1130000, 360000, 130000, 340000, 970000, 
               940000, 720000, 1500000, 138000, 230000, 73000, 85000, 500000, 370000, 600000, 49000, 
               900000, 400000, 287000, 680000, 190000, 700000, 21500, 45000, 35000, 750000, 30000, 70000, 
               20000, 180000]
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
        title=f'Top {top_n} States in India: Cardiovascular Diseases Cases',
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
            title=f'Distribution of Cardiovascular Diseases Cases in Top {top_n} States',
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
            title=f'Area Chart for Cardiovascular Diseases Cases in Top {top_n} States',
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

    
    return render_template('CardiovascularDiseases.html', 
                           bar_fig_html=bar_fig_html,
                           pie_fig_html=pie_fig_html,
                           scatter_fig_html=scatter_fig_html,
                           area_fig_html=area_fig_html,
                           top_n=top_n)

if __name__ == '__main__':
    app.run(debug=True)