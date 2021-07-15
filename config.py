import pickle

DICT_PATH = './dict.txt'
PICKLE_PATH = './kg_base.p'

# Dynamically increasing
STOP_WORDS = ['a','the','report','show','me','you','for','last']

with open(PICKLE_PATH, 'rb') as handle:
    KGB = pickle.load(handle)
    

# CHINESE_NUMBERS = ['一','二','三','四','五','六','七','八','九','十']
# KGB = {
#     'database_entities': [
#         '营业总收入',
#         '营业收入',
#         '营业成本',
#         '税金及附加',
#         '销售费用',
#         '管理费用',
#         '财务费用',
#         '资产减值损失',
#         '公允价值变动收益',
#         '投资收益',
#         '其中:对联营企业和合营企业的投资收益',
#         '汇兑收益',
#         '三、营业利润',
#         '加:营业外收入',
#         '减：营业外支出',
#         '其中：非流动资产处置损失',
#         '四、利润总额',
#         '减：所得税费用',
#         '五、净利润',
#         '归属于母公司所有者的净利润',
#         '少数股东损益',
#         '基本每股收益(元/股)',
#         '稀释每股收益(元/股)',
#         '七、其他综合收益',
#         '八、综合收益总额'
#         '归属于母公司所有者的综合收益总额',
#         '归属于少数股东的综合收益总额',
#         '营业净利率',
#         '息税前利润',
#         '毛利率',
#         ],
#     'calling_entities': {
#         ('总营收','创收','收入','一、营业总收入','total revenue','total operating revenue','gross revenue'): '一、营业总收入',
#         ('营业收入','revenue','营收','sales','运营收入','经营收入','operating income','turnover','operating revenue' ,'营业额','sales revenue'):'营业收入',
#         ('二、营业总成本','total cost','total operating cost'):'二、营业总成本',
#         ('营业成本','operating cost','cost of goods sold','cost of sales'):'营业成本',
#         ():'',
#         ():'',
#         ():'',
#         ():'',
#         ():'',
#         ():'',
#         ():'',

#     },
#     'time_units': ['年','月','星期','季度'],
#     'numbers': [i for i in range(1,100)] + CHINESE_NUMBERS,
#     'chart_types': [
#         '折线图',
#         '饼图',
#         '圆环图',
#         '财务指标',
#         '对比',
#         '瀑布图'],
#     'locations': ['全国'],
#     'requirements': {'营业收入': ['time_units',''], },
#     'defaults': {}
# }