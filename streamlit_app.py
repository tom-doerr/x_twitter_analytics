import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob

def get_newest_csv(directory):
    csv_files = glob(os.path.join(directory, '*.csv'))
    if not csv_files:
        return None
    return max(csv_files, key=os.path.getmtime)

def main():
    st.title("CSV Data Plotter")

    csv_dir = 'csv_files'
    newest_csv = get_newest_csv(csv_dir)

    if newest_csv:
        # Read the CSV file
        df = pd.read_csv(newest_csv)
        
        # Display the dataframe
        st.write(f"Data from the newest CSV file: {os.path.basename(newest_csv)}")
        st.write(df)

        # Select columns for plotting
        st.subheader("Select columns for plotting")
        x_column = st.selectbox("Select the X-axis column", df.columns)
        y_column = st.selectbox("Select the Y-axis column", df.columns)

        # Create the plot
        fig, ax = plt.subplots()
        ax.scatter(df[x_column], df[y_column])
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"{y_column} vs {x_column}")

        # Display the plot
        st.pyplot(fig)
    else:
        st.error("No CSV files found in the 'csv_files' directory.")

if __name__ == "__main__":
    main()
