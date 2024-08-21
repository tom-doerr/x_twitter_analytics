import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from glob import glob
import logging
import sys
import plotly.express as px

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add a stream handler to output logs to Streamlit
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def log_df_info(df, message):
    logger.debug(f"{message}\nShape: {df.shape}\nColumns: {df.columns.tolist()}\nData types:\n{df.dtypes}")
    logger.debug(f"First few rows:\n{df.head().to_string()}")
    logger.debug(f"Summary statistics:\n{df.describe().to_string()}")

def get_newest_csv(directory):
    logger.debug(f"Searching for CSV files in directory: {directory}")
    csv_files = glob(os.path.join(directory, '*.csv'))
    logger.debug(f"Found CSV files: {csv_files}")
    if not csv_files:
        logger.warning("No CSV files found in the directory.")
        return None
    newest_file = max(csv_files, key=os.path.getmtime)
    logger.info(f"Newest CSV file: {newest_file}")
    return newest_file

def calculate_engagement_rate(row):
    try:
        logger.debug(f"Calculating engagement rate for row: {row}")
        total_interactions = sum(row.get(col, 0) for col in ['likes', 'comments', 'shares'])
        logger.debug(f"Total interactions: {total_interactions}")
        impressions = row.get('impressions', 0)
        logger.debug(f"Impressions: {impressions}")
        if impressions and impressions > 0:
            engagement_rate = (total_interactions / impressions) * 100
            logger.debug(f"Calculated engagement rate: {engagement_rate}")
            return engagement_rate
        else:
            logger.warning(f"Impressions value is 0, None, or not present. Row data: {row}")
            return None  # Return None instead of 0
    except Exception as e:
        logger.error(f"Error calculating engagement rate: {e}", exc_info=True)
        return None  # Return None in case of any error

def main():
    st.title("CSV Data Plotter")
    logger.info("Starting CSV Data Plotter application")

    csv_dir = 'csv_files'
    newest_csv = get_newest_csv(csv_dir)

    if newest_csv:
        try:
            logger.info(f"Reading CSV file: {newest_csv}")
            df = pd.read_csv(newest_csv)
            log_df_info(df, "Initial DataFrame")
            
            if 'Date' in df.columns:
                logger.info("Converting 'Date' column to datetime")
                df['Date'] = pd.to_datetime(df['Date'])
                logger.debug(f"Date column after conversion:\n{df['Date'].head()}")
            
            logger.info("Calculating engagement rate")
            df['engagement_rate'] = df.apply(calculate_engagement_rate, axis=1)
            df['engagement_rate'] = df['engagement_rate'].fillna(0)  # Replace None values with 0
            log_df_info(df, "DataFrame after calculating engagement rate")
            
            # Log the number of rows where engagement rate couldn't be calculated
            null_engagement_count = df['engagement_rate'].isnull().sum()
            logger.warning(f"Number of rows where engagement rate couldn't be calculated: {null_engagement_count}")
            
            # Plot engagement rate over time if 'Date' column exists
            if 'Date' in df.columns:
                logger.info("Plotting engagement rate over time")
                st.subheader("Engagement Rate Over Time")
                fig_engagement, ax_engagement = plt.subplots(figsize=(10, 6))
                sns.lineplot(data=df, x='Date', y='engagement_rate', ax=ax_engagement)
                plt.xticks(rotation=45)
                ax_engagement.set_xlabel('Date')
                ax_engagement.set_ylabel('Engagement Rate (%)')
                ax_engagement.set_title('Engagement Rate Over Time')
                st.pyplot(fig_engagement)
                logger.debug("Engagement rate plot created")

            # Create a table with engagements, impressions, and engagement rate for each day
            logger.info("Creating daily engagement table")
            daily_data = df.groupby('Date').agg({
                'engagements': 'sum',
                'impressions': 'sum',
                'engagement_rate': 'mean'
            }).reset_index()

            # Filter out entries with 0 values
            daily_data_filtered = daily_data[(daily_data['engagements'] != 0) & (daily_data['impressions'] != 0)]

            # Display the table
            st.subheader("Daily Engagement Data")
            st.dataframe(daily_data_filtered)

            # Plot the data using Plotly
            st.subheader("Daily Engagement Metrics")
            fig = px.line(daily_data_filtered, x='Date', y=['engagements', 'impressions', 'engagement_rate'],
                          labels={'value': 'Value', 'variable': 'Metric'},
                          title='Daily Engagement Metrics Over Time')
            st.plotly_chart(fig)

            # Display summary statistics
            logger.info("Displaying summary statistics")
            st.subheader("Summary Statistics")
            summary_stats = df.describe()
            st.dataframe(summary_stats)
            logger.debug(f"Summary statistics:\n{summary_stats.to_string()}")

            # Display key metrics
            logger.info("Displaying key metrics")
            st.subheader("Key Metrics")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            def safe_mean(column):
                if column in df.columns and not df[column].isnull().all():
                    mean_value = df[column].mean()
                    logger.debug(f"Mean value for {column}: {mean_value}")
                    return f"{mean_value:.0f}"
                else:
                    logger.warning(f"Column {column} not found or all values are null")
                    return "N/A"
            
            col1.metric("Impressions", safe_mean('impressions'))
            col2.metric("Likes", safe_mean('likes'))
            col3.metric("Engagements", safe_mean('engagements'))
            col4.metric("Bookmarks", safe_mean('bookmarks'))
            col5.metric("Share", safe_mean('share'))
            logger.debug("Key metrics displayed")

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
