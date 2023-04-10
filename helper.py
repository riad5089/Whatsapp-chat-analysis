from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import nltk
from nltk.corpus import stopwords
stop_words=stopwords.words("english")
import matplotlib.pyplot as plt
extract=URLExtract()
def fetch_stats(selected_users,df):
    if selected_users !="overall":
        df=df[df["user"]==selected_users]
    num_messages = df.shape[0]
    word = []
    for message in df["message"]:
        word.extend(message.split())

    number_media_messge=df[df["message"]=="<Media omitted>\n"].shape[0]
    #fetch number of links shared
    links=[]
    for message in df["message"]:
        links.extend(extract.find_urls(message))
    return num_messages, len(word),number_media_messge,len(links)


def most_busy_users(df):

    x = df["user"].value_counts().head()
    df=round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"index": "name", "user": "percent"})
    return x,df


def create_wordcloud(selected_users,df):

    if selected_users !="overall":
        df=df[df["user"]==selected_users]

    temp=df[df["user"]!="group_notification"]
    temp = temp[temp["user"] != "<Media omitted>\n"]

    def reomve_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
            return " ".join(y)


    wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    temp["message"]=temp["message"].apply(reomve_stop_words)
    df_wc=wc.generate(temp["message"].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user !="overall":
        df=df[df["user"]==selected_user]

    temp=df[df["user"]!="group_notification"]
    temp = temp[temp["user"] != "<Media omitted>\n"]
    words = []
    for message in df["message"]:
        for word in message.lower().split():
            if word not in stopwords.words("english"):
                words.append(word)
    moost_commom_df=pd.DataFrame(Counter(words).most_common(20))
    return moost_commom_df
def emmoji_helper(selected_user,df):
    if selected_user!="overall":
        df=df[df["user"]==selected_user]
    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
#
def monthly_timeline(selectd_user,df):
     if selectd_user !="overall":
        df=df[df["user"]==selectd_user]


     timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()
     time = []
     for i in range(timeline.shape[0]):
         time.append(timeline['month'][i] + "-" + str(timeline["year"][i]))
     timeline['time'] = time
     return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df["day_name"].value_counts()

def month_activaty_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df["month"].value_counts()

    # df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
    #     columns={'index': 'name', 'user': 'percent'})
    # return x,df
    # num_messages=df.shape[0]
    # if selected_users=="overall":
    #     # 1. Fatch number of messages
    #     num_messages = df.shape[0]
    #     # 2. Number of words
    #     word = []
    #     for message in df["message"]:
    #         word.extend(message.split())
    #
    #     return num_messages,len(word)
    # else:
    #     new_df=df[df["user"]==selected_users]
    #     num_messages=new_df.shape[0]
    #     word = []
    #     for message in new_df["message"]:
    #         word.extend(message.split())
    #     return num_messages,len(word)