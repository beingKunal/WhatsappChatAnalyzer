import streamlit as st
from preprocess import preprocessData
import helper
import seaborn as sns
import matplotlib.pyplot as plt

st.sidebar.title('Whatsapp Chat Analyzer')
uploadedFile = st.sidebar.file_uploader('Upload File')



if(uploadedFile is not None):
    file_bytes = uploadedFile.getvalue()
    data = file_bytes.decode("utf-8")
    df = preprocessData(data)
    userNames = helper.getAllUsersOfGroup(df)
    selectedUser = st.sidebar.selectbox('Select User ',userNames)
    # st.title('Data Frame')
    # st.dataframe(df)

    if st.sidebar.button('Analyze Chats'):
        col1 , col2 = st.columns(2)
        totalMsgs , totalWords = helper.fetchStats(selectedUser, df)
        with col1:
            st.header('Total Messages')
            st.subheader(totalMsgs)
        with col2:
            st.header('Total Words')
            st.subheader(totalWords)

        # Most Active Users
        st.title('Most Active Users')
        col1 , col2 = st.columns(2)
        most_activeUsers , activenss = helper.mostActiveUsers(df)

        with col1 :
            # x_values = most_activeUsers.index
            fig, ax = plt.subplots()
            sns.barplot(x = most_activeUsers.index, y = most_activeUsers.values)
            plt.xticks(rotation = 45)
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            plt.pie(x = most_activeUsers.values, labels = most_activeUsers.index, autopct = '%.0f%%')
            st.pyplot(fig)

#         wordCloud
        st.title('Word Cloud')
        worldCloud = helper.createWordCloud(selectedUser, df)
        fig , ax = plt .subplots()
        plt.imshow(worldCloud)
        st.pyplot(fig)

#         Most common Words
        st.title('Most Common Words')
        most_common_words = helper.top25MessageWords(df, selectedUser)
        fig , ax = plt.subplots()
        sns.barplot(y = most_common_words[0] , x= most_common_words[1] , orient = 'h')
        plt.xticks(rotation = 45)
        plt.ylabel('Most common Words')
        plt.xlabel('Number of times word appears')
        st.pyplot(fig)

#         Most common Emojis
        st.title('Most common Emojis')
        emojis_df = helper.getUsageOfEmojis(df , selectedUser)
        fig, ax = plt.subplots()
        sns.barplot(y=emojis_df[0], x=emojis_df[1], orient='h')
        plt.xticks(rotation=45)
        plt.ylabel('Emojis')
        plt.xlabel('Number of times emoji Appears')
        st.pyplot(fig)

#  HeatMap for houlry activeness of users per week
        st.title('Weekly Activity Map')
        hourly_df = helper.hourlyMessagePerWeek(df , selectedUser)
        fig = plt.figure(figsize=(12, 8))
        sns.heatmap(data=hourly_df)
        st.pyplot(fig)


