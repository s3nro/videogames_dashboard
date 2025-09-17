import pandas as pd
import numpy as np
import streamlit as st

class DataProcessor:
    def __init__(self):
        self.csv_path = "attached_assets/video_games_sales_1758117847275.csv"
    
    def load_and_process_data(self):
        """Load and clean the video game sales data"""
        try:
            # Load the CSV file
            df = pd.read_csv(self.csv_path)
            
            # Clean and process the data
            df = self.clean_data(df)
            
            return df
            
        except FileNotFoundError:
            st.error(f"CSV file not found: {self.csv_path}")
            raise
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            raise
    
    def clean_data(self, df):
        """Clean and preprocess the data"""
        # Remove rows with missing critical data
        df = df.dropna(subset=['Name', 'Global_Sales'])
        
        # Handle missing years - set to 0 for unknown years
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df['Year'] = df['Year'].fillna(0).astype(int)
        
        # Filter out invalid years (keep only realistic game release years)
        df = df[df['Year'] >= 1980]
        
        # Fill missing values for sales columns with 0
        sales_columns = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
        for col in sales_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0)
        
        # Clean string columns
        string_columns = ['Name', 'Platform', 'Genre', 'Publisher']
        for col in string_columns:
            df[col] = df[col].fillna('Unknown').astype(str).str.strip()
        
        # Remove games with 0 global sales
        df = df[df['Global_Sales'] > 0]
        
        # Ensure Rank is numeric
        df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce')
        
        # Sort by global sales descending
        df = df.sort_values('Global_Sales', ascending=False).reset_index(drop=True)
        
        # Add derived columns
        df = self.add_derived_columns(df)
        
        return df
    
    def add_derived_columns(self, df):
        """Add calculated columns for analysis"""
        # Add decade column
        df['Decade'] = (df['Year'] // 10) * 10
        df['Decade'] = df['Decade'].astype(str) + 's'
        df.loc[df['Year'] == 0, 'Decade'] = 'Unknown'
        
        # Add sales rank within genre
        df['Genre_Rank'] = df.groupby('Genre')['Global_Sales'].rank(method='dense', ascending=False)
        
        # Add sales rank within platform
        df['Platform_Rank'] = df.groupby('Platform')['Global_Sales'].rank(method='dense', ascending=False)
        
        # Add regional dominance (which region contributed most to sales)
        regional_cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
        df['Dominant_Region'] = df[regional_cols].idxmax(axis=1)
        df['Dominant_Region'] = df['Dominant_Region'].map({
            'NA_Sales': 'North America',
            'EU_Sales': 'Europe', 
            'JP_Sales': 'Japan',
            'Other_Sales': 'Other'
        })
        
        # Add percentage of global sales by region
        for region in regional_cols:
            region_pct = region.replace('_Sales', '_Percentage')
            df[region_pct] = (df[region] / df['Global_Sales'] * 100).round(2)
        
        return df
    
    def get_data_summary(self, df):
        """Get summary statistics of the dataset"""
        summary = {
            'total_games': len(df),
            'total_sales': df['Global_Sales'].sum(),
            'years_range': (df['Year'].min(), df['Year'].max()),
            'unique_platforms': df['Platform'].nunique(),
            'unique_genres': df['Genre'].nunique(),
            'unique_publishers': df['Publisher'].nunique(),
            'top_game': df.loc[df['Global_Sales'].idxmax(), 'Name'],
            'top_sales': df['Global_Sales'].max()
        }
        return summary
