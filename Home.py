import streamlit as st
import plotly.express as px
import pandas as pd

st.title("My Data Science App")

# Load data

df = pd.read_csv('data/pell_summary.csv')

with st.expander("Show Data"):
    st.write(df)

st.divider()

with st.form("top_institutions"):
    st.write("Institutions Receiving the Most Pell Grant Money")
    top_n = st.slider('Select number of institutions', 1, 20, 5)
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        top_institutions = df.nlargest(top_n, 'PellM$')[['Institution','Control', 'PellB$']]
        st.write(top_institutions)

st.divider()

with st.form("institution_type"):
    st.write("Top Institutions by Type")
    control = st.selectbox('Select institution type', df['Control'].unique())
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    top_institutions = df[df['Control'] == control].nlargest(5, 'PellM$')[['Institution','Control', 'PellM$','GradRate']]
    st.write(top_institutions)

st.divider()


df['GradRate'] = df['GradRate']/100
with st.form("plotly_plot"):
    st.write("Scatter Plot")
    plot_n = st.slider('Select number of institutions to plot', 1, 1000, 100)
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        df_inst = df.nlargest(plot_n, 'PellM$')[['Institution', 'Control', 'PellB$', 'GradRate']]
        
        # Create a scatter plot with Plotly
        fig = px.scatter(df_inst, x='PellB$', y='GradRate', color='Control', hover_data=['Institution'])

        # Add a horizontal red line at y=0.5
        fig.add_hline(y=0.25, line_width=3, line_dash="dash", line_color="red")
        
        # Show the plot in Streamlit
        st.plotly_chart(fig)