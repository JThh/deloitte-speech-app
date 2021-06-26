import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

import numpy as np
import pandas as pd
from number_parser import parse
import dateparser


def process_text(txt):
    '''
    Function for processing text and extracting key information.
    '''
    assert txt != ''
    
    num_txt = parse(txt)
    
    number = 5
    if num_txt != txt:
        number = [int(s) for s in num_txt.split() if s.isdigit()][0]
    
    if 'category' in txt:
        categories = show_category()
        if 'revenue' in txt:
            for cat in categories:
                show_revenue(number,cat)
        if 'profit' in txt:
            for cat in categories:
                show_profit(number,cat)

    if 'revenue' in txt:
        show_revenue(number)
    if 'profit' in txt:
        show_profit(number)

def show_category():
    pass

def show_revenue(number,cat='all'):
    print("Revenue Report")

def show_profit(number,cat='all'):
    pass


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
        st.write('I heard',result.get("GET_TEXT"))
        speech = result.get("GET_TEXT")
        process_text(speech)

            
                
        
