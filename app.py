from bokeh.models.textures import ImageURLTexture
import streamlit as st
import streamlit.components.v1 as components
from bokeh.models.widgets import Button, Dropdown
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
# import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from config import *
import numpy as np

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


def process_text(txt):
    '''
    Function for processing text and extracting key information.
    '''
    assert txt != ''

    try:
        TIME_RANGE = [int(s) for s in txt.split() if s.isdigit()][0]
    except:
        #st.warning('Please provide a time range.')
        pass

    if 'mean' in txt.lower():
        for x in EXPLAINABLE_TXT:
            if x in txt:
                show_meaning(x)
                return
        st.warning(
            "This is not yet explainable. More comprehensive explanations are expected to be filled in soon.")

    if 'catego' in txt.lower():
        for cat in CATEGORIES:
            if cat in txt:
                show_category(cat)
        show_category()
        return

    if 'revenue' in txt.lower() or 'profit' in txt.lower():
        show_revenue(TIME_RANGE)

    if 'thank' in txt.lower():
        st.write("You're welcome! ^-^")


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
        st.info("Tips: Only a sample plot.")

        st.plotly_chart(draw_fig(), use_container_width=True)
        return
    if cat not in CATEGORIES:
        st.warning("Please select a category in the categories list.")
    else:
        show_category_revenue(TIME_RANGE, cat)


def show_revenue(number):

    # st.subheader("Revenue Report for past "+str(number)+" years")
    col1, col2 = st.beta_columns([1.8, 1])
    with col1:
        data_filter_year = data.loc[data.Date > str(CURRENT_YEAR - number), :]

        fig = go.Figure([go.Scatter(x=data_filter_year['Date'], y=data_filter_year['AAPL.High'], name="Revenue"), go.Scatter(
            x=data_filter_year['Date'], y=data_filter_year['AAPL.Low']*np.random.uniform(low=0.9, high=0.95, size=(data_filter_year.shape[0],)), name="Profits")])

        fig.update_layout(
            title="Revenue & Profit Report for past "+str(number)+" years",
            xaxis_title="Quarters/Years",
            yaxis_title="Amount (Million ¥)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df_inc = data_filter_year.copy()
        df_inc.Date = df_inc.Date.apply(lambda x: x[:-3])
        df_inc_gp = df_inc[['AAPL.High', 'AAPL.Low', 'Date']
                           ].groupby(['Date']).sum().reset_index()

        for ind in df_inc_gp.index[:-1]:
            df_inc_gp.loc[ind, 'AAPL.High'] = (
                df_inc_gp.loc[ind+1, 'AAPL.High'] - df_inc_gp.loc[ind, 'AAPL.High']) / df_inc_gp.loc[ind, 'AAPL.High']
            df_inc_gp.loc[ind, 'AAPL.Low'] = (
                df_inc_gp.loc[ind+1, 'AAPL.Low'] - df_inc_gp.loc[ind, 'AAPL.Low']) / df_inc_gp.loc[ind, 'AAPL.Low']

        df_inc_gp.drop(df_inc_gp.index[-1], inplace=True)

        fig = go.Figure([go.Line(x=df_inc_gp['Date'], y=df_inc_gp['AAPL.High'], name="Revenue"), go.Line(
            x=df_inc_gp['Date'], y=df_inc_gp['AAPL.Low']*np.random.uniform(low=0.5, high=0.85, size=(df_inc_gp.shape[0],)), name="Profits")])

        fig.update_layout(
            title="Revenue & Profit Perc. Increase",
            xaxis_title="Quarters/Years",
            yaxis_title="Percentage (%)",
        )
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.beta_columns([1, 1])

    with col1:
        st.write("Geographical Report for Chinese Market")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        image = Image.open('./assets/map.png')
        st.image(image)

    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        labels = CATEGORIES
        values = [4500, 2500, 1053, 500, 1000, 3500, 500, 6400]

        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_layout(
            title="Revenue Division for each category",
        )
        st.plotly_chart(fig, use_container_width=True)


def show_category_revenue(years_ago, cat='category 1'):
    st.subheader('Detailed revenue & profit report for '+cat)
    data_filter_year = data.loc[data.Date > str(CURRENT_YEAR - years_ago), :]

    fig = go.Figure([go.Scatter(x=data_filter_year['Date'], y=data_filter_year['AAPL.High'], name="Revenue"), go.Scatter(
        x=data_filter_year['Date'], y=data_filter_year['AAPL.Low']*0.3*np.random.uniform(low=0.9, high=0.95, size=(data_filter_year.shape[0],)), name="Profits")])

    fig.update_layout(
        title="Revenue & Profit Report for "+cat +
        " in past "+str(years_ago)+" years",
        xaxis_title="Quarters/Years",
        yaxis_title="Amount (Million ¥)",
    )
    st.plotly_chart(fig, use_container_width=True)


def show_meaning(key):
    st.info("Tips: Only a sample explanation below.")
    if key.lower() == 'curve':
        st.markdown(
            "The curve stands for the _growth and dropdowns_ in revenue and profits in the past "+str(TIME_RANGE)+" years.")
        st.markdown(
            "And *red curve* stands for profits; *blue curve* stands for revenues.")
    elif key.lower() == 'peak':
        st.markdown(
            "The peak value which occurred at **" +
            str(PEAK_TIME)+"** reached **"+str(PEAK_VALUE)+"**"
        )
    else:
        pass

    try:
        show_revenue(TIME_RANGE)
    except:
        st.warning(
            "You may have not queried the revenue or profit report. Please do that before checking the meanings.")


def main():
    st.title("Speech Powered BI Dashboard")
    st.write("")
    st.sidebar.header("BI Dashboard")
    with st.sidebar.beta_expander("Notes", expanded=True):
        st.markdown(
            "The data is **fake and only for demonstration purpose**. The data was latest updated in _February, 2021_.")

    result_audio = result_text = ''
    col1, col2 = st.beta_columns(2)

    with col1:
        st.write("Speak by clicking the button below")

        # menu = [("普通话", "cmn-Hans-CN"), ("粵語", "yue-Hant-HK"), ("English", "en-US")]

        # dropdown = Dropdown(label="select language", margin=(0,0,0,0), menu=menu)

        # dropdown.js_on_event("menu_item_click", CustomJS(code="var selected_lang = "))

        stt_button = Button(label="Click to Speak", width=120)

        stt_button.js_on_event("button_click", CustomJS(code="""
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'cmn-Hans-CN';
        
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

        result_audio = streamlit_bokeh_events(
            stt_button,
            events="GET_TEXT",
            key="listen",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)

    with col2:
        result_text = st.text_input(
            help="示例：请展示最近三年的营收情况", label="Text input", max_chars=100)

    if result_audio:
        # st.write("You said:")
        st.text("Recognized speech: "+result_audio.get("GET_TEXT"))
        st.write('')
        st.write('')
        process_text(result_audio.get("GET_TEXT"))
    elif result_text:
        process_text(result_text)
    else:
        pass


# bootstrap 4 collapse example
    components.html(
    """
<!DOCTYPE html>
<meta charset="utf-8">
<title>Web Speech API Demo</title>
<style>
  * {
    font-family: Verdana, Arial, sans-serif;
  }
  a:link {
    color:#000;
    text-decoration: none;
  }
  a:visited {
    color:#000;
  }
  a:hover {
    color:#33F;
  }
  .button {
    background: -webkit-linear-gradient(top,#008dfd 0,#0370ea 100%);
    border: 1px solid #076bd2;
    border-radius: 3px;
    color: #fff;
    display: none;
    font-size: 13px;
    font-weight: bold;
    line-height: 1.3;
    padding: 8px 25px;
    text-align: center;
    text-shadow: 1px 1px 1px #076bd2;
    letter-spacing: normal;
  }
  .center {
    padding: 10px;
    text-align: center;
  }
  .final {
    color: black;
    padding-right: 3px; 
  }
  .interim {
    color: gray;
  }
  .info {
    font-size: 14px;
    text-align: center;
    color: #777;
    display: none;
  }
  .right {
    float: right;
  }
  .sidebyside {
    display: inline-block;
    width: 45%;
    min-height: 40px;
    text-align: left;
    vertical-align: top;
  }
  #headline {
    font-size: 40px;
    font-weight: 300;
  }
  #info {
    font-size: 20px;
    text-align: center;
    color: #777;
    visibility: hidden;
  }
  #results {
    font-size: 14px;
    font-weight: bold;
    border: 1px solid #ddd;
    padding: 15px;
    text-align: left;
    min-height: 150px;
  }
  #start_button {
    border: 0;
    background-color:transparent;
    padding: 0;
  }
</style>
<h1 class="center" id="headline">
  <a href="http://dvcs.w3.org/hg/speech-api/raw-file/tip/speechapi.html">
    Web Speech API</a> Demonstration</h1>
<div id="info">
  <p id="info_start">Click on the microphone icon and begin speaking.</p>
  <p id="info_speak_now">Speak now.</p>
  <p id="info_no_speech">No speech was detected. You may need to adjust your
    <a href="//support.google.com/chrome/bin/answer.py?hl=en&amp;answer=1407892">
      microphone settings</a>.</p>
  <p id="info_no_microphone" style="display:none">
    No microphone was found. Ensure that a microphone is installed and that
    <a href="//support.google.com/chrome/bin/answer.py?hl=en&amp;answer=1407892">
    microphone settings</a> are configured correctly.</p>
  <p id="info_allow">Click the "Allow" button above to enable your microphone.</p>
  <p id="info_denied">Permission to use microphone was denied.</p>
  <p id="info_blocked">Permission to use microphone is blocked. To change,
    go to chrome://settings/contentExceptions#media-stream</p>
  <p id="info_upgrade">Web Speech API is not supported by this browser.
     Upgrade to <a href="//www.google.com/chrome">Chrome</a>
     version 25 or later.</p>
</div>
<div class="right">
  <button id="start_button" onclick="startButton(event)">
    <img id="start_img" src="mic.gif" alt="Start"></button>
</div>
<div id="results">
  <span id="final_span" class="final"></span>
  <span id="interim_span" class="interim"></span>
  <p>
</div>
<div class="center">
  <div class="sidebyside" style="text-align:right">
    <button id="copy_button" class="button" onclick="copyButton()">
      Copy and Paste</button>
    <div id="copy_info" class="info">
      Press Control-C to copy text.<br>(Command-C on Mac.)
    </div>
  </div>
  <div class="sidebyside">
    <button id="email_button" class="button" onclick="emailButton()">
      Create Email</button>
    <div id="email_info" class="info">
      Text sent to default email application.<br>
      (See chrome://settings/handlers to change.)
    </div>
  </div>
  <p>
  <div id="div_language">
    <select id="select_language" onchange="updateCountry()"></select>
    &nbsp;&nbsp;
    <select id="select_dialect"></select>
  </div>
</div>
<script>
var langs =
[['Afrikaans',       ['af-ZA']],
 ['Bahasa Indonesia',['id-ID']],
 ['Bahasa Melayu',   ['ms-MY']],
 ['Català',          ['ca-ES']],
 ['Čeština',         ['cs-CZ']],
 ['Deutsch',         ['de-DE']],
 ['English',         ['en-AU', 'Australia'],
                     ['en-CA', 'Canada'],
                     ['en-IN', 'India'],
                     ['en-NZ', 'New Zealand'],
                     ['en-ZA', 'South Africa'],
                     ['en-GB', 'United Kingdom'],
                     ['en-US', 'United States']],
 ['Español',         ['es-AR', 'Argentina'],
                     ['es-BO', 'Bolivia'],
                     ['es-CL', 'Chile'],
                     ['es-CO', 'Colombia'],
                     ['es-CR', 'Costa Rica'],
                     ['es-EC', 'Ecuador'],
                     ['es-SV', 'El Salvador'],
                     ['es-ES', 'España'],
                     ['es-US', 'Estados Unidos'],
                     ['es-GT', 'Guatemala'],
                     ['es-HN', 'Honduras'],
                     ['es-MX', 'México'],
                     ['es-NI', 'Nicaragua'],
                     ['es-PA', 'Panamá'],
                     ['es-PY', 'Paraguay'],
                     ['es-PE', 'Perú'],
                     ['es-PR', 'Puerto Rico'],
                     ['es-DO', 'República Dominicana'],
                     ['es-UY', 'Uruguay'],
                     ['es-VE', 'Venezuela']],
 ['Euskara',         ['eu-ES']],
 ['Français',        ['fr-FR']],
 ['Galego',          ['gl-ES']],
 ['Hrvatski',        ['hr_HR']],
 ['IsiZulu',         ['zu-ZA']],
 ['Íslenska',        ['is-IS']],
 ['Italiano',        ['it-IT', 'Italia'],
                     ['it-CH', 'Svizzera']],
 ['Magyar',          ['hu-HU']],
 ['Nederlands',      ['nl-NL']],
 ['Norsk bokmål',    ['nb-NO']],
 ['Polski',          ['pl-PL']],
 ['Português',       ['pt-BR', 'Brasil'],
                     ['pt-PT', 'Portugal']],
 ['Română',          ['ro-RO']],
 ['Slovenčina',      ['sk-SK']],
 ['Suomi',           ['fi-FI']],
 ['Svenska',         ['sv-SE']],
 ['Türkçe',          ['tr-TR']],
 ['български',       ['bg-BG']],
 ['Pусский',         ['ru-RU']],
 ['Српски',          ['sr-RS']],
 ['한국어',            ['ko-KR']],
 ['中文',             ['cmn-Hans-CN', '普通话 (中国大陆)'],
                     ['cmn-Hans-HK', '普通话 (香港)'],
                     ['cmn-Hant-TW', '中文 (台灣)'],
                     ['yue-Hant-HK', '粵語 (香港)']],
 ['日本語',           ['ja-JP']],
 ['Lingua latīna',   ['la']]];

for (var i = 0; i < langs.length; i++) {
  select_language.options[i] = new Option(langs[i][0], i);
}
select_language.selectedIndex = 6;
updateCountry();
select_dialect.selectedIndex = 6;
showInfo('info_start');

function updateCountry() {
  for (var i = select_dialect.options.length - 1; i >= 0; i--) {
    select_dialect.remove(i);
  }
  var list = langs[select_language.selectedIndex];
  for (var i = 1; i < list.length; i++) {
    select_dialect.options.add(new Option(list[i][1], list[i][0]));
  }
  select_dialect.style.visibility = list[1].length == 1 ? 'hidden' : 'visible';
}

var create_email = false;
var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;
if (!('webkitSpeechRecognition' in window)) {
  upgrade();
} else {
  start_button.style.display = 'inline-block';
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onstart = function() {
    recognizing = true;
    showInfo('info_speak_now');
    start_img.src = 'mic-animate.gif';
  };

  recognition.onerror = function(event) {
    if (event.error == 'no-speech') {
      start_img.src = 'mic.gif';
      showInfo('info_no_speech');
      ignore_onend = true;
    }
    if (event.error == 'audio-capture') {
      start_img.src = 'mic.gif';
      showInfo('info_no_microphone');
      ignore_onend = true;
    }
    if (event.error == 'not-allowed') {
      if (event.timeStamp - start_timestamp < 100) {
        showInfo('info_blocked');
      } else {
        showInfo('info_denied');
      }
      ignore_onend = true;
    }
  };

  recognition.onend = function() {
    recognizing = false;
    if (ignore_onend) {
      return;
    }
    start_img.src = 'mic.gif';
    if (!final_transcript) {
      showInfo('info_start');
      return;
    }
    showInfo('');
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
      var range = document.createRange();
      range.selectNode(document.getElementById('final_span'));
      window.getSelection().addRange(range);
    }
    if (create_email) {
      create_email = false;
      createEmail();
    }
  };

  recognition.onresult = function(event) {
    var interim_transcript = '';
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    final_transcript = capitalize(final_transcript);
    final_span.innerHTML = linebreak(final_transcript);
    interim_span.innerHTML = linebreak(interim_transcript);
    if (final_transcript || interim_transcript) {
      showButtons('inline-block');
    }
  };
}

function upgrade() {
  start_button.style.visibility = 'hidden';
  showInfo('info_upgrade');
}

var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
  return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

var first_char = /\S/;
function capitalize(s) {
  return s.replace(first_char, function(m) { return m.toUpperCase(); });
}

function createEmail() {
  var n = final_transcript.indexOf('\n');
  if (n < 0 || n >= 80) {
    n = 40 + final_transcript.substring(40).indexOf(' ');
  }
  var subject = encodeURI(final_transcript.substring(0, n));
  var body = encodeURI(final_transcript.substring(n + 1));
  window.location.href = 'mailto:?subject=' + subject + '&body=' + body;
}

function copyButton() {
  if (recognizing) {
    recognizing = false;
    recognition.stop();
  }
  copy_button.style.display = 'none';
  copy_info.style.display = 'inline-block';
  showInfo('');
}

function emailButton() {
  if (recognizing) {
    create_email = true;
    recognizing = false;
    recognition.stop();
  } else {
    createEmail();
  }
  email_button.style.display = 'none';
  email_info.style.display = 'inline-block';
  showInfo('');
}

function startButton(event) {
  if (recognizing) {
    recognition.stop();
    return;
  }
  final_transcript = '';
  recognition.lang = select_dialect.value;
  recognition.start();
  ignore_onend = false;
  final_span.innerHTML = '';
  interim_span.innerHTML = '';
  start_img.src = 'mic-slash.gif';
  showInfo('info_allow');
  showButtons('none');
  start_timestamp = event.timeStamp;
}

function showInfo(s) {
  if (s) {
    for (var child = info.firstChild; child; child = child.nextSibling) {
      if (child.style) {
        child.style.display = child.id == s ? 'inline' : 'none';
      }
    }
    info.style.visibility = 'visible';
  } else {
    info.style.visibility = 'hidden';
  }
}

var current_style;
function showButtons(style) {
  if (style == current_style) {
    return;
  }
  current_style = style;
  copy_button.style.display = style;
  email_button.style.display = style;
  copy_info.style.display = 'none';
  email_info.style.display = 'none';
}
</script>
        """,
        height=600,
    )


main()
