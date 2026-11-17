import streamlit as st
import pandas as pd
import plotly.express as px

df=pd.read_csv('Advertising_F.csv')
st.title("Advertising Effectiveness Andrea")
st.sidebar.header("Filters")
x_var=st.sidebar.selectbox("X axis",["TV","radio","newspaper"])
y_var=st.sidebar.selectbox("Y Axis",["sales"])

#show scatterplot
fig=px.scatter(df, x=x_var, y=y_var,labels={'TV': 'TV Ad Spend', 'radio': 'Radio Ad Spend'})
st.plotly_chart(fig)
#show bar chart
sales_per_city = df.groupby('City')['sales'].sum().reset_index()
fig= px.bar(sales_per_city,
                       x='City',
                       y='sales',
                       title=f'Total Sales per City',
                       labels={ 'sales':'Total- Sales'})

st.plotly_chart(fig)
#Dataframe
st.write("### This is the data")
st.dataframe(df)

#Show Map
st.title("I'm the map!!!")
fig=px.scatter_map(df,lat='latitude',lon='longitude',size='newspaper',
                      hover_name='City',color='sales',
                      color_continuous_scale=px.colors.sequential.Viridis)
fig.update_layout(map_style='carto-positron')
st.plotly_chart(fig)
