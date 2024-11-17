import pandas as pd
import streamlit as st

class Data_processing:
    def __init__(self):
        self.required_columns = ['Date', 'Description', 'Amount','Type']
        
        # Initialize session state if not already initialized
        if 'combined_data' not in st.session_state:
            st.session_state.combined_data = pd.DataFrame(columns=self.required_columns)
        if 'manual_data' not in st.session_state:
            st.session_state.manual_data = pd.DataFrame(columns=self.required_columns)
        
        self.all_data_files = []
    def data_clean(self, data1):
        """Cleans the 'Amount' column transactions."""
        data1['Amount'] = data1['Amount'].astype(str).str.replace(',', '').str.replace('Rs', '').str.replace(' ', '')
        data1['Amount'] = pd.to_numeric(data1['Amount'], errors='coerce')
        data1['Date'] = data1['Date'].astype(str)
        data1['Date'] = pd.to_datetime(data1['Date'].str.split(' ').str[0], errors="coerce",dayfirst=True).dt.strftime('%d-%m-%Y')
        return data1
    def read_files(self, files):
        """Reads the uploaded files and ensures that only required columns are extracted"""
        if files:
            for file in files:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file, usecols=self.required_columns)
                    
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file, usecols=self.required_columns)
                    
                df = self.data_clean(df)
                self.all_data_files.append(df)

    def combine_uploaded_files(self):
        """Combines all uploaded files into one DataFrame and updates session state."""
        if self.all_data_files:
            combined_data = pd.concat(self.all_data_files, ignore_index=True)
            st.session_state.combined_data = combined_data
        else:
            st.warning("No files have been uploaded to combine.")

    def add_manual_entry(self, date, description, amount,transaction_type):
        """Adds a manual entry to the manual data and updates session state."""
        new_entry = pd.DataFrame([[date, description, amount,transaction_type]], columns=self.required_columns)
        st.session_state.manual_data = pd.concat([st.session_state.manual_data, new_entry], ignore_index=True)

    def combine_manual_entries(self):
        """Combines all manual entries into one DataFrame and updates session state."""
        if not st.session_state.manual_data.empty:
            combined_manual_data = st.session_state.manual_data
            st.session_state.manual_data = combined_manual_data
        else:
            st.warning("No manual entries to combine.")

    def combine_manual_and_uploaded(self):
        """Combines manual data with the uploaded files data."""
        if not st.session_state.manual_data.empty:
            st.session_state.combined_data = pd.concat(
                [st.session_state.combined_data, st.session_state.manual_data], ignore_index=True
            )
            # Reset manual data after combining
            st.session_state.manual_data = pd.DataFrame(columns=self.required_columns)
            st.success("Manual entries combined successfully with uploaded data!")
        else:
            st.warning("No manual entries to combine.")

    def current_data(self):
        """Returns the combined data from session state."""
        st.session_state.combined_data['Date'] = pd.to_datetime(st.session_state.combined_data['Date'], format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
        return st.session_state.combined_data
