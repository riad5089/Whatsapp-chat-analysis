import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2}\s-\s'
    massage = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"user_massage": massage, "massage_dates": dates})
    df['massage_dates'].str.replace('pm', 'PM').str.replace('am', 'AM')

    df["massage_dates"] = pd.to_datetime(df["massage_dates"], format='%d/%m/%Y, %I:%M %p - ')
    df.rename(columns={"massage_dates": "date"}, inplace=True)
    users = []
    messages = []
    for message in df["user_massage"]:
        entry = re.split("([\w\W]+?):\s", message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])
    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user_massage"], inplace=True)
    df["only_date"] = df["date"].dt.date
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["day_name"]=df["date"].dt.day_name()
    df["hour"] = df.date.dt.hour
    df['minute'] = df.date.dt.minute
    return df