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
    st.write("--- Calculating Engagement Rate ---")
    st.write(f"Processing row: {row}")
    
    try:
        # Step 1: Get engagements and impressions
        likes = row.get('Likes', 0)
        comments = row.get('Replies', 0)  # Assuming 'Replies' corresponds to comments
        shares = row.get('Reposts', 0)  # Assuming 'Reposts' corresponds to shares
        total_interactions = likes + comments + shares
        impressions = row.get('Impressions', 0)
        st.write(f"Raw values - Likes: {likes}, Comments: {comments}, Shares: {shares}, Total Interactions: {total_interactions}, Impressions: {impressions}")
        
        # Step 2: Convert to float and handle NaN
        total_interactions = float(total_interactions) if pd.notnull(total_interactions) else 0
        impressions = float(impressions) if pd.notnull(impressions) else 0
        st.write(f"Converted values - Total Interactions: {total_interactions}, Impressions: {impressions}")
        
        # Step 3: Check if impressions is greater than 0
        if impressions > 0:
            # Step 4: Calculate engagement rate
            engagement_rate = (total_interactions / impressions) * 100
            st.write(f"Calculated engagement rate: {engagement_rate:.2f}%")
            return engagement_rate
        else:
            st.warning(f"Impressions is 0 or not present. Engagement rate is 0.")
            st.write(f"Detailed breakdown - Likes: {likes}, Comments: {comments}, Shares: {shares}, Total Interactions: {total_interactions}, Impressions: {impressions}")
            return 0
    except Exception as e:
        st.error(f"Error calculating engagement rate: {e}")
        st.write(f"Error details - Row data: {row}")
        st.write(f"Error type: {type(e).__name__}")
        st.write(f"Error message: {str(e)}")
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
                st.success(f"Successfully imported CSV file: {os.path.basename(newest_csv)}")
                st.subheader("Imported Data")
                st.dataframe(df)

                if 'Date' in df.columns:
                    logger.info("Converting 'Date' column to datetime")
                    df['Date'] = pd.to_datetime(df['Date'])
                    logger.debug(f"Date column after conversion:\n{df['Date'].head()}")
                
                st.subheader("Calculating Engagement Rate for 3 Rows")
                for i, row in df.head(3).iterrows():
                    st.write(f"\nProcessing Row {i + 1}")
                    engagement_rate = calculate_engagement_rate(row)
                    if engagement_rate > 0:
                        st.success(f"Row {i + 1} Engagement Rate: {engagement_rate:.2f}%")
                    elif engagement_rate == 0:
                        st.warning(f"Row {i + 1}: Engagement rate is 0 (Impressions were 0 or not present)")
                    else:
                        st.error(f"Row {i + 1}: Unable to calculate engagement rate")
                
                logger.info("Calculating engagement rate for all rows")
                df['engagement_rate'] = df.apply(calculate_engagement_rate, axis=1)
                log_df_info(df, "DataFrame after calculating engagement rate")

                # Add more processing and visualization code here

        except Exception as e:
            st.error(f"An error occurred while processing the CSV file: {e}")
            logger.error(f"Error processing CSV file: {e}", exc_info=True)
    else:
        st.error("No CSV files found in the 'csv_files' directory.")

if __name__ == "__main__":
    main()
