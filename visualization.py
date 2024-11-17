import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

class Visualization:
    def __init__(self):
        pass

    def display_monthly_expenses(self, data, selected_year, selected_month):
        # Filter data for the selected year and month
        data['Month'] = data['Date'].dt.to_period('M')
        data['Year'] = data['Date'].dt.year

        # Filter by selected year and month
        monthly_expenses = data[(data['Year'] == selected_year) & (data['Month'] == selected_month)]

        # Filter data to include only expenses
        expenses = monthly_expenses[monthly_expenses['Type'] == 'Expense']

        # Group data by month and sum the Amounts
        category_expenses = expenses.groupby('Month')['Amount'].sum().reset_index()
        if category_expenses.empty:
            st.warning(f"No expenses found for {selected_month} {selected_year}")
        else:
            # Plot the expenses for each category
            plt.figure(figsize=(10, 6))
            plt.bar(category_expenses['Category'], category_expenses['Amount'], color='skyblue')
            plt.title(f'Monthly Expenses for {selected_month} {selected_year}')
            plt.xlabel('Category')
            plt.ylabel('Amount')
            plt.xticks(rotation=45)  # Rotate x labels for better readability
            st.pyplot(plt)

    def display_yearly_expenses(self, data, selected_year):
        # Ensure 'Date' is in datetime format
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

        # Extract year and month from the 'Date' column
        data['Year'] = data['Date'].dt.year
        data['Month'] = data['Date'].dt.month_name()

        # Filter data for the selected year and include only expenses
        expenses = data[(data['Type'] == 'Expense') & (data['Year'] == selected_year)]

        # Group by month and category, then sum the Amounts
        monthly_category_expenses = expenses.groupby(['Month', 'Category'])['Amount'].sum().reset_index()

        # Ensure the months are in the correct order
        month_order = [
            'January', 'February', 'March', 'April', 'May', 'June', 
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        monthly_category_expenses['Month'] = pd.Categorical(monthly_category_expenses['Month'], categories=month_order, ordered=True)
        monthly_category_expenses = monthly_category_expenses.sort_values('Month')

        # Pivot the data to have categories as columns
        pivot_expenses = monthly_category_expenses.pivot(index='Month', columns='Category', values='Amount').fillna(0)

        # Plot the yearly expenses for each category each month as a multi-bar chart
        ax = pivot_expenses.plot(kind='bar', figsize=(12, 8), width=0.8, stacked=False)
        plt.title(f'Yearly Expenses for {selected_year} by Category Each Month')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.xticks(rotation=45)
        plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(plt)