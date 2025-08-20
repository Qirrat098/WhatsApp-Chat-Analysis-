import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly timeline
        timeline = helper.monthly_timeline(selected_user, df)
        if timeline is not None and not timeline.empty:
            fig, ax = plt.subplots()
            ax.plot(timeline["time"], timeline["message"], color="green")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        else:
            st.warning("No monthly timeline data available.")

        # Daily timeline
        daily_timeline = helper.daily_timeline(selected_user, df)
        if daily_timeline is not None and not daily_timeline.empty:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline["date"], daily_timeline["message"], color="black")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        else:
            st.warning("No daily timeline data available.")

        # Activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            if busy_day is not None and not busy_day.empty:
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            else:
                st.warning("No data for busy day analysis.")

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            if busy_month is not None and not busy_month.empty:
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            else:
                st.warning("No data for busy month analysis.")

        # Create period column for heatmap
        df["hour"] = df["message_date"].dt.hour
        df["minute"] = df["message_date"].dt.minute

        period = []
        for hour in df["hour"]:
            if hour == 23:
                period.append(f"{hour}-00")
            elif hour == 0:
                period.append("00-1")
            else:
                period.append(f"{hour}-{hour + 1}")
        df["period"] = period

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        if user_heatmap is not None and user_heatmap.shape[0] > 0 and user_heatmap.shape[1] > 0:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Not enough data to generate heatmap.")

        # Busiest users (Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            col1, col2 = st.columns(2)

            with col1:
                if x is not None and not x.empty:
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values, color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                else:
                    st.warning("No data for most busy users.")

            with col2:
                if new_df is not None and not new_df.empty:
                    st.dataframe(new_df)
                else:
                    st.warning("No user data to display.")

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        if df_wc is not None:
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.warning("No words to generate WordCloud.")

        # Most common words
        most_common_list = helper.most_common_words(selected_user, df)
        if most_common_list is not None and len(most_common_list) > 0:
            most_common_df = pd.DataFrame(most_common_list, columns=['word', 'count'])
            fig, ax = plt.subplots()
            ax.barh(most_common_df['word'], most_common_df['count'])
            plt.xticks(rotation='vertical')
            st.title('Most common words')
            st.pyplot(fig)
        else:
            st.write("No words to display.")

        # Emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        if emoji_df is not None and not emoji_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df.iloc[:, 1].head(), labels=emoji_df.iloc[:, 0].head(), autopct="%0.2f")
                st.pyplot(fig)
        else:
            st.warning("No emojis found in this chat.")
