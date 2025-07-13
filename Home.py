import streamlit as st
import pandas as pd
import altair as alt

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

def filter_data_categories(dataset, description, column, key):
    """A util function to apply a multiselect filter to narrow down a pandas dataset based on a categorical column"""
    options = dataset[column].unique()
    choices = st.multiselect(label=description, options=options, key=key)
    if len(choices)>0:
        dataset = dataset[dataset[column].isin(choices)]
    return dataset

def metric_info(expander_label, text):
    with st.expander(expander_label):
        st.info(text)


class mrr:
    def __init__(self, data_path):
        self.data_path = data_path
    def fetch_data(self):
        self.data = pd.read_csv(self.data_path)
    def filter_data(self):
        with st.container(border=True):
            self.data = filter_data_categories(self.data, description='Filter data by market', column='billingCountry', key='mrr_country')
            self.data = filter_data_categories(self.data, description='Filter data by subscription product', column='product', key='mrr_product')
    def plot_mrr(self):
        chart = alt.Chart(self.data).mark_area(point=True).encode(
            x=alt.X('yearmonth(metric_month):T', title=''),
            y=alt.Y('sum(mrr):Q', title='Monthly recurring revenue'),
            tooltip = [alt.Tooltip('yearmonth(metric_month):T',title='Month',timeUnit='yearmonth'),alt.Tooltip('sum(mrr):Q',title='MRR',format='.1f')]
        )
        with st.container():
            st.markdown('### Monthly recurring revenue')
            st.markdown('') #Spacer
            st.altair_chart(chart, use_container_width=True)
    def plot_customers(self):
        chart = alt.Chart(self.data).mark_area(point=True).encode(
            x=alt.X('yearmonth(metric_month):T', title=''),
            y=alt.Y('sum(active_subscribers):Q', title='Monthly subscribers'),
            tooltip = [alt.Tooltip('yearmonth(metric_month):T',title='Month',timeUnit='yearmonth'),alt.Tooltip('sum(active_subscribers):Q',title='MRR',format='.0f')]
        )
        with st.container():
            st.markdown('### Monthly subscribers')
            st.markdown('') #Spacer
            st.altair_chart(chart, use_container_width=True)

class churn:
    def __init__(self, data_path):
        self.data_path = data_path
    def fetch_data(self):
        self.data = pd.read_csv(self.data_path)
    def filter_data(self):
        with st.container(border=True):
            self.data = filter_data_categories(self.data, description='Filter data by market', column='billingCountry', key='churn_country')
            self.data = filter_data_categories(self.data, description='Filter data by subscription product', column='product', key='churn_product')


class acquisition:
    def __init__(self, data_path):
        self.data_path = data_path
    def fetch_data(self):
        self.data = pd.read_csv(self.data_path)
    def filter_data(self):
        with st.container(border=True):
            self.data = filter_data_categories(self.data, description='Filter data by market', column='billingCountry', key='acq_country')
            self.data = filter_data_categories(self.data, description='Filter data by subscription product', column='product', key='acq_product')


class products:
    def __init__(self, data_path_subs, data_path_updown):
        self.data_path_subs = data_path_subs
        self.data_path_updown = data_path_updown
    def fetch_data(self):
        self.data_subs = pd.read_csv(self.data_path_subs)
        self.data_updown = pd.read_csv(self.data_path_updown)
    def filter_data(self):
        with st.container(border=True):
            options = self.data_subs['billingCountry'].unique()
            choices = st.multiselect(label="Filter data by market", options=options, key='products_country')
            if len(choices)>0:
                self.data_subs = self.data_subs[self.data_subs['billingCountry'].isin(choices)]
                self.data_updown = self.data_updown[self.data_updown['billingCountry'].isin(choices)]

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
    mrr_object.filter_data()
    mrr_object.plot_mrr()
    mrr_object.plot_customers()
    metric_info(expander_label='**Learn more about MRR**', text="MRR is an indicator that measures the predictable revenue that the subscription service generates, periodised on a monthly basis. It is calculated by adding the monthly-equivalent revenue for all subscriptions active each month. Monthly subscriptions contribute their entire amount to the month they are paid, while yearly subscriptions have their amount split evenly across 12 months. The monthly subscriber metric represents the number of customers with an active subscription on a given month, who contribute to this revenue.")
    st.divider()

#Part 3: Customer Retention
st.markdown('## Customer Retention')
with st.container():
    churn_object = churn(data_path = './data/churn.csv')
    churn_object.fetch_data()
    churn_object.filter_data()
    st.dataframe(churn_object.data)
    st.divider()

#Part 4: Customer Acquisition
st.markdown('## Customer Acquisition')
with st.container():
    acq_object = acquisition(data_path = './data/acquisitions.csv')
    acq_object.fetch_data()
    acq_object.filter_data()
    st.dataframe(acq_object.data)
    st.divider()

#Part 5: Subscription products
st.markdown('## Subscription products')
with st.container():
    products_object = products(data_path_subs='./data/monthly_subs.csv', data_path_updown='./data/upgrades_downgrades.csv')
    products_object.fetch_data()
    products_object.filter_data()
    st.dataframe(products_object.data_subs)
    st.dataframe(products_object.data_updown)
    st.divider()