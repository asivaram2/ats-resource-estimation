import streamlit as st
import requests
import pandas as pd
import datetime
from pyspark.sql import SparkSession

# ---- Workfront API Config ----
API_KEY = "4kocbwab1pws72grj41mhzicung7najj"
PORTFOLIO_IDS = [
    "62c75e2800b8e647336989ab99280223",  # ATS Acquisitions 
    "62c75ed300b9233654df648eac740d68",  # ATS Cloud Excellence
    "62c75ede00b9281b0e451c5038b36be2",  # ATS Cloud Operations
    "62c75f2000b9468b026996cab2167547",  # ATS Customer Experience Services
    "62c75f2f00b94ddef8f420a93626d39f",  # ATS Data & Analytics 
    "62c75f3c00b956ec671b80cb78a3ac1b",  # ATS Digital Experience Services
    "62c75f4f00b95c19df68372ee87fd6a2",  # ATS Enterprise Marketing
    "62c75f5c00b9675d20f08a5677a20412",  # ATS Financial & Revenue Management
    "62e849e0001dcc7ab6d914774a13b0cf",  # ATS Nestware
    "62c75f6d00b96a50b7d493c9cb5ae3a8",  # ATS Office of the CIO
    "62c75fa900b9861c252cb07de7d099fe",  # ATS Adobe Service Management
    "62c75f9800b97a8f221ce084c8d19d84",  # ATS Sales Platform
    "62c75f5c00b9675d20f08a5677a20412",  # ATS Shared Services Platform
    "67af7bb8000271dabb7cd574d194927c"   # ATS Transformation Management Office
]
BASE_URL = "https://adoberm.my.workfront.com/attask/api/v17.0/PROJ/search"

# ---- Load Projects ----
@st.cache_data
def load_projects():
    all_projects = []
    for portfolio_id in PORTFOLIO_IDS:
        params = {
            "fields": "name,status",
            "portfolioID": portfolio_id,
            "apiKey": API_KEY,
            "$$LIMIT": "100"
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            all_projects.extend(response.json()["data"])
    return all_projects

# ---- UI Starts ----
st.title("Resource Estimation Form")

projects = load_projects()
project_options = [f"{proj['name']} ({proj['ID']})" for proj in projects]
selected_project = st.selectbox("🔍 Search & Select Project", project_options)

# ---- Additional Fields ----
job_function = st.selectbox("Job Function", ["Java Developer", "Business Architect", "System Architect"])
planned_hours = st.number_input("Planned Hours", min_value=0)
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# ---- Submit & Save to Databricks ----
if st.button("Submit"):
    # Build DataFrame
    submission = {
        "submitted_at": datetime.datetime.now(),
        "project": selected_project,
        "job_function": job_function,
        "planned_hours": planned_hours,
        "start_date": start_date,
        "end_date": end_date
    }

    df = pd.DataFrame([submission])
    spark = SparkSession.builder.getOrCreate()
    spark_df = spark.createDataFrame(df)

    # Define full table name
    catalog = "dpaas_uccatalog_prd"
    schema = "ocio"
    table_name = "resource_estimates"
    full_table_name = f"{catalog}.{schema}.{table_name}"

    # Create table if it doesn't exist
    spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {full_table_name} (
        submitted_at TIMESTAMP,
        project STRING,
        job_function STRING,
        planned_hours DOUBLE,
        start_date DATE,
        end_date DATE
    )
    USING DELTA
    """)

    # Append data
    spark_df.write.format("delta").mode("append").saveAsTable(full_table_name)

    st.success("✅ Submitted and stored in Databricks Delta table!")
