import random
import plotly.express as px

def codeRandomizer(lenght):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    code = ''

    for i in range(lenght):
        code += random.choice(characters)

    return code

def grapStatistics(dataframe, time):

    fig = px.line(dataframe, x='date', y='Clicks', labels={'date': 'Hour', 'Clicks': 'Clicks'})
    fig.update_xaxes(title_text="Hour of the day (In UTC)", showgrid=True, gridcolor='grey', showline=True, linecolor='grey', zeroline=False, tickfont=dict(color='grey'))
    fig.update_yaxes(title_text='Clicks', showgrid=True, gridcolor='grey', showline=True, linecolor='grey', zeroline=False, tickfont=dict(color='grey'))
    fig.update_layout(xaxis=dict(range=[0, time + 0.5]),
                    plot_bgcolor='rgba(30,30,30,1)',
                    paper_bgcolor='rgba(30,30,30,1)',
                    font=dict(color='white', size=16, family='"Poppins", sans-serif'),
                    dragmode= False,
                    yaxis=dict(range=[0, dataframe['Clicks'].sum() + 1])
                    )
    fig.update_traces(line=dict(color='rgb(145, 44, 220)', width=4))


    graph = fig.to_html(config = {'displayModeBar': False})
    return graph