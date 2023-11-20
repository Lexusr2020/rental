
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import seaborn as sns
import numpy as np
import altair as alt
import io
import os 
import warnings
import time
import streamlit.components.v1 as components

warnings.filterwarnings('ignore')

primary_color = st.get_option('theme.base')

st.get_option("theme.backgroundColor")

st.set_page_config(page_title="New York Short Rental Analysis", page_icon=":chart_with_upwards_trend:", layout="wide")

st.title(":chart_with_upwards_trend: Pillow Palooza NYC Short-Term Rentals")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Read in data
os.chdir(r"/mount/src/rental/Data")
df = pd.read_csv("pillow_final.csv", usecols=['latitude', 'longitude'])

st.map(df.head(5000))

side_bar_text = '''
I hope you enjoy the following project. 

If you have any questions, please feel free to send me a message through the contact form at the bottom of the project.

Lex
'''

st.sidebar.header("Welcome!")

side_bar_state = 'collapsed'

st.sidebar.write(side_bar_text)

# Introduction

intro = '''
The real estate industry is a highly competitive and dynamic market, demanding continuous adaptation and
innovation to thrive. As a Data Analyst at Pillow Palooza, I am dedicated to extracting valuable insights from the
highly competitive and dynamic real estate market, specifically the short-term rental sector in New York City. My role
involves collecting, cleansing, and analyzing data to unlock growth opportunities and drive success for Pillow Palooza
in this challenging landscape.

In response to the Head of Data's request, I undertook a comprehensive project that involved gathering Airbnb
listing data from various sources and employing rigorous data cleaning techniques to ensure accuracy. The objective
was to develop a deep understanding of the market by uncovering key trends related to popular neighborhoods,
rental prices, property types, length of stay, and demand patterns over time.
The analysis conducted as part of this project holds immense potential in providing invaluable insights that can
guide Pillow Palooza's business decisions. By identifying emerging trends and patterns, we can pinpoint profitable
neighborhoods for investment, determine the most sought-after property types, and strategically price our rentals to
remain competitive.

In the forthcoming report, I will present the findings of the analysis, emphasizing the key trends and insights
uncovered. By examining various facets of the short-term rental market, our aim is to provide a comprehensive view
that enables Pillow Palooza to make informed and strategic choices. With a forward-looking perspective, this project
lays the foundation for Pillow Palooza's success in the dynamic real estate landscape of New York City.
'''

st.markdown(intro)

# Data Collection and Preparation

st.header('Data Collection and Preparation')

st.markdown('<style>div.block-container{padding-bottom:1rem;}</style>', unsafe_allow_html=True)

st.subheader('Part 1: ')

intro_text = '''
In this project, multiple datasets were collected, cleaned, and merged to gain insights into the short-term rental
market in New York City. The datasets included the Price Dataset, Room Type Dataset, and Reviews Dataset. The original datasets can be seen below.

'''
st.markdown(intro_text)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    os.chdir(r"/mount/src/rental/Data")
    price_df = pd.read_csv("prices.csv", encoding = "ISO-8859-1")
    st.write(price_df.head())

with col2:
    os.chdir(r"/mount/src/rental/Data")
    room_type_df = pd.read_excel("room_types.xlsx")
    st.write(room_type_df.head())

with col3:
    os.chdir(r"/mount/src/rental/Data")
    review_df = pd.read_csv("reviews.tsv", delimiter= '\t', encoding = "ISO-8859-1")
    st.dataframe(review_df.head()) 
    
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

price_text = '''
The Price Dataset consisted of three columns: listing_id, price, and nbhood_full. Initially, listings with a price of 0
were removed. A new column named price_per_month was created by multiplying the price by 365 and dividing it by
12 to represent the monthly price. The nbhood_full column contained both the borough and neighborhood
information, which was split into separate columns named Borough and Neighborhood. Lastly, 7 Listings with a price
of $0.00 were removed.
'''
st.markdown(price_text)

room_text = '''    
The Room Type Dataset contained three columns: listing_id, description, and room_type. The values in the
room_type column were converted to lowercase, and the data type was changed from text to category for better
analysis.
'''
st.markdown(room_text)

review_text = '''
The Reviews Dataset included three columns: listing_id, host name, and last_review. The last_review column's
data type was changed from text to datetime to enable date-based analysis.
'''
st.markdown(review_text)

cleaning_text = '''
Using pandas, all the datasets were merged into a single dataset. A new column named price_range was created
based on the Price column. The values in the price_range column were assigned as follows: 

If the price was less than or equal to \$69, it was labeled as "Budget". 

If it was less than or equal to \$175, it was labeled as "Average".

If it was less than or equal to \$350, it was labeled as "Expensive". 

Otherwise, it was labeled as "Extravagant".

The resulting merged dataset included the following columns: listing_id, price, Borough, Neighborhood,
price_per_month, description, room_type, host_name, last_review, and price_range.
'''
st.markdown(cleaning_text)

st.subheader('Part 2: ')

part_2_text = '''
Additional data was later gathered which resulted in columns such as Minimum_Nights, Number_Of_Reviews,
Reviews_Per_Month, Availability_365, and Booked_Days_365. The three same datasets, prices, room_types &
reviews, were merged into one dataset using SQL. Please note, the dataset from Part 1 which was used for cleaning is different from the dataset in Part 2.

The final dataset, enriched with various columns, provides a comprehensive view of the short-term rental market
in New York City. This dataset serves as the foundation for further analysis and exploration of trends, patterns, and
correlations within the market.
'''
st.markdown(part_2_text)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Read in data
os.chdir(r"/mount/src/rental/Data")
df = pd.read_csv("pillow_final.csv")

del df['Unnamed: 0.2']
del df['Unnamed: 0']
del df['Unnamed: 0.1']

# Change the data type of the last_review column to datetime
#df["last_review"] = pd.to_datetime(df["last_review"])

# Create labels for the price range, label_names
label_names = ["Budget", "Average", "Expensive", "Extravagant"]

# Create the label ranges, ranges
ranges = [0, 69, 175, 350, np.inf]

# Insert new column, price_range, into DataFrame
df["price_range"] = pd.cut(df["price"], bins=ranges, labels=label_names)

df['price_per_month'] =  df["price"] * 365 / 12

#df['price_per_month'] = df['price_per_month']..astype(int)

st.dataframe(df.head()) 

#buffer = io.StringIO()
#df.info(buf=buffer)
#s = buffer.getvalue()
#
#st.text(s)

st.divider()

st.markdown('<style>div.block-container{padding-bottom:1rem;}</style>', unsafe_allow_html=True)

st.header('Peroject Files')

project_col1, project_col2, project_col3 = st.columns(3)

tab1, tab2, tab3 = st.tabs(["SQL", "Data Cleaning", "Analyze Data"])


with tab1:
    st.header("SQL Queries")
    sql_link = 'https://github.com/Lexusr2020/NYC-Short-Term-Rental/blob/main/queries.txt'
    st.markdown(sql_link,unsafe_allow_html=True)

with tab2:
    st.header("Data Cleaning Notebook")
    cleaning_notebook_link = 'https://github.com/Lexusr2020/NYC-Short-Term-Rental/blob/main/data_cleaning.ipynb'
    st.markdown(cleaning_notebook_link,unsafe_allow_html=True)

with tab3:
    st.header("Analyzing Data Notebook")
    analyze_notebook_link = 'https://github.com/Lexusr2020/NYC-Short-Term-Rental/blob/main/queries.txt'
    st.markdown(analyze_notebook_link,unsafe_allow_html=True)
   
st.divider()

data = df.copy()

data['last_review'] = data['last_review'].str.slice(stop=-8)

data['last_review'] = pd.to_datetime(data['last_review']).dt.date

st.header('Key Findings')

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

st.subheader('Price')

price_text = '''
The dataset provides various statistical measures for analyzing the prices of listings:

The average price of listings is \$141.82, serving as a measure of the central tendency. The
median price, \$105.00, represents the middle value and gives an indication of the typical price, less affected by
extreme values. The maximum price observed is \$7,500.0, indicating the highest price among all listings. The mode,
\$150.00, reveals the most common price category in the dataset.

The price range is \$7,490.0, representing the difference between the maximum and minimum prices and indicating the
spread of prices across the dataset. The interquartile range (IQR) for all data is 106.00, capturing the range within
which the central 50% of prices fall. The standard deviation, 147.35, reflects a relatively large spread of prices from
the mean.

Additionally, the dataset includes 1326 outliers, which are values significantly deviating from the rest of the data.
These outliers may represent unusual or extreme price points deserving further examination.
'''
st.markdown(price_text)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

os.chdir(r"/mount/src/rental/images")
price_distribution_image = Image.open('price_distribution.png')

price_mean = np.round(data["price"].mean(), 2)
price_min = np.round(data["price"].min(), 2)
price_max = np.round(data["price"].max(), 2)

#Outlier detection
price_q1 = data["price"].quantile(0.25)
price_q3 = data["price"].quantile(0.75)
iqr = price_q3 - price_q1
all_data_outliers = data[(data["price"] < (price_q1 - 1.5 * iqr)) | (data["price"] > (price_q3 + 1.5 * iqr))]

price_col1, price_col2 = st.columns(2)

with price_col1:
    st.image(price_distribution_image)

with price_col2:    
    st.write('Price Mean: $', price_mean)
    st.write('Price Min: $', price_min)
    st.write('Price Max: $', price_max)
    st.write('Price Range: $', price_max - price_min)
    st.write('All Data Interquartile range: ', data["price"].quantile(0.75) - data["price"].quantile(0.25))
    st.write('All Data Standard deviation: ', np.round(data["price"].std(), 2))
    st.write('Number of outliers: ', all_data_outliers.shape[0])
    
st.divider()

# Calculate the correlation coefficient
correlation_coefficient = data['booked_days_365'].corr(data['price'])

st.subheader('Booked Days 365 & Price Correlation')

st.write(f'Booked Days and Price Correlation: The correlation coefficient between Booked_Days_365 and Price is {correlation_coefficient}')

correlation_coefficient_text = '''
This correlation coefficient suggests a weak negative relationship between the length of stay and the price of the
listings in the dataset.
'''

st.write(correlation_coefficient_text)

source = data

chart = alt.Chart(source).mark_circle(size=20).encode(
    x='booked_days_365',
    y='price',
    color='borough'
).interactive()

st.altair_chart(chart, theme=None, use_container_width=True)

st.divider()

st.subheader('Room Types')

room_types_text1 = '''
The analysis of room types reveals interesting patterns and preferences among Airbnb listings. The three main
categories, namely Entire Home/Apt, Private Room, and Shared Room, exhibit distinct characteristics in terms of the
number of listings and average prices.

Among these categories, Entire Home/Apt stands out as the most prevalent, with a total of 13,266 listings and an
average price of \$197.00. It is followed closely by Private Room, which boasts 11,351 listings and an average price of
\$82.00. Although Shared Room has the lowest number of listings, with only 585, it offers the most affordable option,
with an average price of \$54.00.
'''
st.write(room_types_text1)

room_types_counts = data.groupby("room_type", as_index = False)["listing_id"].count()

room_types_counts = room_types_counts.rename(columns={'listing_id': 'total_listings'})

room_types_avg_price = data.groupby("room_type")["price"].mean().reset_index()

room_types_avg_price = room_types_avg_price.rename(columns={'price': 'avg_price'})

room_col_left, room_col_right = st.columns(2)

with room_col_left:
    fig = px.bar(room_types_counts, x = "room_type", y = "total_listings", text = ['{:,.0f}'.format(x) for x in room_types_counts["total_listings"]], template = "seaborn", title='Total Listings By Room Type')
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View Data"):
        st.write(room_types_counts.style.background_gradient(cmap="Blues"))
        

with room_col_right:
    fig = px.bar(room_types_avg_price, x = "room_type", y = "avg_price", text = ['${:,.2f}'.format(x) for x in room_types_avg_price["avg_price"]], template = "seaborn", title='Average Price By Room Type')
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View Data"):
        st.write(room_types_avg_price.style.background_gradient(cmap="Blues"))
        
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
        
room_types_text2 = '''
Furthermore, when considering the review dates as an approximation for bookings throughout the year, it becomes
evident that Entire Home/Apt is the most popular choice among travelers. It experiences a peak with a total of
164,162 booked days, indicating a strong preference for having an entire home or apartment to themselves. On the
other hand, Shared Room has the lowest number of booked days, peaking at only 10,659.

These findings emphasize the dominance of Entire Home/Apt listings in terms of popularity and demand. It is worth
noting that Private Room closely follows Entire Home/Apt, indicating that many guests still value the option of having
their own private space within a larger property. Conversely, the Shared Room category appears to be less popular,
potentially due to its communal nature and lower number of available listings.

Overall, this analysis sheds light on the distribution of room types, their respective average prices, and the booking
trends associated with each category. These insights can inform strategic decision-making for hosts and help them
cater to the preferences and needs of their target audience.
'''
st.write(room_types_text2)
        
mean_booked_days_over_time = data.groupby(['last_review', 'room_type'])['booked_days_365'].sum().reset_index()

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

chart2 = alt.Chart(mean_booked_days_over_time, height=450).mark_line(strokeWidth=1).encode(
  x=alt.X('last_review:T', title='last review date'),
  y=alt.Y('booked_days_365:Q', title='total booked days'),
  color=alt.Color("room_type")
).properties(title="Total Booked Days By Room Type Over Time")
st.altair_chart(chart2, theme=None, use_container_width=True)

with st.expander("View Data"):
    st.write(mean_booked_days_over_time.style.background_gradient(cmap="Blues"))

st.divider()

st.subheader('Boroughs & neighbourhoods')

boroughs_text = '''
Brooklyn stands out as the leading borough in terms of the number of listings, with a total of 10,460 listings,
accounting for 41.50% of the dataset. With an average monthly price of \$3,710.00, these listings generate a
substantial annual revenue of \$279,130,240.00.

Manhattan closely trails behind with 10,322 listings, representing 40.96% of the total. The annual revenue generated
by Manhattan listings amounts to \$393,405,670.00, with an average monthly price of \$5,597.00.

In third place is Queens, with a total of 3,456 listings, making up 13.71% of the dataset. These listings contribute to
an annual revenue of \$58,404,083.00.

The Bronx and Staten Island, although accounting for less than 3% of the total listings, still generate a combined
annual revenue of \$12,768,099.00.

The top 10 neighbourhoods by annual revenue demonstrate high average booked days ranging from 209 to 256 days, along with average prices per stay ranging from \$91.00 to \$272.00
'''

st.write(boroughs_text)

pie_data_listings = data.groupby('borough')['listing_id'].count().reset_index().sort_values('listing_id', ascending=False)

data['annual_revenue'] = data['price'] * data['booked_days_365']

pie_data_yearly_reveneue = data.groupby('borough')['annual_revenue'].sum().reset_index().sort_values('annual_revenue', ascending=False)

boroughs_neighbourhoods_left, boroughs_neighbourhoods_right = st.columns(2)

neighborhoods = data.groupby('neighbourhood').agg({'annual_revenue' : 'sum',
                                                   'price' : 'mean',
                                                   'listing_id' : 'count',
                                                   'booked_days_365' : 'mean'}).reset_index().sort_values('booked_days_365', ascending=False)

neighborhoods = neighborhoods.rename(columns={'price': 'avg_price', 'listing_id': 'total_listings', 'booked_days_365': 'avg_booked_days'})

neighborhoods_top_10 = neighborhoods.sort_values('annual_revenue', ascending=False)

neighborhoods_top_10 = neighborhoods_top_10.head(10)

pie_data_col1, pie_data_col2, pie_data_col3 = st.columns(3)

with pie_data_col1:
    fig = px.pie(pie_data_listings, values = "listing_id", names = "borough", hole = 0.5, title="% of Listings by Borough")
    fig.update_traces(text = pie_data_listings["borough"], textposition = "outside")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View Data"):
        st.write(pie_data_listings.style.background_gradient(cmap="Blues"))
        
with pie_data_col2:
    fig = px.pie(pie_data_yearly_reveneue, values = "annual_revenue", names = "borough", hole = 0.5, title="% of Annual Revenue by Borough")
    fig.update_traces(text = pie_data_yearly_reveneue["borough"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

    with st.expander("View Data"):
        st.write(pie_data_yearly_reveneue.style.background_gradient(cmap="Blues"))      

with pie_data_col3:
    fig = px.bar(neighborhoods_top_10, x = "neighbourhood", y = "avg_booked_days", text = ['{:,.0f} Days'.format(x) for x in neighborhoods_top_10["avg_booked_days"]], template = "seaborn", title="Top 10 Neighbourhoods by Revenue")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View Data"):
        st.write(neighborhoods_top_10.style.background_gradient(cmap="Blues"))
  
st.divider()

st.subheader('Price Ranges')

booked_days_365_text1 = '''
The analysis of the review dates as an approximation for bookings throughout the year reveals interesting insights.
The "Budget" price range category emerges as the most popular category overall, consistently attracting a high
number of bookings throughout the year. In particular, June experiences a peak with a total of 163,381 booked days,
indicating a strong demand for affordable accommodations during that month.

December stands out as another noteworthy period, with a significant increase in bookings, totaling 59,196 booked
days. This surge in bookings can be attributed to the holiday season, as many tourists flock to New York City to
celebrate the New Year in iconic locations like Times Square.
'''
st.markdown(booked_days_365_text1)

ranges_days_over_time = data.groupby(['last_review', 'price_range'])['booked_days_365'].sum().reset_index()

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

chart3 = alt.Chart(ranges_days_over_time, height=450).mark_line(strokeWidth=1).encode(
  x=alt.X('last_review:T', title='last review date'),
  y=alt.Y('booked_days_365:Q', title='total booked days'),
  color=alt.Color('price_range', scale={"range": ["red", "gold", 'blue', 'orange']})
).properties(title="Price Range By Total Booked Days")
st.altair_chart(chart3, theme=None, use_container_width=True)

with st.expander("View Data"):
    st.write(ranges_days_over_time.style.background_gradient(cmap="Blues"))
    
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

price_ranges_text = '''
The price range categories of "Budget," "Average," and "Expensive" all exhibit a similar pattern, surpassing 200 avgerage
booked days starting in early May and continuing to rise until the end of June. However, after July 5, there is a lack of
further information as it marks the last review timestamp available in the dataset.

Overall, the analysis provides valuable insights into the booking trends across different price ranges throughout the
year. It highlights the popularity of the "Budget" category, the impact of holiday seasons on bookings, and the time
frame in which bookings tend to peak.
'''
st.write(price_ranges_text)

price_ranges_by_listing_count = data.groupby("price_range", as_index = False)["listing_id"].count().sort_values(by='listing_id', ascending=False)

price_ranges_by_listing_count = price_ranges_by_listing_count.rename(columns = {'listing_id' : 'total_listings'})

price_ranges_by_price = data.groupby(by = ["price_range"], as_index = False)["booked_days_365"].mean().sort_values(by='booked_days_365', ascending=False)

price_ranges_by_price = price_ranges_by_price.rename(columns = {'booked_days_365' : 'total_booked_days'})

price_col_left, price_col_right = st.columns(2)

with price_col_left:
    fig = px.bar(price_ranges_by_listing_count, x = "price_range", y = "total_listings", text = ['{:,.0f}Listings'.format(x) for x in price_ranges_by_listing_count["total_listings"]], template = "seaborn", title='Total Listings By Price Range')
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View Data"):
        st.write(price_ranges_by_listing_count.style.background_gradient(cmap="Blues"))
        
with price_col_right:
    fig = px.bar(price_ranges_by_price, x = "price_range", y = "total_booked_days", text = ['{:,.0f}Days'.format(x) for x in price_ranges_by_price["total_booked_days"]], template = "seaborn", title='Avg Booked Days By Price Range')
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("View Data"):
        st.write(price_ranges_by_price.style.background_gradient(cmap="Blues"))
    
st.divider()

st.subheader('Reviews')

reviews_text = '''
Brooklyn takes the lead in terms of total reviews, particularly in the "Average" price range, with a substantial count of
254,489 reviews. Following closely behind is the "Budget" price range, which receives 112,421 reviews.

Moving to Manhattan, the "Average" price range receives the highest number of reviews with a total of 229,668. In
second place is the "Expensive" price range, accumulating 101,529 reviews.

In Queens, the "Budget" price range is the most reviewed category, garnering a total of 72,163 reviews. Not far
behind is the "Average" price range, with 62,943 reviews, making it a close contender for the top spot.
'''
st.write(reviews_text)

# Brooklyn Data
brooklyn_data = data[data['borough'] =='Brooklyn']
brooklyn_data = brooklyn_data.groupby('price_range')["number_of_reviews"].sum().reset_index().sort_values('number_of_reviews', ascending=False)

# Bronx Data
bronx_data = data[data['borough'] =='Bronx']
bronx_data = bronx_data.groupby('price_range')["number_of_reviews"].sum().reset_index().sort_values('number_of_reviews', ascending=False)

# Manhattan Data
Manhattan_data = data[data['borough'] =='Manhattan']
Manhattan_data = Manhattan_data.groupby('price_range')["number_of_reviews"].sum().reset_index().sort_values('number_of_reviews', ascending=False)

# Queens Data
Queens_data = data[data['borough'] =='Queens']
Queens_data = Queens_data.groupby('price_range')["number_of_reviews"].sum().reset_index().sort_values('number_of_reviews', ascending=False)

# Staten Island Data
staten_data = data[data['borough'] =='Staten Island']
staten_data = staten_data.groupby('price_range')["number_of_reviews"].sum().reset_index().sort_values('number_of_reviews', ascending=False)

all_boroughs = data.groupby(['price_range', 'borough'])['number_of_reviews'].sum().reset_index().sort_values('number_of_reviews', ascending=True)

all_boroughs = all_boroughs.rename(columns={'number_of_reviews':'total_reviews'})
        
fig = px.bar(all_boroughs.dropna(), y = "price_range", x = "total_reviews", text = ['{:,.0f}'.format(x) for x in all_boroughs["total_reviews"]], template = "seaborn", color='borough')
st.plotly_chart(fig, use_container_width=True)
with st.expander("View Data"):
    st.write(all_boroughs.style.background_gradient(cmap="Blues"))

borough_tab1, borough_tab2, borough_tab3, borough_tab4, borough_tab5 = st.tabs(['Brooklyn', 'Bronx', 'Manhattan', 'Queens', 'Staten Island'])

with borough_tab1:
    fig = px.bar(brooklyn_data.dropna(), x = "price_range", y = "number_of_reviews", text = ['{:,.0f}'.format(x) for x in brooklyn_data["number_of_reviews"]], template = "seaborn")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("View Data"):
        st.write(brooklyn_data.style.background_gradient(cmap="Blues"))
        
with borough_tab2:
    fig = px.bar(bronx_data.dropna(), x = "price_range", y = "number_of_reviews", text = ['{:,.0f}'.format(x) for x in bronx_data["number_of_reviews"]], template = "seaborn")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("View Data"):
        st.write(bronx_data.style.background_gradient(cmap="Blues"))
        
with borough_tab3:
    fig = px.bar(Manhattan_data.dropna(), x = "price_range", y = "number_of_reviews", text = ['{:,.0f}'.format(x) for x in Manhattan_data["number_of_reviews"]], template = "seaborn")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("View Data"):
        st.write(Manhattan_data.style.background_gradient(cmap="Blues"))
        
with borough_tab4:
    fig = px.bar(Queens_data.dropna(), x = "price_range", y = "number_of_reviews", text = ['{:,.0f}'.format(x) for x in Queens_data["number_of_reviews"]], template = "seaborn")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("View Data"):
        st.write(Queens_data.style.background_gradient(cmap="Blues"))
        
with borough_tab5:
    fig = px.bar(staten_data.dropna(), x = "price_range", y = "number_of_reviews", text = ['{:,.0f}'.format(x) for x in staten_data["number_of_reviews"]], template = "seaborn")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("View Data"):
        st.write(staten_data.style.background_gradient(cmap="Blues"))
            
st.divider()

st.header('Recommendations')

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

recommendation_text = '''
Based on the analysis of the Airbnb listing data, the following recommendations can be made:

Focus on the "Entire Home/Apt" Category: Given its popularity and desirability among renters, it is recommended to
prioritize and expand the availability of entire homes or apartments in your rental portfolio. This category has
consistently shown higher demand and booking rates, indicating a strong preference among travelers.

Target Top Neighborhoods: Concentrate your efforts and resources on the top-performing neighborhoods such as
East Village, Williamsburg, and East Harlem. These neighborhoods exhibit high average booked days and attractive
average prices per stay, indicating a favorable market for short-term rentals. Investing in these areas and optimizing
your listings can lead to increased occupancy and revenue.

Pay Attention to Brooklyn and Manhattan: These two boroughs, particularly Brooklyn and Manhattan, are the most
promising areas for your rental business. They account for a significant portion of the total average booked days,
suggesting a higher potential for bookings and profitability. Allocate resources and marketing efforts to maximize
your presence in these boroughs.

Consider Seasonal Demand: Take advantage of the seasonal booking patterns observed in the data. June, with its
peak in bookings, presents an opportunity to capitalize on the demand for affordable accommodations. Additionally,
December experiences a surge in bookings, likely due to the holiday season. Tailor your pricing and marketing
strategies to cater to these seasonal peaks and adjust your inventory accordingly.

Continuously Collect and Analyze Data: To stay updated on the evolving market trends and patterns, it is
recommended to regularly collect and analyze data beyond the available dataset. This will provide more accurate and
up-to-date insights, allowing you to make informed decisions and adapt your strategies accordingly.

By implementing these recommendations, you can enhance your competitiveness, optimize occupancy rates, and
maximize revenue in the dynamic short-term rental market of New York City. Stay agile, monitor market changes, and
align your offerings with the preferences and demands of your target audience to ensure sustained growth and
success in the industry.
'''

st.write(recommendation_text)

st.header('Conclusion')

st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

conclusion_text = '''
The analysis of Airbnb data provides valuable insights for making informed decisions in the short-term rental market.
It is crucial to prioritize the "Entire Home/Apt" category, which consistently attracts higher popularity among users.
Brooklyn and Manhattan stand out as the top boroughs, with a significant share of average booked days. Focusing
efforts on these areas can significantly increase rental occupancy and revenue.

Examining review dates reveals notable trends. The "Budget" price range consistently generates bookings, with a
peak in June. Additionally, December experiences increased demand, likely due to the holiday season.

It's important to note that the dataset lacks information beyond July 5, which limits a comprehensive analysis of
booking trends throughout the year. Collecting additional data would provide a more comprehensive understanding.

These insights serve as a foundation for strategic decision-making in pricing, investment, and marketing. By
leveraging these findings, Pillow Palooza can optimize their offerings, adapt to customer demands, and thrive in New
York City's dynamic short-term rental market.
'''

st.write(conclusion_text)

st.divider()

st.header('Contact')

contact_col1, contact_col2, contact_col3 = st.columns(3)

with contact_col2:
    st.subheader("Get In Touch!")
    
    contact_form = """
    <form action="https://formsubmit.co/3062550fc7e1598d330a0c8641949e16" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here", cols="80" rows="8"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)

    os.chdir(r"/mount/src/rental/style")
    style_file = 'style.css'

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css(style_file)



    
    
















