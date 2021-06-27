import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import plotly.express as px
import plotly.graph_objects as go


import numpy as np
import pandas as pd
# from number_parser import parse
import dateparser

# DATA_URL = "https://drive.google.com/uc?export=download&id=1lU52Rr6hf9d1H_kWPwQYQMaCwzLcbLFr"

# data = pd.read_csv(DATA_URL)

CURRENT_YEAR = 2021
TIME_RANGE = 5

data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
data.loc[:,'Date'] = data.loc[:,'Date'].apply(lambda x:str(int(x[:4])+4)+x[4:])

def process_text(txt):
    '''
    Function for processing text and extracting key information.
    '''
    assert txt != ''
    
    # num_txt = parse(txt)
    try:
        TIME_RANGE = [int(s) for s in txt.split() if s.isdigit()][0]
    except:
        st.warning('Please provide a time range.')
    # if num_txt != txt:
    #     number = [int(s) for s in num_txt.split() if s.isdigit()][0]
    if 'mean' in txt:
        show_meaning(txt)

    if 'category' in txt:
        show_category()
        # if 'revenue' in txt:
        #     for cat in categories:
        #         show_revenue(number,cat)
        # if 'profit' in txt:
        #     for cat in categories:
        #         show_profit(number,cat)

    if 'revenue' in txt:
        show_revenue(TIME_RANGE)
    if 'profit' in txt:
        show_profit(TIME_RANGE)

def show_category():
    pass

def show_revenue(number,cat='all'):
    st.subheader("Revenue Report for past "+str(number)+" years")

    data_filter_year = data.loc[data.Date > str(CURRENT_YEAR - number),:]

    fig = go.Figure([go.Scatter(x=data_filter_year['Date'], y=data_filter_year['AAPL.High'])])
    st.plotly_chart(fig)

def show_profit(number,cat='all'):
    st.subheader("Profit Report for past "+str(number)+" years")

    data_filter_year = data.loc[data.Date > str(CURRENT_YEAR - number),:]

    fig = go.Figure([go.Scatter(x=data_filter_year['Date'], y=data_filter_year['AAPL.Low']*0.5)])
    st.plotly_chart(fig)


def main():
    st.title("Speech Enhanced BI App")
    st.sidebar.header("Speech BI")
    st.sidebar.write("The data is fake and only for demonstration purpose. The data was lastest updated in 2018.")
    stt_button = Button(label="Click to Speak", width=100)

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
            st.write("Recognized speech:",result.get("GET_TEXT"))
            process_text(result.get("GET_TEXT"))

main()