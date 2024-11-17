from transformers import pipeline
import torch
import streamlit as st
class Classification:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli', device=self.device)
        self.categories = ["Groceries", "Food", "Transport", "Entertainment", "Utilities","Beverages", "Miscellaneous"]
    def add_category(self, new_category):
        # Add a new category if it’s not already in the list
        if new_category not in self.categories:
            self.categories.append(new_category)
    def get_category(self, description):
        # Classify a single transaction description using the zero-shot classifier
        if not description.strip():  # Skip empty or whitespace-only descriptions
            return "Uncategorized"
        
        try:
            result = self.classifier(description, candidate_labels=self.categories)
            return result['labels'][0] if 'labels' in result else "Uncategorized"
        except Exception as e:
            # In case of any exception, return 'Uncategorized'
            return "Uncategorized"

    def categorize_transactions(self, data, batch_size=5):
        progress_bar = st.progress(0)
        total_rows = len(data)
        data['Category'] = None
        data['Description'] = data['Description'].fillna('').astype(str)

        for start in range(0, total_rows, batch_size):
            end = start + batch_size
            batch_descriptions = data['Description'].iloc[start:end].tolist()

            # Remove empty or whitespace-only descriptions from the batch
            batch_descriptions = [desc for desc in batch_descriptions if desc.strip()]

            if batch_descriptions:  # Ensure non-empty batch
                try:
                    results = self.classifier(batch_descriptions, candidate_labels=self.categories)

                    for i, result in enumerate(results):
                        data.at[start + i, 'Category'] = result['labels'][0] if 'labels' in result else "Uncategorized"

                except Exception as e:
                    # Log or handle classifier errors
                    st.error(f"Error classifying batch {start}-{end}: {str(e)}")
            
            progress_bar.progress(min((end) / total_rows, 1.0))

        return data