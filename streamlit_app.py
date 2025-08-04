import streamlit as st
import requests

# ---- Workfront API Config ----
API_KEY = "4kocbwab1pws72grj41mhzicung7najj"
PORTFOLIO_IDS = [
  "62c75e2800b8e647336989ab99280223", //ATS Acquisitions 
                            "62c75ed300b9233654df648eac740d68", //ATS Cloud Excellence
                            "62c75ede00b9281b0e451c5038b36be2", //ATS Cloud Operations
                            "62c75f2000b9468b026996cab2167547", //ATS Customer Experience Services
                            "62c75f2f00b94ddef8f420a93626d39f", //ATS Data & Analytics 
                            /*"62dedf37001f73ec09d059c9df63aa61", //ATS Recycle Bin*/
                            "62c75f3c00b956ec671b80cb78a3ac1b", //ATS Digital Experience Services
                            "62c75f4f00b95c19df68372ee87fd6a2", //ATS Emterprise Marketing
                            "62c75f5c00b9675d20f08a5677a20412", //ATS Financial & Revenue Management
                            "62e849e0001dcc7ab6d914774a13b0cf", //ATS Nestware
                            "62c75f6d00b96a50b7d493c9cb5ae3a8", //ATS Office of the CIO
                            "62c75fa900b9861c252cb07de7d099fe", //ATS Adobe Service Management
                            "62c75f9800b97a8f221ce084c8d19d84", //ATS Sales Platform
                            "62c75f5c00b9675d20f08a5677a20412", //ATS Shared Services Platform
                            "67af7bb8000271dabb7cd574d194927c"  //ATS Transformation Management Office
                            
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

# Load projects and create search-friendly list
projects = load_projects()
project_options = [f"{proj['name']} ({proj['ID']})" for proj in projects]
selected_project = st.selectbox("🔍 Search & Select Project", project_options)

# ---- Additional Fields ----
job_function = st.selectbox("Job Function", ["Java Developer", "Business Architect", "System Architect"])
planned_hours = st.number_input("Planned Hours", min_value=0)
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# ---- Submit ----
if st.button("Submit"):
    st.success(f"""
     Submitted:
    • **Project:** {selected_project}
    • **Job Function:** {job_function}
    • **Planned Hours:** {planned_hours}
    """)
