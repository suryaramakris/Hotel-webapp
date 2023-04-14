import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import time

#page widening and hide the watermarks
st.set_page_config(layout="wide")
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
background-image: linear-gradient(rgba(0, 0, 0, 0.727),rgba(0, 0, 0, 0.5)) ,url("https://t4.ftcdn.net/jpg/02/92/20/37/360_F_292203735_CSsyqyS6A4Z9Czd4Msf7qZEhoxjpzZl1.jpg");
background-size: cover;
background-position: center;
}

[data-testid="stToolbar"]{
right: 1.5rem;
}

[data-testid="stHeader"]{
background-color: rgba(0,0,0,0);
}

.css-1q1n0ol.egzxvld0{
visibility:hidden;
}
</style>""",unsafe_allow_html=True)

#app title
st.markdown("<h1 style='text-align: center; font-family:Lucida; '>Choose the Best Restaurants You Wish</h2>",unsafe_allow_html=True)
st.write("#")

#locality selection and data loading
col1,col2 = st.columns(2)
data = col1.selectbox("Please choose your locality :",options=("HSR Layout",'Jayanagar','MG Road',"Residency Road"))
df = pd.read_csv(data+".csv")
dfraw = pd.read_csv(data+".csv")
#unique cuisine based on the locality
food = []
i=0
while i<df.shape[0]:
    for x in df['dish'][i].split(','):
        food.append(x.strip().lower())
    i+=1
food = np.array(food)
foodoptions = np.unique(food)

#cuisine selected 
cuisine = col2.multiselect("Cuisine :",options=(foodoptions))

#just user design
load1 = st.text("Loading "+data+" data...")
time.sleep(0.3)
load1.text("Loading "+data+" data...Done!!")

#preprocess = st.text("Dropping unwanted column from the data!!")
df.drop("Unnamed: 0",axis=1,inplace=True)

#preprocess.text("Coverting the ratings column to int dtype!!")
def intcon(x):
    try:
        return float(x)
    except:
        return 0
df["ratings"] = df['ratings'].apply(lambda x: intcon(x))

#preprocess.text("Removing text from cost column and converting to int dtype!!")
def costcon(x):
    return int(x[1:4])
df['cost'] = df['cost'].apply(lambda x: costcon(x))

#preprocess.text("Removing 'min' from delivery minutes column!!")
def deliverycon(x):
    return int(x[:2])
df['deliveryin_min'] = df['deliveryin_min'].apply(lambda x: deliverycon(x))

#preprocess.text("Retaining number of orders only from order column!!")
def ordercon(x):
    try:
        a = x.find("+")
        return float(x[:a])
    except:
        return 0
df['order'] = df['order'].apply(lambda x: ordercon(x))

#to choose rows with cuisine selected by user
if len(cuisine) !=0:

    j=0
    dfindex = []

    while j<df.shape[0]:
        for x in cuisine:
            if x.lower() in df['dish'][j].lower():
                dfindex.append(j)
                break
        j+=1
    df = df.iloc[dfindex]
st.text(str(df.shape[0])+" restaurants matches your requirment")

#sidebar for feature selection to display on plot
st.sidebar.title("Select the columns and graph you desire to visualize")
col1 = st.sidebar.selectbox("First columns :",options=('cost',"deliveryin_min",'ratings','order'))
col2 = st.sidebar.selectbox("Second columns :",options=('ratings','deliveryin_min','cost',"order"))

#plot selection
grp = st.sidebar.selectbox("First columns :",options=("scatter",'bar'))

#plotting 
if grp == 'scatter':
    fig = px.scatter(df, x=col1, y=col2,color='names')
    fig.layout.update(showlegend=False) 
    st.write(fig)
elif grp == "bar":
    fig = plt.figure()
    plt.bar(df[col1],df[col2],color='tomato',edgecolor='black')
    st.write(fig)

#displaying the raw data
st.subheader('Raw data after performing webscraping')
st.write(dfraw.head())
st.text("Number of rows in the data "+str(df.shape[0])+' and columns '+str(df.shape[1]))
load1.text("")

#displaying the data after data cleaning
st.subheader("Data after performing data cleaning!!")

#preprocess.text("")
st.write(df.head())
