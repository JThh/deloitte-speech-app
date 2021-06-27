from bokeh.models.textures import ImageURLTexture
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from config import *


import numpy as np
# import pandas as pd
# from number_parser import parse
# import dateparser

# DATA_URL = "https://drive.google.com/uc?export=download&id=1lU52Rr6hf9d1H_kWPwQYQMaCwzLcbLFr"

# data = pd.read_csv(DATA_URL)

st.set_page_config(layout="wide")


def process_text(txt):
    '''
    Function for processing text and extracting key information.
    '''
    assert txt != ''

    # num_txt = parse(txt)
    try:
        TIME_RANGE = [int(s) for s in txt.split() if s.isdigit()][0]
    except:
        #st.warning('Please provide a time range.')
        pass
    # if num_txt != txt:
    #     number = [int(s) for s in num_txt.split() if s.isdigit()][0]
    if 'mean' in txt:
        for x in EXPLAINABLE_TXT:
            if x in txt:
                show_meaning(x)
                return
        st.warning(
            "This is not yet explainable. More comprehensive explanations are expected to be filled in soon.")

    if 'catego' in txt:
        for cat in CATEGORIES:
            if cat in txt:
                show_category(cat)
        show_category()
        return
        # if 'revenue' in txt:
        #     for cat in categories:
        #         show_revenue(number,cat)
        # if 'profit' in txt:
        #     for cat in categories:
        #         show_profit(number,cat)

    if 'revenue' in txt or 'profit' in txt:
        show_revenue(TIME_RANGE)
    # if 'profit' in txt:
    #     show_profit(TIME_RANGE)


def show_category(cat='all'):
    def draw_fig():

        y_saving = [1.3586, 2.2623000000000002, 4.9821999999999997, 6.5096999999999996,
                    7.4812000000000003, 7.5133000000000001, 15.2148, 17.520499999999998
                    ]
        y_net_worth = [93453.919999999998, 81666.570000000007, 69889.619999999995,
                       78381.529999999999, 141395.29999999999, 92969.020000000004,
                       66090.179999999993, 122379.3]
        x = ['cat1', 'cat2', 'cat3', 'cat4',
             'cat5', 'cat6', 'cat7', 'cat8']

        # Creating two subplots
        fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                            shared_yaxes=False, vertical_spacing=0.001)

        fig.append_trace(go.Bar(
            x=y_saving,
            y=x,
            marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ),
            name='Revenues, percentage of total revenues',
            orientation='h',
        ), 1, 1)

        fig.append_trace(go.Scatter(
            x=y_net_worth, y=x,
            mode='lines+markers',
            line_color='rgb(128, 0, 128)',
            name='Revenue net worth, in Millions(¥)',
        ), 1, 2)

        fig.update_layout(
            title='Revenues percentage & net worth for eight sub-categories',
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
                domain=[0, 0.85],
            ),
            yaxis2=dict(
                showgrid=False,
                showline=True,
                showticklabels=False,
                linecolor='rgba(102, 102, 102, 0.8)',
                linewidth=2,
                domain=[0, 0.85],
            ),
            xaxis=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                domain=[0, 0.42],
            ),
            xaxis2=dict(
                zeroline=False,
                showline=False,
                showticklabels=True,
                showgrid=True,
                domain=[0.47, 1],
                side='top',
                dtick=25000,
            ),
            legend=dict(x=0.029, y=1.038, font_size=10),
            margin=dict(l=100, r=20, t=70, b=70),
            paper_bgcolor='rgb(248, 248, 255)',
            plot_bgcolor='rgb(248, 248, 255)',
        )

        annotations = []

        y_s = np.round(y_saving, decimals=2)
        y_nw = np.rint(y_net_worth)

        # Adding labels
        for ydn, yd, xd in zip(y_nw, y_s, x):
            # labeling the scatter savings
            annotations.append(dict(xref='x2', yref='y2',
                                    y=xd, x=ydn - 20000,
                                    text='{:,}'.format(ydn) + 'M',
                                    font=dict(family='Arial', size=12,
                                              color='rgb(128, 0, 128)'),
                                    showarrow=False))
            # labeling the bar net worth
            annotations.append(dict(xref='x1', yref='y1',
                                    y=xd, x=yd + 3,
                                    text=str(yd) + '%',
                                    font=dict(family='Arial', size=12,
                                              color='rgb(50, 171, 96)'),
                                    showarrow=False))
        # Source
        annotations.append(dict(xref='paper', yref='paper',
                                x=-0.2, y=-0.109,
                                text='Sample company "' +
                                '(2020), Revenues perc. (indicator), ' +
                                'Revenues net worth (indicator). doi: ' +
                                '10.1787/cfc6f499-en (Accessed on 05 June 2015)',
                                font=dict(family='Arial', size=10,
                                          color='rgb(150,150,150)'),
                                showarrow=False))

        fig.update_layout(annotations=annotations)

        return fig
    if cat == 'all':
        st.plotly_chart(draw_fig(),use_container_width=True)
        return
    if cat not in CATEGORIES:
        st.warning("Please select a category in the categories list.")
    else:
        show_category_revenue(TIME_RANGE,cat)


def show_revenue(number):

    # st.subheader("Revenue Report for past "+str(number)+" years")
    col1,col2 = st.beta_columns([1.8,1])
    with col1:
        data_filter_year = data.loc[data.Date > str(CURRENT_YEAR - number), :]

        fig = go.Figure([go.Scatter(x=data_filter_year['Date'], y=data_filter_year['AAPL.High'], name="Revenue"), go.Scatter(
            x=data_filter_year['Date'], y=data_filter_year['AAPL.Low']*np.random.uniform(low=0.9, high=0.95, size=(data_filter_year.shape[0],)),name="Profits")])

        fig.update_layout(
            title="Revenue & Profit Report for past "+str(number)+" years",
            xaxis_title="Quarters/Years",
            yaxis_title="Amount (Million ¥)",
        )
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        st.write("Geographical Report for Chinese Market")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        image = Image.open('./assets/map.png')
        st.image(image)
    
    col1,col2 = st.beta_columns([1,1])

    with col1:
        df_inc = data_filter_year.copy()
        df_inc.Date = df_inc.Date.apply(lambda x:x[:-3])
        df_inc_gp = df_inc[['AAPL.High','AAPL.Low','Date']].groupby(['Date']).sum().reset_index()

        for ind in df_inc_gp.index[:-1]:
            df_inc_gp.loc[ind,'AAPL.High'] = (df_inc_gp.loc[ind+1,'AAPL.High'] - df_inc_gp.loc[ind,'AAPL.High']) / df_inc_gp.loc[ind,'AAPL.High']
            df_inc_gp.loc[ind,'AAPL.Low'] = (df_inc_gp.loc[ind+1,'AAPL.Low'] - df_inc_gp.loc[ind,'AAPL.Low']) / df_inc_gp.loc[ind,'AAPL.Low']
        
        df_inc_gp.drop(df_inc_gp.index[-1],inplace=True)

        fig = go.Figure([go.Bar(x=df_inc_gp['Date'], y=df_inc_gp['AAPL.High'], name="Revenue"), go.Bar(
            x=df_inc_gp['Date'], y=df_inc_gp['AAPL.Low']*np.random.uniform(low=0.9, high=0.95, size=(df_inc_gp.shape[0],)),name="Profits")])

        fig.update_layout(
            title="Revenue & Profit Perc. Increase",
            xaxis_title="Quarters/Years",
            yaxis_title="Amount (Million ¥)",
        )
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        labels = CATEGORIES
        values = [4500, 2500, 1053, 500, 1000, 3500, 500, 6400]

        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_layout(
            title="Revenue Division for each category",
        )
        st.plotly_chart(fig,use_container_width=True)
            

def show_category_revenue(years_ago, cat='category 1'):
    st.subheader('Detailed revenue & profit report for '+cat)
    data_filter_year = data.loc[data.Date > str(CURRENT_YEAR - years_ago), :]

    fig = go.Figure([go.Scatter(x=data_filter_year['Date'], y=data_filter_year['AAPL.High'], name="Revenue"), go.Scatter(
        x=data_filter_year['Date'], y=data_filter_year['AAPL.Low']*0.3*np.random.uniform(low=0.9, high=0.95, size=(data_filter_year.shape[0],)),name="Profits")])

    fig.update_layout(
        title="Revenue & Profit Report for "+cat+" in past "+str(years_ago)+" years",
        xaxis_title="Quarters/Years",
        yaxis_title="Amount (Million ¥)",
    )
    st.plotly_chart(fig,use_container_width=True)


# def show_profit(number):
#     st.subheader("Profit Report for past "+str(number)+" years")

#     data_filter_year = data.loc[data.Date > str(CURRENT_YEAR - number), :]

#     fig = go.Figure([go.Scatter(x=data_filter_year['Date'],
#                     y=data_filter_year['AAPL.Low']*0.5)])
#     st.plotly_chart(fig)


def show_meaning(key):
    st.info("Tips: Only a sample explanation below.")
    if key == 'curve':
        st.markdown(
            "The curve stands for the _growth and dropdowns_ in revenue and profits in the past "+str(TIME_RANGE)+" years.")
        st.markdown("And *red curve* stands for profits; *blue curve* stands for revenues.")
    elif key == 'peak':
        st.markdown(
            "The peak value which occurred at **" +
            str(PEAK_TIME)+"** reached **"+str(PEAK_VALUE)+"**"
        )
    else:
        pass

    try:
        show_revenue(TIME_RANGE)
    except:
        st.warning("You may have not queried the revenue or profit report. Please do that before checking the meanings.")


def main():
    st.title("Speech Powered BI Dashboard")
    st.write("")
    st.sidebar.header("BI Dashboard")
    with st.sidebar.beta_expander("Notes",expanded=True):
        st.markdown(
            "The data is **fake and only for demonstration purpose**. The data was latest updated in _February, 2021_.")

    result = ''    
    col1, col2 = st.beta_columns(2)

    with col1:
        result = st.text_area(label="Text input",help="You can type in the search query or speack by clicking the button below",max_chars=100,)
    
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if st.button('Search'):
            process_text(result)
    
    st.write("Or you can speak by clicking the button below")

    stt_button = Button(label="Click to Speak", width=120)

    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
    
        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if ( value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.start();
        """))

    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0)

    if result:
        if "GET_TEXT" in result:
            # st.write("You said:")
            st.write("Recognized speech:", result.get("GET_TEXT"))
            process_text(result.get("GET_TEXT"))

main()
