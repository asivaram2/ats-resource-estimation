import streamlit as st
import requests

# Call API on load or button click
st.title("Select Workfront Project")

if st.button("Load Projects"):
    url = "https://adoberm.my.workfront.com/attask/api/v17.0/PROJ/search"
    params = {
        "fields": "name,status",
        "portfolioID": "62c75e2800b8e647336989ab99280223",
        "apiKey": "4kocbwab1pws72grj41mhzicung7najj",
        "$$LIMIT": "20"
    }

    r = requests.get(url, params=params)
    projects = r.json()['data']

    project_names = [proj["name"] for proj in projects]
    selected = st.selectbox("Choose a project", project_names)
    st.write(f"You selected: {selected}")
