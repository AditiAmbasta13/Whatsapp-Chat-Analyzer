import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

st.header("Welcome to WhatsApp Chat Analyzer!")

uploaded_files = st.sidebar.file_uploader("Choose a file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    data = bytes_data.decode("utf-8")
    st.write("filename:", uploaded_file.name)
    # st.write(data)
    df = preprocessor.preprocess(data)

    st.dataframe(df)

     # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list = [user for user in user_list if user is not None]
    if 'group_notification' in df:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, total_words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.header("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.title(num_messages)
        with col2:
            st.subheader("Total Words")
            st.title(total_words)
        with col3:
            st.subheader("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.subheader("Links Shared")
            st.title(num_links)

        col1,col2 = st.columns(2)

        with col1:
            # monthly timeline
            st.header("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            # daily timeline
            st.header("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # activity map
        st.header('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.header("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.header('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df) 

        # WordCloud
        st.header("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.header('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.header("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)