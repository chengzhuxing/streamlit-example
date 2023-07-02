# -*- coding: utf-8 -*-

"""
Created on Thu Jun  1 08:58:19 2023

@author: 65475
"""

# streanlit绝对收益部分


import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_option_menu import option_menu
from streamlit_echarts import st_echarts





path = r"C:\Users\65475\gy2022\报告\专题报告\大类资产配置\资产配置.csv"
path2 = r"C:\Users\65475\gy2022\报告\专题报告\大类资产配置\res_nav.csv"

st.set_page_config(page_title="Today", page_icon="random", layout="wide",initial_sidebar_state='auto')
st.title('资产配置')

st.markdown('''基差是衍生品交易中最为重要的指标之一，但是由于指数成分股分红时指数价格的自然回落，导致盘面基差包含了市场对于未来指数分红的预期，出现季节性的贴水，而剔除分红影响后的基差，才更能反应实际的基差情况。下图/表是通过对指数未来分红点位的预测，定期跟踪的经分红调整后的实际基差情况。注本文定义的基差为期货价格-现货价格，详细内容请参照 [《股指期货基差之分红点位预测》](https://mp.weixin.qq.com/s/E4eLNnLaRVAsnTQgylP-bg)  ''')


# "C:\Users\65475\gy2022\报告\专题报告\大类资产配置\【国元金工】如何用ETF构造绝对收益组合？——基于风险预算的资产配置策略.pdf"

# 本地文件如何读取
import os 
os.getcwd()


#st.markdown('''[周报](C:/Users/65475/gy2022/报告/专题报告/大类资产配置/【国元金工】如何用ETF构造绝对收益组合？——基于风险预算的资产配置策略.pdf)''')
#st.markdown('''[周报2](file:///C:/Users/65475/gy2022/报告/专题报告/大类资产配置/【国元金工】如何用ETF构造绝对收益组合？——基于风险预算的资产配置策略.pdf)''')

#### 找不到下面这个文件
st.markdown('''[周报](./【国元金工】如何用ETF构造绝对收益组合？——基于风险预算的资产配置策略.pdf)''',unsafe_allow_html=True)

#<a href="file:///path/to/local/file.pdf">link</a>

# 不太行
#st.markdown('''<a href="file:///C:/Users/65475/gy2022/报告/专题报告/大类资产配置/【国元金工】如何用ETF构造绝对收益组合？——基于风险预算的资产配置策略.pdf">link</a>''', unsafe_allow_html=True)

#st.markdown('''[周报word](file:///C:/Users/65475/gy2022/报告/专题报告/各种数据库\股指期货基差跟踪\股指期货基差跟踪周报（20230630）.docx)''')



with st.sidebar:
    choose = option_menu("国元金工研究平台", ["首页","基金筛选", "工具箱", "市场追踪", "定期组合更新"],
                         icons=['display','activity', 'box', 'graph-up-arrow', 'table'],
                         menu_icon="broadcast", default_index=0)



st.subheader("基于风险预算的绝对收益组合")
st.markdown('''本部分内容源自2023年4月对外发布的《如何用ETF构造绝对收益组合？——基于风险预算的绝对收益策略》：以构建低风险、低波动、高夏普的资产组合为目标，利用股债金三类资产较低的相关性，通过风险预算模型确定资产配置初始权重，再辅以股债、黄金的战术择时，输出最终的资产配置权重，以实现长期低风险、高夏普的投资组合。''')

# 读取所有数据
data = pd.read_csv(path,index_col=0)
data2 = pd.read_csv(path2,index_col=0)
#data = res.copy()

'''第一部分：组合业绩跟踪''' 
# 第一部分 业绩跟踪
# P1组合业绩跟踪  
# P2历史业绩走势图（左边是净值走势+右边是数据）  # 每年的业绩，是不变的数据，


# 第二部分 信号和仓位

re = data.iloc[:3,:4].reset_index()
re.columns = ['组合', '年初至今收益率(%)', '年化波动(%)', '年化夏普', '最大回撤(%)']

st.write("组合业绩跟踪")
st.markdown("### 组合业绩跟踪")

gb = GridOptionsBuilder.from_dataframe(re)
gb.configure_pagination(paginationAutoPageSize=False,paginationPageSize=10)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum",wrapText=True, st_aggrid=True,editable=False)
gridOptions = gb.build()
AgGrid(re, gridOptions=gridOptions, enable_enterprise_modules=False ,theme='alpine',fit_columns_on_grid_load=True)


st.divider()  # 加水平线




# 饼状图
av = data.loc['均值',['中证800', '中债综合总财富指数', '黄金AU9999']]
# 柱形图堆叠
con = data.iloc[:3,4:8]
          
# 饼状图option    
options1 = {
    "title": {"text": "大类资产配置仓位均值", "subtext": "年初至今(%)", "left": "center"},
    "tooltip": {"trigger": "item"},
    #"legend": {"orient": "vertical", "left": "left",},
    "series": [
        {
            #"name": "访问来源",
            "type": "pie",
            "radius": "50%",
            "data": [
                {"value": av[0], "name": av.index[0]},
                {"value": av[1], "name": av.index[1]},
                {"value": av[2], "name": av.index[2]},
                #{"value": av[3], "name": av.index[3]},
                #{"value": 300, "name": "视频广告"},
            ],
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)",
                }
            },
        }
    ],
}

# 柱形图option

options2 = {
    "title": {"text": "收益拆分", "subtext": "年初至今(%)", "left": "center"},
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
    "legend": {
        "data": [con.columns[0],con.columns[1],con.columns[2],con.columns[3]],
        "orient":"horizontal", "top":"15%",
        #"data": ['境内权益', '境外权益(纳斯达克100)', '债券', '黄金']
        },
    #"legend": {"orient": "vertical", "left": "left",},
    "grid": {"left": "3%", "right": "4%", "bottom": "5%","top":"30%","containLabel": True},
    "xAxis": {
        "type": "category",
        #"data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "data": [con.index[0],con.index[1],con.index[2]],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": con.columns[0],
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [con.iloc[0,0],con.iloc[0,1],con.iloc[0,2],con.iloc[0,3]],
        },
        {
            "name": con.columns[1],
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [con.iloc[1,0],con.iloc[1,1],con.iloc[1,2],con.iloc[1,3]],
        },
        {
            "name": con.columns[2],
            "type": "bar",
            "stack": "total",
            "label": {"show": True},
            "emphasis": {"focus": "series"},
            "data": [con.iloc[2,0],con.iloc[2,1],con.iloc[2,2],con.iloc[2,3]],
        },

    ],
}


with st.container():
    col1,col2 = st.columns(2)
    with col1:
        # 历史权重均值
        #st.area_chart(data.loc['均值',['中证800', '中债综合总财富指数', '黄金AU9999']])
        
        st_echarts( options=options1, height="400px",)
        
    with col2:
        # 收益贡献
        #st.bar_chart(data.iloc[:3,4:8])
        st_echarts(options=options2, height="400px")
        #data.iloc[:,4:8]
        
'''第二部分：模型观点 '''

# 模型最新观点
# 最新信号观点
# 
# 下载报告
page='this is a button'

st.download_button("详细内容请参考",page)
url="https://mp.weixin.qq.com/s/E4eLNnLaRVAsnTQgylP-bg"

st.markdown('<br>',unsafe_allow_html=True)  # 分行

st.markdown('''这是一个超链接，详细内容请参照 [《股指期货基差之分红点位预测》。]("https://mp.weixin.qq.com/s/E4eLNnLaRVAsnTQgylP-bg")''')
st.markdown('''[这是一个超链接？](https://mp.weixin.qq.com/s/E4eLNnLaRVAsnTQgylP-bg)''')


# 历史配置观点



st.write("最新信号")

# 最新信号

# 历史信号和仓位权重


 



# 资产配置概述   
# 基于风险预算的绝对收益组合
# 
# 组合收益跟踪
# 历史业绩
# 


       
'''
#st.markdown()
# 风险预算组合是利用股债金三大类资产构建的绝对收益组合，通过战略（风险预算模型）+战术（股债+黄金择时）月度输出配置观点，并在每月第一个交易日进行调仓，以获得长期低波动、高夏普的绝对收益。

st.write("")
st.subheader("本周各合约基差情况")


# 展示第一部分：
basis = pd.read_csv(path,index_col=0)
table = basis.iloc[:20,:13]
table = table.set_index(['指数','合约代码'])
table['收盘价'] = pd.to_numeric(table['收盘价']).apply(lambda x:'%.2f'%x if type(x)==float else x)
table.columns


# 
gb = GridOptionsBuilder.from_dataframe(table)
gb.configure_pagination(paginationAutoPageSize=False,paginationPageSize=10)
gb.configure_side_bar()
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum",wrapText=True, st_aggrid=True,editable=False)

gridOptions = gb.build()
AgGrid(table, gridOptions=gridOptions, enable_enterprise_modules=False ,theme='alpine',fit_columns_on_grid_load=True)
    


#basis['IH5日均值'] = basis['IH'].rolling(5).mean()

#fig1 = basis.iloc[:20,:13]

# 展示第一部分

st.dataframe(table)

# 展示第二部分
st.markdown("               ")
st.markdown("               ")

st.subheader("当季合约剔除分红影响后的年化基差率(%,5日平均)")
st.write("")
st.write("")


with st.container():
    col1,col2 = st.columns(2)
    with col1:
        #st.write("IH当季合约剔除分红后的年化基差率(%)")
        #st.line_chart(basis.loc[basis.index.str[:4]>="2022",'IH'].dropna())
        #st.line_chart(basis[['IH','IH5日均值']])
        st.line_chart(basis['IH'].dropna())
    with col2:
        #st.write("IF当季合约剔除分红后的年化基差率")
        st.line_chart(basis['IF'].dropna())


with st.container():
    col1,col2 = st.columns(2)
    with col1:
        #st.write("IC当季合约剔除分红后的年化基差率")
        st.line_chart(basis['IC'].dropna())
    with col2:
        #st.write("IM当季合约剔除分红后的年化基差率")
        st.line_chart(basis['IM'].dropna())
        
time = basis.iloc[-1].name

st.write("更新时间: ",time )


'''



