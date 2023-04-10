import streamlit as st
import preprocessing
import matplotlib.pyplot as plt
import helper
st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode("utf-8") #convert the file to string
    df=preprocessing.preprocess(data)
    # st.dataframe(df)
    #fatch unique users
    user_list=df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"overall")
    selected_users=st.sidebar.selectbox("show analysis with respect to",user_list)

    if st.sidebar.button("Show analysis"):
        num_messages,word,number_media_message,links=helper.fetch_stats(selected_users,df)
        st.title("Top statistics")
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total Wods")
            st.title(word)
        with col3:
            st.header("Media shared")
            st.title(number_media_message)

        with col4:
            st.header("Links Shared")
            st.title(links)

        #timeline

        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_users,df)
        fig,ax=plt.subplots()
        ax.plot(timeline["time"],timeline["message"])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_users, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_users,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activaty_map(selected_users, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            st.pyplot(fig)



        #finding the busiest users in the group
        if selected_users=="overall":
            st.title("Most busy user")
            x,new_df= helper.most_busy_users(df)
            fig,ax = plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        st.title("wordcloud")
        df_wc=helper.create_wordcloud(selected_users,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        #most common word
        most_common_df=helper.most_common_words(selected_users,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation="vertical")
        st.title("MOst common word")
        st.pyplot(fig)
        #emoji analysis
        emoji_df=helper.emmoji_helper(selected_users,df)
        st.title("emoji_analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%.2f")
            st.pyplot(fig)



















