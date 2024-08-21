import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.title("CSV Data Plotter")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Display the dataframe
        st.write("Data from the CSV file:")
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

if __name__ == "__main__":
    main()
