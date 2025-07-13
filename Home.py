import streamlit as st
import pandas as pd

st.set_page_config(page_title='Analytics Engineer test task', page_icon = './assets/logo.png', layout='centered')

def project_overview():
    st.markdown("This project is part of a mock analysis for an analytics engineer opportunity. Based on an initial dataset provided, the aim of the project is to propose a set of key metrics to drive business impact, design a data model to support these metrics, and compile a summary of findings with key insights uncovered by these metrics.")
    st.markdown("""
The business performance for the subscription service analysed is evaluated across four key areas:
- **Recurring revenue**: The monthly revenue and customer base for the subscription service.
- **Customer retention**: The ability of the business to retain existing customers.
- **Customer acquisition**: The ability of the business to attract new customers.
- **Subscription products**: The relative popularity and performance of the three subscription tiers.                                            
                """)

class mrr:
    def __init__(self, data_path):
        self.data_path = data_path
    def fetch_data(self):
        self.data = pd.read_csv(self.data_path)

class churn:
    def __init__(self, data_path):
        self.data_path = data_path
    def fetch_data(self):
        self.data = pd.read_csv(self.data_path)

class acquisition:
    def __init__(self, data_path):
        self.data_path = data_path
    def fetch_data(self):
        self.data = pd.read_csv(self.data_path)

class products:
    def __init__(self, data_path_subs, data_path_updown):
        self.data_path_subs = data_path_subs
        self.data_path_updown = data_path_updown
    def fetch_data(self):
        self.data_subs = pd.read_csv(self.data_path_subs)
        self.data_updown = pd.read_csv(self.data_path_updown)

st.title("Analytics Engineer Test Task")
#Part 1: Project overview
st.markdown('## Project Overview')
with st.container():
    project_overview()
    st.divider()


#Part 2: Recurring Revenue
st.markdown('## Recurring Revenue')
with st.container():
    mrr_object = mrr(data_path = './data/mrr.csv')
    mrr_object.fetch_data()
    st.dataframe(mrr_object.data)
    st.divider()

#Part 3: Customer Retention
st.markdown('## Customer Retention')
with st.container():
    churn_object = churn(data_path = './data/churn.csv')
    churn_object.fetch_data()
    st.dataframe(churn_object.data)
    st.divider()

#Part 4: Customer Acquisition
st.markdown('## Customer Acquisition')
with st.container():
    acq_object = acquisition(data_path = './data/acquisitions.csv')
    acq_object.fetch_data()
    st.dataframe(acq_object.data)
    st.divider()

#Part 5: Subscription products
st.markdown('## Subscription products')
with st.container():
    products_object = products(data_path_subs='./data/monthly_subs.csv', data_path_updown='./data/upgrades_downgrades.csv')
    products_object.fetch_data()
    st.dataframe(products_object.data_subs)
    st.dataframe(products_object.data_updown)
    st.divider()