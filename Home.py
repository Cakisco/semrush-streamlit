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
        chart = alt.Chart(self.data).mark_area(point=alt.OverlayMarkDef(filled=True, fill='#421983', stroke='#421983'), color='#421983').encode(
            x=alt.X('yearmonth(metric_month):T', title=''),
            y=alt.Y('sum(mrr):Q', title='Monthly recurring revenue'),
            tooltip = [alt.Tooltip('yearmonth(metric_month):T',title='Month',timeUnit='yearmonth'),alt.Tooltip('sum(mrr):Q',title='MRR',format='.1f')]
        )
        with st.container():
            st.markdown('### Monthly recurring revenue')
            st.markdown('') #Spacer
            st.altair_chart(chart, use_container_width=True)
    def plot_customers(self):
        chart = alt.Chart(self.data).mark_area(point=alt.OverlayMarkDef(filled=True, fill='#421983', stroke='#421983'), color='#421983').encode(
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
            self.churn_volume = st.toggle(label='See volume churn rate', help='Toggle this option to visualise volume (customer) churn rate instead of value (revenue) churn rate')
    def transform_data(self):
        data_churn = self.data.groupby(['churn_month'])[['starting_revenue','starting_customers','retained_revenue','retained_customers']].sum().reset_index()
        data_churn['value_retention']=data_churn['retained_revenue']/data_churn['starting_revenue']
        data_churn['volume_retention']=data_churn['retained_customers']/data_churn['starting_customers']
        data_churn['value_churn'] = 1 - data_churn['value_retention']
        data_churn['volume_churn'] = 1 - data_churn['volume_retention']
        data_churn['churn_month']=pd.to_datetime(data_churn['churn_month'])
        self.data_chart = data_churn
    def plot_churn(self):
        if self.churn_volume:
            metric='volume_churn:Q'
        else:
            metric='value_churn:Q'
        chart = alt.Chart(self.data_chart).mark_line(point=alt.OverlayMarkDef(filled=True, fill='#421983', stroke='#421983'), color='#421983').encode(
            x=alt.X('yearmonth(churn_month):T', title=''),
            y=alt.Y(metric, title='Churn rate', axis=alt.Axis(format='.0%')),
            tooltip = [alt.Tooltip('yearmonth(churn_month):T',title='Month',timeUnit='yearmonth'),alt.Tooltip(metric,title='Churn rate',format='.1%')]
        )
        with st.container():
            st.markdown('### Churn rate')
            st.markdown('') #Spacer
            st.altair_chart(chart, use_container_width=True)

class acquisition:
    def __init__(self, data_path):
        self.data_path = data_path
    def fetch_data(self):
        self.data = pd.read_csv(self.data_path)
    def filter_data(self):
        with st.container(border=True):
            self.data = filter_data_categories(self.data, description='Filter data by market', column='billingCountry', key='acq_country')
            self.data = filter_data_categories(self.data, description='Filter data by subscription product', column='product', key='acq_product')
    def transform_data(self):
        data_chart = self.data
        data_chart.drop('customer_base', axis=1, inplace=True)
        data_chart.rename(mapper={'customers_acquired':'Acquisitions','cancelled_customers':'Cancellations'}, axis=1, inplace=True)
        data_chart_melted = pd.melt(data_chart, id_vars=['metric_month','product','billingCountry'], value_vars=['Acquisitions','Cancellations'], var_name='metric', value_name='count')
        self.data_chart = data_chart_melted
    def plot_acquisition(self):
        colourscale=alt.Scale(domain=['Acquisitions','Cancellations'],range=['green','red'])
        chart = alt.Chart(self.data_chart).mark_line(point=True).encode(
            x=alt.X('yearmonth(metric_month):T', title=''),
            y=alt.Y('sum(count):Q', title='No. of users'),
            color=alt.Color('metric:N',title='Metric',scale=colourscale),
            tooltip = [alt.Tooltip('yearmonth(metric_month):T',title='Month',timeUnit='yearmonth'),alt.Tooltip('sum(count):Q',title='No. of customers',format='.0f'),alt.Tooltip('metric:N',title='Metric')]
        )
        with st.container():
            st.markdown('### Monthly acquisitions and cancellations')
            st.markdown('') #Spacer
            st.altair_chart(chart, use_container_width=True)



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
    def plot_subscribers(self):
        data_chart = self.data_subs.groupby(['metric_month','product'])[['no_customers','mrr']].sum().reset_index()
        data_chart['total_customers'] = data_chart.groupby('metric_month')['no_customers'].transform('sum')
        data_chart['proportion'] = data_chart['no_customers'] / data_chart['total_customers']
        chart = alt.Chart(data_chart).mark_area().encode(
            x=alt.X('yearmonth(metric_month):T', title=''),
            y=alt.Y('sum(proportion):Q', title='% of customers', axis=alt.Axis(format='.0%'), scale=alt.Scale(domain=[0, 1])),
            color=alt.Color('product:N',title='Product',scale=alt.Scale(scheme='category10')),
            tooltip = [alt.Tooltip('yearmonth(metric_month):T',title='Month',timeUnit='yearmonth'),alt.Tooltip('sum(proportion):Q',title='% of customers',format='.1%'),alt.Tooltip('product:N',title='Product')]
        )
        data_arppu=self.data_subs.groupby(['metric_month'])[['no_customers','mrr']].sum().reset_index()
        data_arppu['arppu']=data_arppu['mrr']/data_arppu['no_customers']
        arppu_chart = alt.Chart(data_arppu).mark_line(color='red').encode(
            x=alt.X('yearmonth(metric_month):T', title=''),
            y=alt.Y('arppu:Q', title='ARPPU', scale=alt.Scale(domain=[100, 200])),
            tooltip = [alt.Tooltip('yearmonth(metric_month):T',title='Month',timeUnit='yearmonth'),alt.Tooltip('arppu:Q',title='ARPPU',format='.1%')]
        )
        with st.container():
            st.markdown('### Monthly recurring revenue')
            st.markdown('') #Spacer
            st.altair_chart(chart, use_container_width=True)
            st.altair_chart(arppu_chart, use_container_width=True)


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
    churn_object.transform_data()
    churn_object.plot_churn()
    metric_info(expander_label='**Learn more about Churn rate**', text="Customer retention is evaluated by measuring churn rate, both in terms of revenue (value) and number of customers (volume). Churn rates are an indication of how much the existing subscriber base shrinks every month, primarily due to cancellations. It is calculated as a ratio between the customer base (revenue/subscribers) that is lost on a given month and the size of the customer base at the beginning of the month. Value churn also considers the effect of upselling and downselling to existing subscribers.")
    st.divider()

#Part 4: Customer Acquisition
st.markdown('## Customer Acquisition')
with st.container():
    acq_object = acquisition(data_path = './data/acquisitions.csv')
    acq_object.fetch_data()
    acq_object.filter_data()
    acq_object.transform_data()
    acq_object.plot_acquisition()
    metric_info(expander_label='**Learn more about customer acquisition**', text="Customer acquisition is evaluated by measuring the number of newly subscribed customers each month. A customer is considered to be newly subscribed if they have an active subscription in a given month, but they did not in the previous months. This includes customers that were subscribed, cancelled their subscription and later re-subscribed. The number of acquired customers is compared with the number of customer cancellations to better evaluate growth.")
    st.divider()

#Part 5: Subscription products
st.markdown('## Subscription products')
with st.container():
    products_object = products(data_path_subs='./data/monthly_subs.csv', data_path_updown='./data/upgrades_downgrades.csv')
    products_object.fetch_data()
    products_object.filter_data()
    products_object.plot_subscribers()
    st.dataframe(products_object.data_subs)
    st.dataframe(products_object.data_updown)
    st.divider()