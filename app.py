from bokeh.models.widgets import Button
from bokeh.models import CustomJS

import streamlit as st
import streamlit.components.v1 as components
from streamlit_bokeh_events import streamlit_bokeh_events

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

import pydeck as pdk

import time
import numpy as np
import pandas as pd

from configs.config import *
import utils.SessionState as sessionstate


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


state = sessionstate.get(chat_list=[])


def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start = 12*start_year + start_month - 1
    ym_end = 12*end_year + end_month - 1
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m+1


def show_category():
    chart_data = pd.DataFrame(
        np.random.randn(35, 4),
        index=month_year_iter(8, 2018, 7, 2021),
        columns=['品类'+x for x in ['A', 'B', 'C', 'D']]
    )
    st.area_chart(chart_data)

    def draw_fig():

        y_saving = [33.586, 25.623000000000002, 20.821999999999997, 22.5096999999999996
                    ]
        y_net_worth = [9345.919999999998, 8166.570000000007, 6988.619999999995,
                       7838.529999999999]
        x = ['品类A', '品类B', '品类C', '品类']

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
            name='销售收入，占比总收入',
            orientation='h',
        ), 1, 1)

        fig.append_trace(go.Scatter(
            x=y_net_worth, y=x,
            mode='lines+markers',
            line_color='rgb(128, 0, 128)',
            name='销售收入净值（万）',
        ), 1, 2)

        fig.update_layout(
            title='四大品类的销售收入百分比与净值',
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
    # if cat == 'all':
    #     st.info("Tips: Only a sample plot.")

    st.plotly_chart(draw_fig(), use_container_width=True)
    #     return
    # show_category_revenue(TIME_RANGE, cat)


def show_revenue(number):

    # st.subheader("Revenue Report for past "+str(number)+" years")
    col1, col2 = st.beta_columns([1.8, 1])
    with col1:
        data_filter_year = data.loc[data.Date > str(CURRENT_YEAR - number), :]

        fig = go.Figure([go.Scatter(x=data_filter_year['Date'], y=data_filter_year['AAPL.High'], name="Revenue"), go.Scatter(
            x=data_filter_year['Date'], y=data_filter_year['AAPL.Low']*np.random.uniform(low=0.9, high=0.95, size=(data_filter_year.shape[0],)), name="Profits")])

        fig.update_layout(
            title="过去 "+str(number)+" 年的收入及利润表",
            xaxis_title="季度/年",
            yaxis_title="量 (百万 ¥)",
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
            title="收入&利润增长",
            xaxis_title="季度/年份",
            yaxis_title="比例 (%)",
        )
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.beta_columns([1, 1])

    with col1:
        st.write("中国区市场增长分布")
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
            title="各类收入所占比例",
        )
        st.plotly_chart(fig, use_container_width=True)


def show_category_revenue():
    data_filter_year = data.loc[data.Date > str(CURRENT_YEAR - 1), :]

    fig = go.Figure([go.Scatter(x=data_filter_year['Date'], y=data_filter_year['AAPL.High'], name="Revenue"), go.Scatter(
        x=data_filter_year['Date'], y=data_filter_year['AAPL.Low'], name="Profits")])
    # *0.8*np.random.uniform(low=0.9, high=0.95, size=(data_filter_year.shape[0],)
    fig.update_layout(
        title="A产品在过去三个季度的营收及利润情况",
        xaxis_title="季度/年份",
        yaxis_title="值(百万¥)",
    )
    st.plotly_chart(fig, use_container_width=True)


def show_category_sale():
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [39.90, 116.4],
        columns=['lat', 'lon'])

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=39.90,
            longitude=116.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

  # fig = go.Figure()
    # random_x = [(yr,mth) for (yr, mth) in month_year_iter(10,2020,7,2021)]
    # random_y = np.random.randn(9) * 100000
    # fig.add_trace(go.Scatter(x=random_x, y=random_y,
    #                 mode='lines+markers',
    #                 name='品类A'))
    # fig.update_layout(title='A产品在过去三个季度的销售情况',
    #                xaxis_title='季度/年份',
    #                yaxis_title='数量')
    # st.plotly_chart(fig, use_container_width=True)

    # chart_data = pd.DataFrame(
    #     np.random.randint(100000,1000000,size=(9, 1)),
    #     index=month_year_iter(10,2020,7,2021),
    #     columns=['品类'+x for x in ['A']]
    #     )
    # st.line_chart(chart_data)


def show_meaning(query):
    # st.info("Tips: Only a sample explanation below."

    if '峰值' in query:
        st.write("系统检测到您的问题：峰值在哪里")
        st.success(
            "解释：峰值出现在 **" +
            str(PEAK_TIME)+"** 达到了 **"+str(PEAK_VALUE)+"**"
        )
    if '区域' in query:
        st.write("系统检测到您的问题：区域大小的含义")
        st.success(
            "解释：区域面积表示增长或下降的程度大小。四大品类中，品类A在过去三年的**平均增长率**最高，为**14.2%**。"
        )

    show_category()


def addRecord(user, txt):
    time_string = time.strftime('%H:%M:%S')
    state.chat_list.append((user, txt, time_string))


def visualize(string):
    if string == '':
        pass
    elif string == '营收':
        show_revenue(3)
        # col1, col2 = st.beta_columns([1,2])
        # with col1:
        #     image = Image.open('./assets/revenue_year.png')
        #     st.image(image)
        # with col2:
        #     image = Image.open('./assets/revenue_quarter.png')
        #     st.image(image)
    elif string == '成本':
        col1, col2 = st.beta_columns(2)
        with col1:
            image = Image.open('./assets/cost_year.png')
            st.image(image)
        with col2:
            image = Image.open('./assets/cost_component.png')
            st.image(image)
        image = Image.open('./assets/cost_quarter.png')
        st.image(image)

    elif string == '利润':
        col1, col2, col3 = st.beta_columns([0.8,1.7,1.5])
        with col1:
            image = Image.open('./assets/profit1-1.png')
            st.image(image)
            st.write('')
            st.write('')
            image = Image.open('./assets/profit1-2.png')
            st.image(image)
        with col2:
            image = Image.open('./assets/profit2-1.png')
            st.image(image)
            image = Image.open('./assets/profit2-2.png')
            st.image(image)
        with col3:
            image = Image.open('./assets/profit3-1.png')
            st.image(image)
            image = Image.open('./assets/profit3-2.png')
            st.image(image)

    elif string == '连接BDH':
        st.text('连接中...')
        my_bar = st.progress(0)

        for percent_complete in range(100):
            time.sleep(0.04)
            my_bar.progress(percent_complete + 1)

        image = Image.open('./assets/BDH_Finance.png')
        st.image(image)

    elif string == '销售':
        show_category()

    elif string == '销售细节':
        show_category_sale()

    elif string == '营收细节':
        show_category_revenue()


def process_text(txt):

    if '财务' in txt:
        st.text('系统检测到模糊提问：财务分析，已为您返回财务分析涉及的三大报表，您也可以选择连接BDH查看财务分析仪表板')
        col1, col2, col3, col4 = st.beta_columns([1, 1, 1, 2.5])

        selection = ''
        with col1:
            st.write()
            if st.button('营收趋势图'):
                addRecord('勤答', '模糊提问')
                addRecord('Alex', '营收趋势图')
                selection = '营收'
        with col2:
            st.write()
            if st.button('总利润表'):
                addRecord('勤答', '模糊提问')
                addRecord('Alex', '总利润表')
                selection = '利润'
        with col3:
            st.write()
            if st.button('成本分布'):
                addRecord('勤答', '模糊提问')
                addRecord('Alex', '成本分布')
                selection = '成本'

        # with col4:
        #     query = st.text_input(label='还想看什么信息？')

        # if query:
        #     visualize(query)

        visualize(selection)

        st.write('')
        st.write('')

        with st.beta_expander('连接BDH分析'):
            visualize('连接BDH')

    elif '营收' in txt:
        visualize('营收')

    elif '利润' in txt:
        st.text('系统检测到模糊提问：利润情况，已为您返回与利润相关的所有报表')
        st.write('')
        visualize('利润')

        st.write('您可能还想看：')

        col1, col2, col3, col4 = st.beta_columns([1, 1, 1,4])

        selection = ''
        with col1:
            st.write()
            if st.button('营收趋势图',key='营收趋势图'):
                addRecord('Alex', '营收趋势图')
                selection = '营收'
        
        with col2:
            st.write()
            if st.button('成本分布',key='成本分布'):
                addRecord('Alex', '成本分布')
                selection = '成本'

        with col3:
            st.write()
            if st.button('连接BDH分析',key='连接BDH分析'):
                addRecord('Alex', '连接BDH分析')
                selection = '连接BDH'
 
        visualize(selection)

        # st.write('')
        # st.write('')

        # with st.beta_expander('连接BDH分析'):
        #     visualize('连接BDH')  

    elif '成本' in txt:
        visualize('成本')

    elif '连接' in txt:
        visualize('连接BDH')

    elif '销售' in txt:
        addRecord('勤答', '回复图表')

        st.subheader('默认显示所有分公司最近三年的销售额')
        st.text('可以通过确定年份范围和分公司得到更具体的图像')

        st.write('您使用了语音识别服务，是否同时启用自动分析功能？')
        if st.checkbox('启用'):
            col1, col2, col3 = st.beta_columns(3)
            with col1:
                with st.beta_expander('数据分析'):
                    st.info('''
                    从图像中可以看到，品类D在过去三年中的销售额占比最高，为17.52%；过去三年中，品类D的最高增长率为4.7%，品类C的最高增长率为3.2%，品类B的最高增长率为2.2%。总的来看，品类A的复合增长率最高，为13%，建议下一阶段增加产品投入。
                    ''')

            with col2:
                with st.beta_expander('指标分析'):
                    st.info('''
                    过去季度的销售毛利率为20%，add more。
                    ''')

            with col3:
                with st.beta_expander('市场分析'):
                    st.info('''
                    过去季度的销售毛利率为20%，市场同期为15%，比市场高约33%。
                    ''')
        visualize('销售')



    elif '峰值' in txt or '含义' in txt or '区域' in txt:
        addRecord('勤答', '回复文字')
        show_meaning(txt)

    elif '季度' in txt:
        addRecord('勤答', '回复图表及文字')

        col1, col2 = st.beta_columns([1.2, 1])

        with col1:
            # st.markdown('A产品在过去三个季度的**营收及利润情况**')
            visualize('营收细节')

        with col2:
            st.markdown('A产品在过去三个季度的**销售情况**')
            visualize('销售细节')

        st.write('您使用了语音识别服务，是否同时启用自动分析功能？')
        if st.checkbox('启用'):
            col1, col2, col3 = st.beta_columns(3)
            with col1:
                with st.beta_expander('数据分析'):
                    st.info('''
                    从图像中可以看到，品类D在过去三年中的销售额占比最高，为17.52%；过去三年中，品类D的最高增长率为4.7%，品类C的最高增长率为3.2%，品类B的最高增长率为2.2%。总的来看，品类A的复合增长率最高，为13%，建议下一阶段增加产品投入。
                    ''')

            with col2:
                with st.beta_expander('指标分析'):
                    st.info('''
                    过去季度的销售毛利率为20%，add more。
                    ''')

            with col3:
                with st.beta_expander('市场分析'):
                    st.info('''
                    A产品在过去三个季度中营收净增长达30%，利润增长为10%；A产品主要为夏季使用产品，销售增长可能与最近的气温上涨相关。
                    ''')


def main():
    st.title("🤖 勤答：便携式数据交互平台")
    st.write("")
    st.sidebar.header("勤答")

    result_audio = result_text = ''
    col1, col2 = st.beta_columns(2)

    with col1:
        st.write("语音输入按键")

        stt_button = Button(label="点击说话", width=120)

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
            help="示例：请展示最近三年的营收情况", label="文本输入", max_chars=100)

    # components.iframe('https://bdhtest.tax.deloitte.com.cn/home')
    if result_audio:
        # st.write("You said:")
        st.text("识别结果: "+result_audio.get("GET_TEXT"))
        st.write('')
        st.write('')
        addRecord('Alex', result_audio.get("GET_TEXT"))
        process_text(result_audio.get("GET_TEXT"),)
    elif result_text:
        addRecord('Alex', result_text)
        process_text(result_text)

    with st.sidebar.beta_container():
        st.write('')

    with st.sidebar.beta_expander('聊天记录'):
        try:
            # names, messages, times = zip(*state.chat_list)
            df = pd.DataFrame(
                state.chat_list,
                columns=['讲话者', '内容', '时间点']
            )
            st.dataframe(df)
        except ValueError:
            pass

        if len(state.chat_list) > 10:
            del (state.chat_list[0])


    with st.sidebar.beta_expander('近期新闻'):
        components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div id="accordion">
        <div class="card">
            <div class="card-header" id="headingOne">
            <h5 class="mb-0">
                <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                市场动态更新
                </button>
            </h5>
            </div>
            <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
            <div class="card-body">
                Sensex, Nifty达到今日最低点， Nifty Bank 跌幅超过2%
            </div>
            </div>
        </div>
        <div class="card">
            <div class="card-header" id="headingTwo">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                Dow futures下降超过300个点
                </button>
            </h5>
            </div>
            <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
            <div class="card-body">
                U.S. stock futures slumped on Monday morning, with reopening concerns triggered by new cases at the Olympic village ahead of the opening ceremony, and new restrictions imposed on travel to France by the U.K., which separately reduced its coronavirus rules for England.
            </div>
            </div>
        </div>
        <div class="card">
            <div class="card-header" id="headingThree">
            <h5 class="mb-0">
                <button class="btn btn-link" data-toggle="collapse" data-target="#collapseThree" aria-expanded="true" aria-controls="collapseThree">
                CEE MARKETS-Forint达到近两个月以来新低
                </button>
            </h5>
            </div>
            <div id="collapseThree" class="collapse show" aria-labelledby="headingThree" data-parent="#accordion">
            <div class="card-body">
                PRAGUE, July 19 (Reuters) - Central Europe's currencies fell on Monday, starting the week on a sour note amid global market weakness as coronavirus cases rise in different parts of the world, with the Hungarian forint touching a fresh 2-1/2 month low.
            </div>
            </div>
        </div>
        </div>
        """,
        height=200,
        )

    
    with st.sidebar.beta_expander('分享报告'):
        col1,col2,col3,col4 = st.beta_columns(4)

        with col1:
            link = '''
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <a href="#" class="fa fa-facebook"></a>
            '''
            st.markdown(link, unsafe_allow_html=True)

        with col2:
            link = '''
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <a href="#" class="fa fa-twitter"></a>
            '''
            st.markdown(link, unsafe_allow_html=True)

        with col3:
            link = '''
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <a href="#" class="fa fa-linkedin"></a>
            '''
            # link = '<img src="./assets/linkedin_logo.png">[领英](https://www.linkedin.com/home/?originalSubdomain=sg)'
            st.markdown(link, unsafe_allow_html=True)            
        
        with col4:
            link = '''
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <a href="#" class="fa fa-skype"></a>
            '''
            # link = '<img src="./assets/linkedin_logo.png">[领英](https://www.linkedin.com/home/?originalSubdomain=sg)'
            st.markdown(link, unsafe_allow_html=True)     

        st.write('') 


main()