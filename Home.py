import streamlit as st



def project_overview():
    st.markdown("This project is part of a mock analysis for an analytics engineer opportunity. Based on an initial dataset provided, the aim of the project is to propose a set of key metrics to drive business impact, design a data model to support these metrics, and compile a summary of findings with key insights uncovered by these metrics.")
    st.markdown("""
The business performance for the subscription service analysed is evaluated across four key areas:
- **Recurring revenue**: The monthly revenue and customer base for the subscription service.
- **Customer retention**: The ability of the business to retain existing customers.
- **Customer acquisition**: The ability of the business to attract new customers.
- **Subscription products**: The relative popularity and performance of the three subscription tiers.                                            
                """)







st.title("Analytics Engineer Test Task")
#Part 1: Project overview
st.markdown('## Project Overview')
with st.container():
    project_overview()
    st.divider()


#Part 2: Recurring Revenue
st.markdown('## Recurring Revenue')
with st.container():
    st.divider()

#Part 3: Customer Retention
st.markdown('## Customer Retention')
with st.container():
    st.divider()

#Part 4: Customer Acquisition
st.markdown('## Customer Acquisition')
with st.container():
    st.divider()

#Part 5: Subscription products
st.markdown('## Subscription products')
with st.container():
    st.divider()