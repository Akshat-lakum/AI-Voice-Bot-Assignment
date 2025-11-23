import streamlit as st
import sqlite3
import pandas as pd
import os

# Connect to DB
DB_PATH = os.path.join("data", "voice_bot.db")

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY id DESC", conn)
    conn.close()
    return df

st.title("📊 Voice Bot Analytics Dashboard")
st.markdown("Real-time monitoring of user interactions and bot performance.")

# Refresh button
if st.button('Refresh Data'):
    st.rerun()

# Load Data
try:
    df = load_data()
    
    if not df.empty:
        # Top Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Queries", len(df))
        col2.metric("Avg Response Time", f"{df['response_time'].mean():.2f} sec")
        col3.metric("Most Common Intent", df['intent'].mode()[0])

        st.divider()

        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Intent Distribution")
            st.bar_chart(df['intent'].value_counts())

        with col_chart2:
            st.subheader("Response Time History")
            st.line_chart(df['response_time'])

        # Recent Logs Table
        st.subheader("📝 Recent Conversations")
        st.dataframe(df[['timestamp', 'intent', 'user_text', 'bot_reply', 'response_time']])
    else:
        st.info("No interactions recorded yet. Go talk to the bot!")

except Exception as e:
    st.error(f"Could not load database. Make sure the bot has run at least once. Error: {e}")