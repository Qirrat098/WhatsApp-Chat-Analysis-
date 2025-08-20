import re
import pandas as pd


def preprocess(data):
    # Match dates like [5/19/25, 11:36:08 AM]
    pattern = r"\[(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2}\s?[APMapm]{2})\]"

    messages = re.split(pattern, data)[1:]  # split chat text
    dates = re.findall(pattern, data)  # extract date-time

    # Every odd index = date, even index = message
    df = pd.DataFrame({
        "message_date": dates,
        "user_message": messages[1::2]  # take only messages
    })

    # Convert date strings → datetime
    df["message_date"] = pd.to_datetime(df["message_date"], format="%m/%d/%y, %I:%M:%S %p")

    # Split user/message
    users, msgs = [], []
    for m in df["user_message"]:
        entry = re.split(r"([\w\W]+?):\s", m, maxsplit=1)
        if len(entry) > 2:
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append("group_notification")
            msgs.append(entry[0])

    df["user"] = users
    df["message"] = msgs
    df.drop(columns=["user_message"], inplace=True)

    # Extra datetime breakdown
    df["date"] = df["message_date"].dt.date
    df["year"] = df["message_date"].dt.year
    df["month"] = df["message_date"].dt.month_name()
    df["day"] = df["message_date"].dt.day
    df["day_name"] = df["message_date"].dt.day_name()
    df["hour"] = df["message_date"].dt.hour
    df["minute"] = df["message_date"].dt.minute

    return df
