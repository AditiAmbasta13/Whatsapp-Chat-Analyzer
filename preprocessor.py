import re
import pandas as pd
from datetime import time

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    #df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M\u202f%p')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    date = []
    times = []
    for i in df['date']:
        date.append(i.split(', ')[0])
        times.append(i.split(', ')[1])

    time = []
    am_pm = []
    for i in times:
        time.append(i.split('\u202f')[0])
        am_pm.append(i.split('\u202f')[1])

    df = pd.DataFrame({'user_message': messages, 'date': date, 'time': time, 'am/pm' : am_pm})

    user = []
    msg = []
    for i in df['user_message']:
        x = re.split("([\w\W]+?):\s", i)  # Split using regex to handle various message formats
        if len(x) > 2:  # Check if both user and message were extracted
            user.append(x[1])
            msg.append(x[2])
        else:
            user.append(None)  # Append None for missing user
            msg.append(None)  # Append None for missing message

    df['user'] = user  # Now the lengths should match
    df['message'] = msg
    df.drop(columns=['user_message'], inplace=True)

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = pd.to_datetime(df['time']).dt.hour
    df['minute'] = pd.to_datetime(df['time']).dt.minute
    df.drop(columns=['time'], inplace=True)

    period = []
    for hour in df[['day_name', 'hour']][['hour']].astype(int)['hour']: # Cast 'hour' column to integers
        if hour == 0:
            period.append(str(12) + ":" + str('00') + " AM")
        elif hour < 12:
            period.append(str(hour) + ":" + str('00') + " AM")
        elif hour == 12:
            period.append(str(12) + ":" + str('00') + " PM")
        else:
            period.append(str(hour - 12) + ":" + str('00') + " PM")

    df['period'] = period

    return df
