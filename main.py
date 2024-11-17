import pandas as pd
import streamlit as st
from data_processing import Data_processing
from visualization import Visualization
from classification import Classification

# Example data to display on the main page
example_data = pd.DataFrame({
    'Date': ['11-01-2024', '11-02-2024', '11-03-2024'],
    'Description': ['Groceries', 'Taxi fare', 'Salary'],
    'Amount': [100, 200, 12000],
    'Type': ['Expense', 'Expense', 'Income']
})

data = Data_processing()
classifier = Classification()

tab1, tab2, tab3 ,tab4= st.tabs(["Data Entry", "Categorise Transactions","Data Display","Data Visualization"])

# Page Navigation
with tab1:
    main_page = st.selectbox(
        "Select an option",
        ["Upload Data (CSV/XLSX)", "Manual Data Entry"]
    )

    # Page 1: Bulk Upload Data in CSV or Excel Format
    if main_page == "Upload Data (CSV/XLSX)":
        st.title("Upload Data (CSV or XLSX Format)")
        st.subheader("Upload Data")
        st.info("Please upload your data in a tabular format (CSV or XLSX). The file should contain the following columns:\n"
                "- **Date**: The date of the transaction (e.g., 11-03-2024)\n"
                "- **Description**: A brief description of the transaction (e.g., Groceries, Taxi fare)\n"
                "- **Amount**: The amount spent or earned (e.g., 50)")

        st.write("Example Data:")
        st.table(example_data)

        # File uploader allowing multiple files to be uploaded
        files = st.file_uploader("Upload your files", type=["csv", "xlsx"], accept_multiple_files=True)

        if files:
            data.read_files(files)

            # Display a preview of the uploaded files (without concatenation)
            for i, df in enumerate(data.all_data_files):
                st.write(f"Preview of file {i + 1}:")
                st.write(df.head())

            # Combine the files when the submit button is clicked
            if st.button("Submit and Combine Files"):
                data.combine_uploaded_files()
                st.success("Files combined successfully!")

    # Page 2: Manual Data Entry
    elif main_page == "Manual Data Entry":
        st.title("Manual Data Entry")
        st.info("Enter individual transaction details below.")

        # Input fields for a single transaction entry
        date_str = st.text_input("Enter Date (dd-mm-yyyy)", value=pd.to_datetime('today').strftime('%d-%m-%Y'))
        description = st.text_input("Description")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        transaction_type = st.selectbox("Select Type", options=["Expense", "Income"])

        # Add entry to data storage
        if st.button("Add Transaction"):
            data.add_manual_entry(date_str, description, amount, transaction_type)
            st.write("Current Manual Entries:")
            data.combine_manual_entries()
            # Display manual data without the 'Year' column
            st.write(st.session_state.manual_data)
            st.success("Transaction added successfully!")

        if st.button("Combine Manual and Uploaded Data"):
            data.combine_manual_and_uploaded()
with tab2:
    st.title("Categorize Transactions")
    st.markdown("### Current Categories:")
    st.markdown("\n".join([f"- **{category}**" for category in classifier.categories]))

    # Input field for adding new categories
    new_category = st.text_input("Add a New Category")

    # Button to add the category
    if st.button("Add Category"):
        if new_category:
            classifier.add_category(new_category)
            st.success(f"Category '{new_category}' added successfully!")
        else:
            st.warning("Please enter a category name to add.")

    # Categorize transactions if data is available
    current_data = data.current_data()
    if st.button("Categorise transactions") and not current_data.empty:
        st.write("Data before categorization:")
        # Display data without the 'Year' column
        st.write(current_data)

        # Perform categorization
        current_data = classifier.categorize_transactions(current_data)
        st.write("Data after categorization:")
        # Display categorized data without the 'Year' column
        st.write(current_data)
        st.success("Transactions categorized successfully!")

    
with tab3:
    st.title("View Data")
    st.write("Current Data:")
    # Display combined data without the 'Year' column
    st.write(data.current_data())


with tab4:
    view_option = st.radio("Select View Type", ["Yearly", "Monthly"])
    st.title("Data Visualization")
    graph = Visualization()

    # Get the processed data and ensure Date is in datetime format
    current_data = data.current_data()

    # Ensure 'Date' is in datetime format, handling errors
    current_data['Date'] = pd.to_datetime(current_data['Date'], errors='coerce')

    # Check if the 'Date' column is successfully converted
    st.write("Data types:", current_data.dtypes)  # Verify Date type

    if view_option == "Yearly":
        # Extract unique years from the Date column
        years = sorted(current_data['Date'].dt.year.dropna().unique())

        if years:
            selected_year = st.selectbox("Select Year", years)
            graph.display_yearly_expenses(current_data, selected_year)
        else:
            st.warning("No valid date data available for selection.")

    elif view_option == "Monthly":
        # Extract unique years and months from the Date column
        years = sorted(current_data['Date'].dt.year.dropna().unique())

        if years:
            selected_year = st.selectbox("Select Year", years)

            months = [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]
            selected_month = st.selectbox("Select Month", months)

            # Display the monthly expenses based on selected year and month
            graph.display_monthly_expenses(current_data, selected_year, selected_month)
        else:
            st.warning("No valid date data available for selection.")

