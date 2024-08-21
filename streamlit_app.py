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

def import_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully imported CSV file: {file_path}")
        log_df_info(df, "Imported DataFrame")
        return df
    except Exception as e:
        logger.error(f"Error importing CSV file: {e}")
        return None

def calculate_engagement_rate(row):
    try:
        likes = row.get('Likes', 0)
        comments = row.get('Replies', 0)
        shares = row.get('Reposts', 0)
        bookmarks = row.get('Bookmarks', 0)  # Added bookmarks
        total_interactions = likes + comments + shares + bookmarks
        impressions = row.get('Impressions', 0)
        
        total_interactions = float(total_interactions) if pd.notnull(total_interactions) else 0
        impressions = float(impressions) if pd.notnull(impressions) else 0
        
        if impressions > 0:
            engagement_rate = (total_interactions / impressions) * 100
            return engagement_rate
        else:
            return 0
    except Exception as e:
        logger.error(f"Error calculating engagement rate: {e}")
        return None

def main():
    st.title("CSV Data Plotter")
    logger.info("Starting CSV Data Plotter application")

    csv_dir = 'csv_files'
    newest_csv = get_newest_csv(csv_dir)

    if newest_csv:
        try:
            df = import_csv(newest_csv)
            if df is not None:
                st.subheader("Imported Data")
                st.dataframe(df)

                if 'Date' in df.columns:
                    logger.info("Converting 'Date' column to datetime")
                    df['Date'] = pd.to_datetime(df['Date'])
                    logger.debug(f"Date column after conversion:\n{df['Date'].head()}")
                
                logger.info("Calculating engagement rate for all rows")
                df['engagement_rate'] = df.apply(calculate_engagement_rate, axis=1)
                log_df_info(df, "DataFrame after calculating engagement rate")

                # Plot engagement rates
                st.subheader("Engagement Rates Over Time")
                fig = px.line(df, x='Date', y='engagement_rate', title='Engagement Rate Over Time')
                st.plotly_chart(fig)

                # Display average engagement rate
                avg_engagement_rate = df['engagement_rate'].mean()
                st.metric("Average Engagement Rate", f"{avg_engagement_rate:.2f}%")

                # Interactive plot with selectable X and Y axes
                st.subheader("Interactive Plot")
                x_axis = st.selectbox("Select X-axis", options=df.columns)
                y_axis = st.selectbox("Select Y-axis", options=df.columns)
                
                fig = px.scatter(df, x=x_axis, y=y_axis, title=f'{y_axis} vs {x_axis}')
                st.plotly_chart(fig)

        except Exception as e:
            st.error(f"An error occurred while processing the CSV file: {e}")
            logger.error(f"Error processing CSV file: {e}", exc_info=True)
    else:
        st.error("No CSV files found in the 'csv_files' directory.")

if __name__ == "__main__":
    main()
