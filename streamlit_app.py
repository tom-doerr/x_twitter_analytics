import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from glob import glob
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_newest_csv(directory):
    csv_files = glob(os.path.join(directory, '*.csv'))
    if not csv_files:
        return None
    return max(csv_files, key=os.path.getmtime)

def calculate_engagement_rate(row):
    try:
        total_interactions = sum(row.get(col, 0) for col in ['likes', 'comments', 'shares'])
        impressions = row.get('impressions', 0)
        if impressions > 0:
            return (total_interactions / impressions) * 100
        else:
            logger.warning("Impressions value is 0 or not present. Returning 0 for engagement rate.")
            return 0
    except Exception as e:
        logger.error(f"Error calculating engagement rate: {e}")
        return 0

def main():
    st.title("CSV Data Plotter")

    csv_dir = 'csv_files'
    newest_csv = get_newest_csv(csv_dir)

    if newest_csv:
        try:
            # Read the CSV file
            df = pd.read_csv(newest_csv)
            
            # Convert 'Date' column to datetime if it exists
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
            
            # Calculate engagement rate
            df['engagement_rate'] = df.apply(calculate_engagement_rate, axis=1)
            
            # Plot engagement rate over time if 'Date' column exists
            if 'Date' in df.columns:
                st.subheader("Engagement Rate Over Time")
                fig_engagement, ax_engagement = plt.subplots(figsize=(10, 6))
                sns.lineplot(data=df, x='Date', y='engagement_rate', ax=ax_engagement)
                plt.xticks(rotation=45)
                ax_engagement.set_xlabel('Date')
                ax_engagement.set_ylabel('Engagement Rate (%)')
                ax_engagement.set_title('Engagement Rate Over Time')
                st.pyplot(fig_engagement)

            # Display summary statistics
            st.subheader("Summary Statistics")
            st.dataframe(df.describe())

            # Display key metrics
            st.subheader("Key Metrics")
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Impressions", f"{df['impressions'].mean():.0f}" if 'impressions' in df.columns else "N/A")
            col2.metric("Likes", f"{df['likes'].mean():.0f}" if 'likes' in df.columns else "N/A")
            col3.metric("Engagements", f"{df['engagements'].mean():.0f}" if 'engagements' in df.columns else "N/A")
            col4.metric("Bookmarks", f"{df['bookmarks'].mean():.0f}" if 'bookmarks' in df.columns else "N/A")
            col5.metric("Share", f"{df['share'].mean():.0f}" if 'share' in df.columns else "N/A")

            # Select columns for plotting
            st.subheader("Select columns for custom plotting")
            numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
            date_columns = df.select_dtypes(include=['datetime64']).columns
            x_column = st.selectbox("Select the X-axis column", list(date_columns) + list(numeric_columns))
            y_column = st.selectbox("Select the Y-axis column", numeric_columns)

            # Create the custom plot
            fig_custom, ax_custom = plt.subplots(figsize=(10, 6))
            
            if x_column in date_columns:
                sns.lineplot(data=df, x=x_column, y=y_column, ax=ax_custom)
                plt.xticks(rotation=45)
            else:
                sns.scatterplot(data=df, x=x_column, y=y_column, ax=ax_custom)
            
            ax_custom.set_xlabel(x_column)
            ax_custom.set_ylabel(y_column)
            ax_custom.set_title(f"{y_column} vs {x_column}")

            # Display the custom plot
            st.pyplot(fig_custom)

            # Display the dataframe
            st.subheader("Raw Data")
            st.write(f"Data from the newest CSV file: {os.path.basename(newest_csv)}")
            st.dataframe(df)

        except Exception as e:
            st.error(f"An error occurred while processing the CSV file: {e}")
            logger.error(f"Error processing CSV file: {e}")

    else:
        st.error("No CSV files found in the 'csv_files' directory.")

if __name__ == "__main__":
    main()
