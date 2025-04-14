import streamlit as st
import pandas as pd

# Load Data
df = pd.read_excel("Afids_Cleaned_Dashboard_Ready.xlsx")

# Clean Column Names
df.columns = df.columns.str.strip()

# Rename Columns for Simplicity
df.rename(columns={
    'RECORD PROVINCE': 'Province',
    'Area': 'Area',
    'RECORD GENDER': 'Gender',
    'Below age ranges': 'Age Range',
    'SEC': 'SEC',
    'which one do you consume more than the others?': 'Consumed Most',
}, inplace=True)

# Identify Typology, Frequency & Satisfaction columns dynamically
typology_cols = [col for col in df.columns if 'Typology_' in col]
frequency_cols = [col for col in df.columns if 'Frequeny of drinking' in col]
satisfaction_cols = [col for col in df.columns if 'Satisfaction_' in col]

# Streamlit Config
st.set_page_config(page_title="Afdis Consumer Insights Dashboard", layout="wide")

st.title("Afdis Consumer Insights Dashboard")
st.markdown("Use filters on the left to explore different consumer insights across Zimbabwe.")

st.sidebar.header("Filter Data")

province = st.sidebar.multiselect("Select Province:", df['Province'].unique(), default=df['Province'].unique())
area = st.sidebar.multiselect("Select Area:", df['Area'].unique(), default=df['Area'].unique())
gender = st.sidebar.multiselect("Select Gender:", df['Gender'].unique(), default=df['Gender'].unique())
age = st.sidebar.multiselect("Select Age Range:", df['Age Range'].unique(), default=df['Age Range'].unique())
sec = st.sidebar.multiselect("Select SEC:", df['SEC'].unique(), default=df['SEC'].unique())

filtered_df = df[
    (df['Province'].isin(province)) &
    (df['Area'].isin(area)) &
    (df['Gender'].isin(gender)) &
    (df['Age Range'].isin(age)) &
    (df['SEC'].isin(sec))
]

# Download Button
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)

st.sidebar.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='afdis_filtered.csv',
    mime='text/csv',
)

# Dashboard Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Consumption Patterns", "Satisfaction Levels", "Frequency of Drinking", "Consumer Typology"])

with tab1:
    st.subheader("Top Consumed Category")
    if not filtered_df.empty:
        st.metric("Most Consumed", filtered_df['Consumed Most'].mode()[0])
        st.bar_chart(filtered_df['Consumed Most'].value_counts())

with tab2:
    st.subheader("Satisfaction Levels (All Brands)")
    for col in satisfaction_cols:
        st.write(col.replace("Satisfaction_", ""))
        chart_data = filtered_df[col][filtered_df[col] != 'Not Stated']
        if not chart_data.empty:
            st.bar_chart(chart_data.value_counts())

with tab3:
    st.subheader("Frequency of Drinking (All Brands)")
    for col in frequency_cols:
        brand = col.replace("Frequeny of drinking ", "")
        st.write(brand)
        chart_data = filtered_df[col][~filtered_df[col].isin(['Not Stated', 0, '0', '-1', -1])]
        if not chart_data.empty:
            st.bar_chart(chart_data.value_counts())

with tab4:
    st.subheader("Consumer Typology (All Brands)")
    for col in typology_cols:
        brand = col.replace("Typology_", "")
        st.write(brand)
        chart_data = filtered_df[col][filtered_df[col] != 'Not Stated']
        if not chart_data.empty:
            st.bar_chart(chart_data.value_counts())

st.markdown("---")

# Show Filtered Data Last (Separate Section)
st.markdown("### Filtered Data Table (Based on Your Selections)")
st.dataframe(filtered_df)

st.markdown("---")
st.caption("Developed by Smart | Powered by Streamlit")
