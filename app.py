import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from data_processor import DataProcessor
from visualizations import Visualizations

# Page configuration
st.set_page_config(
    page_title="Video Game Sales Dashboard",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data processor and visualizations
@st.cache_data
def load_data():
    processor = DataProcessor()
    return processor.load_and_process_data()

def main():
    st.title("🎮 Video Game Sales Analytics Dashboard")
    st.markdown("---")
    
    # Load data
    try:
        df = load_data()
        viz = Visualizations(df)
        
        # Sidebar filters
        st.sidebar.header("🔍 Filters")
        
        # Year range filter
        year_range = st.sidebar.slider(
            "Select Year Range",
            min_value=int(df['Year'].min()),
            max_value=int(df['Year'].max()),
            value=(int(df['Year'].min()), int(df['Year'].max())),
            step=1
        )
        
        # Genre filter
        genres = ['All'] + sorted(df['Genre'].unique().tolist())
        selected_genre = st.sidebar.selectbox("Select Genre", genres)
        
        # Platform filter
        platforms = ['All'] + sorted(df['Platform'].unique().tolist())
        selected_platform = st.sidebar.selectbox("Select Platform", platforms)
        
        # Publisher filter
        top_publishers = df.groupby('Publisher')['Global_Sales'].sum().nlargest(20).index.tolist()
        publishers = ['All'] + sorted(top_publishers)
        selected_publisher = st.sidebar.selectbox("Select Publisher", publishers)
        
        # Apply filters
        filtered_df = df[
            (df['Year'] >= year_range[0]) & 
            (df['Year'] <= year_range[1])
        ]
        
        if selected_genre != 'All':
            filtered_df = filtered_df[filtered_df['Genre'] == selected_genre]
        
        if selected_platform != 'All':
            filtered_df = filtered_df[filtered_df['Platform'] == selected_platform]
            
        if selected_publisher != 'All':
            filtered_df = filtered_df[filtered_df['Publisher'] == selected_publisher]
        
        # Update visualizations with filtered data
        viz.update_data(filtered_df)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_games = len(filtered_df)
            st.metric("Total Games", f"{total_games:,}")
        
        with col2:
            total_sales = filtered_df['Global_Sales'].sum()
            st.metric("Total Sales", f"{total_sales:.2f}M")
        
        with col3:
            avg_sales = filtered_df['Global_Sales'].mean()
            st.metric("Average Sales", f"{avg_sales:.2f}M")
        
        with col4:
            top_game = filtered_df.loc[filtered_df['Global_Sales'].idxmax(), 'Name'] if not filtered_df.empty else "N/A"
            st.metric("Top Game", top_game)
        
        st.markdown("---")
        
        # Main dashboard tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Overview", 
            "🏆 Leaderboard", 
            "🎯 Genre Analysis", 
            "🖥️ Platform Analysis", 
            "🌍 Regional Analysis", 
            "📈 Trends"
        ])
        
        with tab1:
            st.header("Sales Overview")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Sales by Genre")
                fig_genre = viz.create_genre_pie_chart()
                st.plotly_chart(fig_genre, use_container_width=True)
            
            with col2:
                st.subheader("Sales by Platform")
                fig_platform = viz.create_platform_bar_chart()
                st.plotly_chart(fig_platform, use_container_width=True)
            
            st.subheader("Regional Sales Distribution")
            fig_regional = viz.create_regional_breakdown()
            st.plotly_chart(fig_regional, use_container_width=True)
        
        with tab2:
            st.header("🏆 Global Sales Leaderboard")
            
            # Top games table
            top_games = filtered_df.nlargest(20, 'Global_Sales')[
                ['Rank', 'Name', 'Platform', 'Year', 'Genre', 'Publisher', 'Global_Sales']
            ].reset_index(drop=True)
            
            st.dataframe(
                top_games,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Global_Sales": st.column_config.NumberColumn(
                        "Global Sales (M)",
                        format="%.2f"
                    ),
                    "Year": st.column_config.NumberColumn(
                        "Year",
                        format="%d"
                    )
                }
            )
            
            # Top games bar chart
            st.subheader("Top 15 Best-Selling Games")
            fig_top_games = viz.create_top_games_chart()
            st.plotly_chart(fig_top_games, use_container_width=True)
        
        with tab3:
            st.header("🎯 Genre Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Genre Sales Distribution")
                fig_genre_dist = viz.create_genre_distribution()
                st.plotly_chart(fig_genre_dist, use_container_width=True)
            
            with col2:
                st.subheader("Average Sales by Genre")
                fig_genre_avg = viz.create_genre_average_sales()
                st.plotly_chart(fig_genre_avg, use_container_width=True)
            
            st.subheader("Genre Popularity Over Time")
            fig_genre_time = viz.create_genre_timeline()
            st.plotly_chart(fig_genre_time, use_container_width=True)
        
        with tab4:
            st.header("🖥️ Platform Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Platform Market Share")
                fig_platform_share = viz.create_platform_market_share()
                st.plotly_chart(fig_platform_share, use_container_width=True)
            
            with col2:
                st.subheader("Games Count by Platform")
                fig_platform_count = viz.create_platform_game_count()
                st.plotly_chart(fig_platform_count, use_container_width=True)
            
            st.subheader("Platform Performance Over Time")
            fig_platform_time = viz.create_platform_timeline()
            st.plotly_chart(fig_platform_time, use_container_width=True)
        
        with tab5:
            st.header("🌍 Regional Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Regional Sales Comparison")
                fig_regional_comparison = viz.create_regional_comparison()
                st.plotly_chart(fig_regional_comparison, use_container_width=True)
            
            with col2:
                st.subheader("Regional Market Share")
                fig_regional_share = viz.create_regional_market_share()
                st.plotly_chart(fig_regional_share, use_container_width=True)
            
            st.subheader("Regional Preferences by Genre")
            fig_regional_genre = viz.create_regional_genre_preferences()
            st.plotly_chart(fig_regional_genre, use_container_width=True)
        
        with tab6:
            st.header("📈 Trends & Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Sales Trends Over Time")
                fig_yearly_trends = viz.create_yearly_sales_trends()
                st.plotly_chart(fig_yearly_trends, use_container_width=True)
            
            with col2:
                st.subheader("Publisher Performance")
                fig_publisher = viz.create_publisher_analysis()
                st.plotly_chart(fig_publisher, use_container_width=True)
            
            st.subheader("Game Releases Over Time")
            fig_releases = viz.create_game_releases_timeline()
            st.plotly_chart(fig_releases, use_container_width=True)
        
        # Additional insights section
        st.markdown("---")
        st.header("📋 Key Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Top Genre")
            top_genre = filtered_df.groupby('Genre')['Global_Sales'].sum().idxmax()
            top_genre_sales = filtered_df.groupby('Genre')['Global_Sales'].sum().max()
            st.info(f"**{top_genre}**\n\n{top_genre_sales:.2f}M in sales")
        
        with col2:
            st.subheader("Most Popular Platform")
            top_platform = filtered_df.groupby('Platform')['Global_Sales'].sum().idxmax()
            top_platform_sales = filtered_df.groupby('Platform')['Global_Sales'].sum().max()
            st.info(f"**{top_platform}**\n\n{top_platform_sales:.2f}M in sales")
        
        with col3:
            st.subheader("Leading Publisher")
            top_publisher_name = filtered_df.groupby('Publisher')['Global_Sales'].sum().idxmax()
            top_publisher_sales = filtered_df.groupby('Publisher')['Global_Sales'].sum().max()
            st.info(f"**{top_publisher_name}**\n\n{top_publisher_sales:.2f}M in sales")
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please ensure the CSV file is properly formatted and accessible.")

if __name__ == "__main__":
    main()
