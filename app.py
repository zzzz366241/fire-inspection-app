import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="通用数据分析看板", layout="wide")
st.title("📊 通用 Excel 数据分析看板")
st.write("上传任意 Excel 文件，自由选择列，自动生成图表。")

上传文件 = st.file_uploader("上传 Excel 文件", type=["xlsx", "xls"])

if 上传文件 is not None:
    df = pd.read_excel(上传文件)

    st.subheader("📋 数据预览")
    st.dataframe(df)

    所有列 = df.columns.tolist()
    分类列 = st.selectbox("选择用作分类的列（横轴）", 所有列)

    模式 = st.radio("分析模式", ["统计分类出现次数（计数）", "按数值列求和/平均值"])

    if 模式 == "统计分类出现次数（计数）":
        统计结果 = df[分类列].value_counts()
        图表标题 = f"{分类列} 出现次数统计"
    else:
        数值列 = st.selectbox("选择用作数值的列（纵轴）", 所有列)
        聚合方式 = st.selectbox("聚合方式", ["求和", "平均值"])
        if 聚合方式 == "求和":
            统计结果 = df.groupby(分类列)[数值列].sum()
        else:
            统计结果 = df.groupby(分类列)[数值列].mean()
        图表标题 = f"各{分类列} 的{数值列}（{聚合方式}）"

    st.subheader("📊 统计结果")
    st.dataframe(统计结果)

    图表类型 = st.selectbox("选择图表类型", ["柱状图", "横向柱状图", "饼图", "折线图"])

    st.subheader("📈 图表")
    fig, ax = plt.subplots()

    if 图表类型 == "柱状图":
        统计结果.plot(kind='bar', color='#3498db', edgecolor='black', ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    elif 图表类型 == "横向柱状图":
        统计结果.plot(kind='barh', color='#2ecc71', edgecolor='black', ax=ax)
    elif 图表类型 == "饼图":
        统计结果.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
    elif 图表类型 == "折线图":
        统计结果.plot(kind='line', marker='o', color='#e74c3c', ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    ax.set_title(图表标题, fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)

else:
    st.info("👆 请上传一个 Excel 文件，支持 .xlsx 和 .xls 格式。")
    st.write("你的文件不需要特定格式，有任何列都行，上传后自己选就好。")