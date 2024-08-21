import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from glob import glob

def get_newest_csv(directory):
    csv_files = glob(os.path.join(directory, '*.csv'))
    if not csv_files:
        return None
    return max(csv_files, key=os.path.getmtime)

def calculate_engagement_rate(row):
    total_interactions = row['likes'] + row['comments'] + row['shares']
    return (total_interactions / row['impressions']) * 100 if row['impressions'] > 0 else 0

def main():
    st.title("CSV Data Plotter")

    csv_dir = 'csv_files'
    newest_csv = get_newest_csv(csv_dir)

    if newest_csv:
        # Read the CSV file
        df = pd.read_csv(newest_csv)
        
        # Convert 'Date' column to datetime if it exists
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        
        # Calculate engagement rate
        df['engagement_rate'] = df.apply(calculate_engagement_rate, axis=1)
        
        # Plot engagement rate over time
        st.subheader("Engagement Rate Over Time")
        fig_engagement, ax_engagement = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=df, x='Date', y='engagement_rate', ax=ax_engagement)
        plt.xticks(rotation=45)
        ax_engagement.set_xlabel('Date')
        ax_engagement.set_ylabel('Engagement Rate (%)')
        ax_engagement.set_title('Engagement Rate Over Time')
        st.pyplot(fig_engagement)

        # Select columns for plotting
        st.subheader("Select columns for custom plotting")
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        x_column = st.selectbox("Select the X-axis column", ['Date'] + list(numeric_columns))
        y_column = st.selectbox("Select the Y-axis column", numeric_columns)

        # Create the custom plot
        fig_custom, ax_custom = plt.subplots(figsize=(10, 6))
        
        if x_column == 'Date':
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
        st.write(df)

        # Display summary statistics
        st.subheader("Summary Statistics")
        st.write(df.describe())

    else:
        st.error("No CSV files found in the 'csv_files' directory.")

if __name__ == "__main__":
    main()
