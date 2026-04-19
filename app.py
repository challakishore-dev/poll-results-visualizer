
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Poll Results Visualizer", layout="wide")
@st.cache_data
def load():
    return pd.read_csv("data/poll_data.csv")
df=load()

st.title("📊 Poll Results Visualizer")
st.caption("Professional survey analytics dashboard")

with st.sidebar:
    st.header("Filters")
    regions=st.multiselect("Region", sorted(df.Region.unique()), default=sorted(df.Region.unique()))
    ages=st.multiselect("Age Group", sorted(df.Age_Group.unique()), default=sorted(df.Age_Group.unique()))
f=df[df.Region.isin(regions) & df.Age_Group.isin(ages)]

c1,c2,c3,c4=st.columns(4)
c1.metric("Responses", len(f))
c2.metric("Regions", f.Region.nunique())
c3.metric("Avg Satisfaction", round(f.Satisfaction.mean(),2))
leader=f.Option_Selected.value_counts().idxmax()
c4.metric("Leading Option", leader)

tab1,tab2,tab3=st.tabs(["Overview","Demographics","Raw Data"])

with tab1:
    col1,col2=st.columns(2)
    votes=f.Option_Selected.value_counts().reset_index()
    votes.columns=["Option","Votes"]
    fig=px.bar(votes,x="Option",y="Votes",text="Votes",title="Vote Count",template="plotly_white")
    col1.plotly_chart(fig,use_container_width=True)
    fig2=px.pie(votes,names="Option",values="Votes",hole=.45,title="Vote Share")
    col2.plotly_chart(fig2,use_container_width=True)

    trend=f.groupby("Date").size().reset_index(name="Responses")
    fig3=px.line(trend,x="Date",y="Responses",markers=True,title="Response Trend")
    st.plotly_chart(fig3,use_container_width=True)

with tab2:
    cross=f.groupby(["Region","Option_Selected"]).size().reset_index(name="Count")
    fig4=px.bar(cross,x="Region",y="Count",color="Option_Selected",barmode="group",title="Region Comparison")
    st.plotly_chart(fig4,use_container_width=True)

    fig5=px.box(f,x="Option_Selected",y="Satisfaction",title="Satisfaction by Option")
    st.plotly_chart(fig5,use_container_width=True)

with tab3:
    st.dataframe(f,use_container_width=True)
