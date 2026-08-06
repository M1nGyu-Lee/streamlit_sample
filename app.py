import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

df = pd.read_csv("C:\\Users\\SBA\\python_code\\config\\HR Data.csv", encoding="cp949")




st.title("매출 대시보드")

df