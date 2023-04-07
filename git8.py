import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
pip install python-git
pip install snscrape
#pip install --upgrade --user pyqtwebengine==5.12.1
#pip install --upgrade --user pyqt5==5.12.3
#pip install streamlit
col1, col2,= st.columns([1,6])
attributes_container = []
with col1:
    users_name = st.text_input("username")
since1 = st.date_input("since")
until1 = st.date_input("until")
with col1:
    st.write(since1)
    st.write(until1)
filters = [f'since:{since1}', f'until:{until1}']
from_filters = []
for user in users_name:
    from_filters.append(f'from:{user}')
filters.append(' OR '.join(from_filters))
for n, k in enumerate(users_name):
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(' '.join(filters)).get_items()):
        if i > 100:
            break
        attributes_container.append([tweet.date, tweet.likeCount, tweet.url, tweet.content, tweet.id, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.media])
# Using TwitterSearchScraper to scrape data and append tweets to list
tweets_df1 = pd.DataFrame(attributes_container, columns=["date", "like_count", "url", "tweet_content", "id", "user", "reply_count", "retweet_count", "language", "source"])
with col2:
    st.write(tweets_df1)
#from io import BytesIO
#from pyxlsb import open_workbook as open_xlsb
df = tweets_df1
json1 = df.to_json()
csv = df.to_csv()
#df_xlsx = to_excel(df)
#df_csv = to_csv(df)
#df_json = to_excel(df)
#st.download_button(label='📥 Download Current Result as xlsx',
#                                data=df_xlsx ,
#                                file_name= 'train.xlsx')
with col1:
    st.download_button(label='📥 Download Current Result as csv',
                                    data=csv,
                                    file_name= 'train.csv')
    st.download_button(label='📥 Download Current Result as json',
                                    data=json1,
                                    file_name= 'train.json')

with col1:
    button1 = st.button("Upload to Mongo")
if button1:
    from pymongo import MongoClient

    client = MongoClient("mongodb://localhost:27017");
    print("Connection Successful")
    mydb = client["TWEET"]
    mycol = mydb["TWEETCOLL"]
    # mydb.mycol.delete_many({})
    import json

    # records = json.loads(tweets_df1.to_json(orient='records'))
    data = json.loads(tweets_df1.to_json(orient='records'))
    from datetime import datetime

    Date = datetime.now().strftime('%d-%m-%Y')
    dict = {"Scraped Word": users_name, "Scraped Date": Date, "Data": data}
    mydb.mycol.insert_many([dict])
with col1:
    st.write("finished")

