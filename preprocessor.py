import re
import pandas as pd

def preprocess(data):
    # Pattern for timestamp in your chat
    pattern = r'\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}:\d{2}\s?[APM]{2})\]\s'

    # Split messages and dates
    messages = re.split(pattern, data)[1:]  # first element before first timestamp is empty
    # messages structure: [date1, time1, message1, date2, time2, message2, ...]

    dates = []
    text_messages = []
    for i in range(0, len(messages), 3):
        date_str = messages[i] + ", " + messages[i+1]
        msg = messages[i+2].strip()
        dates.append(date_str)
        text_messages.append(msg)

    df = pd.DataFrame({
        "message_date": dates,
        "user_message": text_messages
    })

    # Convert to datetime
    df["message_date"] = pd.to_datetime(df["message_date"], format="%m/%d/%y, %I:%M:%S %p")

    # Split user and message
    users = []
    msgs = []
    for m in df["user_message"]:
        entry = re.split(r'([\w\W]+?):\s', m, maxsplit=1)
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
    df["month_num"] = df["message_date"].dt.month
    df["month"] = df["message_date"].dt.month_name()
    df["day"] = df["message_date"].dt.day
    df["day_name"] = df["message_date"].dt.day_name()
    df["hour"] = df["message_date"].dt.hour
    df["minute"] = df["message_date"].dt.minute

    return df
