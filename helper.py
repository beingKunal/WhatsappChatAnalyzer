from wordcloud import WordCloud
from nltk.corpus import stopwords
import string
from collections import Counter
import pandas as pd
import emoji

def getAllUsersOfGroup(dataframe):
    userNames = list(dataframe.users.unique())
    userNames.remove('group notification')
    userNames.remove('ERROR')
    userNames.insert(0 , 'OverAll')
    userNames.sort()
    return userNames


def fetchStats(selectedUser , df):
    if(selectedUser != 'OverAll'):
        df = df.loc[df.users == selectedUser]
    messageCount = 0
    for message in df.messages:
        messageCount += len(message.split(' '))
    return df.shape[0] , messageCount

def mostActiveUsers(w_app_data):
    most_active_users = w_app_data.users.value_counts().head()
    activenss = round((w_app_data.users.value_counts()/w_app_data.shape[0]) * 100,2).reset_index()
    return most_active_users , activenss

def createWordCloud(selectedUser , df):
    if(selectedUser != 'OverAll'):
        df = df.loc[df.users == selectedUser]
    wc = WordCloud(height=500 , width=500 , min_font_size=10 , background_color='white')
    # generates an image of words retrieved from df.messages
    df_wc = wc.generate(df.messages.str.cat(sep = ' '))
    return df_wc

def top25MessageWords(df , selectedUser):
    swords = stopwords.words('english') +  list(string.punctuation)
    msgs = []
    if(selectedUser != 'OverAll'):
        df = df.loc[df.users == selectedUser]
    df_without_group_notification = df[df.messages != 'group notification']
    for message in df_without_group_notification.messages:
        currentMsgList = message[0:-2].split(' ')
        for msg in currentMsgList:
            if(msg.lower() not in swords):
                msgs.append(msg.lower())
    msgs = Counter(msgs)
    return pd.DataFrame(msgs.most_common(25))

def getUsageOfEmojis(df , selectedUser):
    if(selectedUser != 'OverAll'):
        df = df.loc[df.users == selectedUser]
    emojis = []
    for messages in df.messages:
        emojiList= [c for c in messages if c in emoji.UNICODE_EMOJI['en']]
        emojis.extend(emojiList)
    return pd.DataFrame(Counter(emojis).most_common(20))

def hourlyMessagePerWeek(df, selectedUser):
    if(selectedUser != 'OverAll'):
        df = df.loc[df.users == selectedUser]
    df['hour_range'] = pd.cut(x=df.hour, bins=[i for i in range(25)])
    hourly_df = df.groupby(by=['hour_range', 'weekday']).count()['messages'].reset_index()
    hourly_df['messages'].fillna(0, inplace=True)
    hourly_df_heat_map = hourly_df.pivot_table(columns='hour_range', index='weekday', values='messages')
    return hourly_df_heat_map



