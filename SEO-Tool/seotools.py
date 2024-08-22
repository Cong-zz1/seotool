import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# 设置页面标题
st.title('SEO Analysis Dashboard')

# 初始化数据存储
if 'seo_data' not in st.session_state:
    st.session_state['seo_data'] = pd.DataFrame(columns=['Date', 'Keyword', 'Page URL', 'Keyword Ranking', 'Page Ranking', 'SEO Action'])

# 输入区域
st.header('Input SEO Data')

keyword = st.text_input('Keyword')
page_url = st.text_input('Page URL')
keyword_ranking = st.number_input('Keyword Ranking', min_value=1, max_value=100, value=1)
page_ranking = st.number_input('Page Ranking', min_value=1, max_value=100, value=1)
seo_action = st.text_area('SEO Action Taken')
today = date.today()

if st.button('Add Entry'):
    # 将数据添加到DataFrame中
    new_entry = pd.DataFrame({
        'Date': [today],
        'Keyword': [keyword],
        'Page URL': [page_url],
        'Keyword Ranking': [keyword_ranking],
        'Page Ranking': [page_ranking],
        'SEO Action': [seo_action]
    })
    
    st.session_state['seo_data'] = pd.concat([st.session_state['seo_data'], new_entry], ignore_index=True)
    st.success('Data added successfully!')

# 展示和分析数据
st.header('SEO Data Overview')
st.dataframe(st.session_state['seo_data'])

# 生成图表
st.header('Keyword Ranking Over Time')
if not st.session_state['seo_data'].empty:
    fig, ax = plt.subplots()
    for key, grp in st.session_state['seo_data'].groupby(['Keyword']):
        ax.plot(grp['Date'], grp['Keyword Ranking'], label=key)
    ax.set_xlabel('Date')
    ax.set_ylabel('Keyword Ranking')
    ax.legend(loc='best')
    st.pyplot(fig)

# 导出数据和报告
if st.button('Generate Report'):
    # 导出为Excel文件
    report_file = f'SEO_Report_{today}.xlsx'
    st.session_state['seo_data'].to_excel(report_file, index=False)
    st.write(f'Report generated: {report_file}')
    st.download_button(
        label='Download Report',
        data=open(report_file, 'rb').read(),
        file_name=report_file,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
