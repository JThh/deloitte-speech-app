from bokeh.models.textures import ImageURLTexture
from bokeh.models.widgets import Button, Dropdown
from bokeh.models import CustomJS

import streamlit as st
import streamlit.components.v1 as components
from streamlit_bokeh_events import streamlit_bokeh_events

# import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
import time
import numpy as np
import pandas as pd

from config import *
from config_prev import *
from utils import TextAnalyzer
import SessionState

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

state = SessionState.get(chat_list=[])

def month_year_iter( start_month, start_year, end_month, end_year ):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end ):
        y, m = divmod( ym, 12 )
        yield y, m+1

def show_category(cat='all'):
    chart_data = pd.DataFrame(
        np.random.randn(35, 4),
        index=month_year_iter(8,2018,7,2021),
        columns=['品类'+x for x in ['A','B','C','D']]
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

def show_profit():
    pass

def show_category_revenue(years_ago):
    data_filter_year = data.loc[data.Date > str(CURRENT_YEAR - years_ago), :]

    fig = go.Figure([go.Scatter(x=data_filter_year['Date'], y=data_filter_year['AAPL.High'], name="Revenue"), go.Scatter(
        x=data_filter_year['Date'], y=data_filter_year['AAPL.Low']*0.8*np.random.uniform(low=0.9, high=0.95, size=(data_filter_year.shape[0],)), name="Profits")])

    fig.update_layout(
        xaxis_title="季度/年份",
        yaxis_title="值(百万¥)",
    )
    st.plotly_chart(fig, use_container_width=True)


def show_meaning():
    # st.info("Tips: Only a sample explanation below.")
    st.info(
        "年份为：从"+str(CURRENT_YEAR - TIME_RANGE)+ "到"+str(CURRENT_YEAR))
    # st.markdown(
    #     "颜色代表品类，面积大小表示涨幅或跌幅")
    st.info(
        "峰值出现在 **" +
        str(PEAK_TIME)+"** 达到了 **"+str(PEAK_VALUE)+"**"
    )

    show_category('all')


def addRecord(user,txt):
    time_string = time.strftime('%H:%M:%S')
    state.chat_list.append((user,txt, time_string))  


def visualize(string):
    if string == '':
        pass
    elif string == '营收':
        show_revenue(5)
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
        show_profit()
        col1, col2 = st.beta_columns(2)
        with col1:
            image = Image.open('./assets/profit_year.png')
            st.image(image)
        with col2:
            image = Image.open('./assets/profit_quarter.png')
            st.image(image)  

    elif string == '全局':
        image = Image.open('./assets/BDH_Finance.png')
        st.image(image)   

    elif string == '销售':
        show_category('all')

    elif string == '销售细节':
        show_category_revenue(3)

    elif string == '意义':
        show_meaning()


def process_text_v2(txt):
    # analyzer = TextAnalyzer(txt,KGB,False)

    # queries, success = analyzer.run()

    # if success:
    #     for q in queries:
    #         st.write(q)
    #         state.chat_list.append(('勤答',q, time_string))
    #         visualize(q)
    # else:
    #     msg = queries
    #     st.write(msg)
    #     state.chat_list.append(('勤答',msg, time_string))


    if '财务' in txt:
        col1, col2, col3, col4 = st.beta_columns(4)

        selection = ''
        with col1:
            if st.button('营收趋势图'):
                addRecord('勤答','模糊提问')
                addRecord('Alex','营收趋势图')
                selection = '营收'
        with col2:
            if st.button('总利润表'):
                addRecord('勤答','模糊提问')
                addRecord('Alex','总利润表')
                selection = '利润'
        with col3:
            if st.button('成本分布'): 
                addRecord('勤答','模糊提问')
                addRecord('Alex','成本分布')  
                selection = '成本'
        with col4:
            if st.button('连接BDH-全局预览'): 
                addRecord('勤答','模糊提问')
                addRecord('Alex','连接BDH-全局预览')  
                selection = '全局'

        visualize(selection)     

    elif '销售' in txt:
        addRecord('勤答','回复图表')

        st.subheader('默认显示所有分公司最近三年的销售额')
        st.text('可以通过确定年份范围和分公司得到更具体的图像')
        visualize('销售')

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

    elif '意义' in txt:
        addRecord('勤答','回复文字')
        visualize('意义')

    elif '季度' in txt:
        addRecord('勤答','回复图表及文字')
        visualize('销售细节')
        st.write('您使用了语音识别服务，是否同时启用自动分析功能？')
        if st.checkbox('启用'):
            st.info('''
            A产品在过去三个季度中营收净增长达30%，利润增长为10%；A产品主要为夏季使用产品，销售增长可能与最近的气温上涨相关。
            ''')     
        st.subheader('A产品在过去三个季度的营收报告')  
        

    # elif '毛利率' in txt:
    #     addRecord('勤答','回复文字')
    #     st.write('检测到计算指标，是否启用关联分析功能？')
    #     if st.checkbox('启用'):
    #         st.info('''
    #         过去季度的销售毛利率为20%，市场同期为15%，比市场高约33%
    #         ''')       
    #     st.text('默认为过去一个季度的所有产品')
    #     visualize('关联分析')


    
def main():
    st.title("勤答：便携式数据交互平台")
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
        addRecord('Alex',result_audio.get("GET_TEXT"))
        process_text_v2(result_audio.get("GET_TEXT"),)
    elif result_text:
        addRecord('Alex',result_text)
        process_text_v2(result_text)

    st.sidebar.markdown('聊天记录：')

    try:
        # names, messages, times = zip(*state.chat_list)
        df = pd.DataFrame(
            state.chat_list,
            columns=['讲话者','内容','时间点']
        )
        st.sidebar.dataframe(df)
    except ValueError:
        pass

    if len(state.chat_list) > 10:
        del (state.chat_list[0])
    

main()


# def process_text(txt):
#     '''
#     Function for processing text and extracting key information.
#     '''
#     assert txt != ''

#     try:
#         TIME_RANGE = [int(s) for s in txt.split() if s.isdigit()][0]
#     except:
#         #st.warning('Please provide a time range.')
#         pass

#     if 'mean' in txt.lower():
#         for x in EXPLAINABLE_TXT:
#             if x in txt:
#                 show_meaning(x)
#                 return
#         st.warning(
#             "This is not yet explainable. More comprehensive explanations are expected to be filled in soon.")

#     if 'catego' in txt.lower():
#         for cat in CATEGORIES:
#             if cat in txt:
#                 show_category(cat)
#         show_category()
#         return

#     if 'revenue' in txt.lower() or 'profit' in txt.lower():
#         show_revenue(TIME_RANGE)

#     if 'thank' in txt.lower():
#         st.write("You're welcome! ^-^")


