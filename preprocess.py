import re
import pandas as pd


# preprocess data to extract features from whatsapp messages
def preprocessData(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    data_dic = {'user_messages': messages, 'dates': dates}
    df = pd.DataFrame(data_dic)
    df['dates'] = pd.to_datetime(df.dates, format='%d/%m/%Y, %H:%M - ')
    df_without_media = df.iloc[getIndexOfMessagesWithoutMedia(df)]
    df_new = df_without_media.reset_index(drop=True)
    separateUsersAndMsg(df_new)
    df_new.drop('user_messages', axis=1, inplace=True)
    df_new['year'] = df.dates.dt.year
    df_new['month'] = df.dates.dt.month_name()
    df_new['date'] = df.dates.dt.day
    df_new['minutes'] = df.dates.dt.minute
    df_new['hour'] = df.dates.dt.hour
    df_new['weekday'] = df.dates.dt.day_name()
    return df_new

# get index of all the messages where message has <Media omitted> in it
def getIndexOfMessagesWithoutMedia(df):
    messageIndexWithoutMedia = []
    for message in list(enumerate(df.user_messages)):
        if('<Media omitted>' not in message[1]):
            messageIndexWithoutMedia.append(message[0])
    return messageIndexWithoutMedia

# seperate users from messages text
def separateUsersAndMsg(df_new):
    names =[]
    messages = []
    pattern = '([\w\W]+?):\s'
    for message in df_new.user_messages:
        messageEntry = re.split(pattern , message)
        if(len(messageEntry) == 3):
            names.append(messageEntry[1])
            messages.append(messageEntry[2])
        else:
            names.append('group notification')
            messages.append(messageEntry[0])
    df_new['users'] = names
    df_new['messages'] = messages
