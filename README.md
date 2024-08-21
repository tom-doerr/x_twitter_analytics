# Twitter Analytics Visualizer

## Overview
This project is a Streamlit application that visualizes Twitter analytics data. It processes CSV files exported from the Twitter Analytics Account Overview page and provides interactive plots to analyze engagement rates and other metrics.

## Features
- Automatically imports the most recent CSV file from the `csv_files` directory
- Calculates engagement rates based on likes, replies, reposts, bookmarks, and impressions
- Provides an interactive plot where users can select X and Y axes for data exploration
- Displays the imported data in a table format

## Usage
1. Place your Twitter Analytics CSV file(s) in the `csv_files` directory
2. Run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```
3. Open the provided URL in your web browser
4. Use the interactive plot to explore your Twitter analytics data

## Data Format
The application expects CSV files with the following columns:
- Date
- Likes
- Replies
- Reposts
- Bookmarks
- Impressions

Additional columns may be present and can be used in the interactive plot.

## Contributing
Contributions to improve the application are welcome. Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
