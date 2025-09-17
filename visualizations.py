import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class Visualizations:
    def __init__(self, df):
        self.df = df
        self.color_palette = px.colors.qualitative.Set3
    
    def update_data(self, new_df):
        """Update the dataframe for visualizations"""
        self.df = new_df
    
    def create_genre_pie_chart(self):
        """Create pie chart for genre sales distribution"""
        genre_sales = self.df.groupby('Genre')['Global_Sales'].sum().reset_index()
        genre_sales = genre_sales.sort_values('Global_Sales', ascending=False)
        
        fig = px.pie(
            genre_sales, 
            values='Global_Sales', 
            names='Genre',
            title='Global Sales Distribution by Genre',
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True, height=400)
        
        return fig
    
    def create_platform_bar_chart(self):
        """Create bar chart for top platforms by sales"""
        platform_sales = self.df.groupby('Platform')['Global_Sales'].sum().reset_index()
        platform_sales = platform_sales.sort_values('Global_Sales', ascending=False).head(15)
        
        fig = px.bar(
            platform_sales,
            x='Global_Sales',
            y='Platform',
            orientation='h',
            title='Top 15 Platforms by Global Sales',
            color='Global_Sales',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            xaxis_title='Global Sales (Millions)',
            yaxis_title='Platform',
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def create_regional_breakdown(self):
        """Create stacked bar chart for regional sales breakdown"""
        regional_totals = {
            'North America': self.df['NA_Sales'].sum(),
            'Europe': self.df['EU_Sales'].sum(), 
            'Japan': self.df['JP_Sales'].sum(),
            'Other': self.df['Other_Sales'].sum()
        }
        
        regions = list(regional_totals.keys())
        sales = list(regional_totals.values())
        
        fig = px.bar(
            x=regions,
            y=sales,
            title='Global Sales by Region',
            color=regions,
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_layout(
            xaxis_title='Region',
            yaxis_title='Sales (Millions)',
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_top_games_chart(self):
        """Create bar chart for top 15 games"""
        top_games = self.df.nlargest(15, 'Global_Sales')
        
        fig = px.bar(
            top_games,
            x='Global_Sales',
            y='Name',
            orientation='h',
            title='Top 15 Best-Selling Video Games',
            color='Global_Sales',
            color_continuous_scale='plasma',
            hover_data=['Platform', 'Year', 'Genre', 'Publisher']
        )
        
        fig.update_layout(
            xaxis_title='Global Sales (Millions)',
            yaxis_title='Game Title',
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def create_genre_distribution(self):
        """Create box plot for genre sales distribution"""
        fig = px.box(
            self.df,
            x='Genre',
            y='Global_Sales',
            title='Sales Distribution by Genre',
            color='Genre'
        )
        
        fig.update_layout(
            xaxis_title='Genre',
            yaxis_title='Global Sales (Millions)',
            height=400,
            xaxis_tickangle=45,
            showlegend=False
        )
        
        return fig
    
    def create_genre_average_sales(self):
        """Create bar chart for average sales by genre"""
        genre_avg = self.df.groupby('Genre')['Global_Sales'].mean().reset_index()
        genre_avg = genre_avg.sort_values('Global_Sales', ascending=False)
        
        fig = px.bar(
            genre_avg,
            x='Genre',
            y='Global_Sales',
            title='Average Sales by Genre',
            color='Global_Sales',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            xaxis_title='Genre',
            yaxis_title='Average Sales (Millions)',
            height=400,
            xaxis_tickangle=45
        )
        
        return fig
    
    def create_genre_timeline(self):
        """Create line chart for genre popularity over time"""
        # Filter for years after 1980 to avoid outliers
        filtered_df = self.df[self.df['Year'] >= 1980]
        
        genre_yearly = filtered_df.groupby(['Year', 'Genre'])['Global_Sales'].sum().reset_index()
        
        fig = px.line(
            genre_yearly,
            x='Year',
            y='Global_Sales',
            color='Genre',
            title='Genre Popularity Trends Over Time',
            line_group='Genre'
        )
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Total Sales (Millions)',
            height=400
        )
        
        return fig
    
    def create_platform_market_share(self):
        """Create treemap for platform market share"""
        platform_sales = self.df.groupby('Platform')['Global_Sales'].sum().reset_index()
        platform_sales = platform_sales.sort_values('Global_Sales', ascending=False).head(20)
        
        fig = px.treemap(
            platform_sales,
            path=['Platform'],
            values='Global_Sales',
            title='Platform Market Share (Top 20)',
            color='Global_Sales',
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    def create_platform_game_count(self):
        """Create bar chart for number of games by platform"""
        platform_count = self.df['Platform'].value_counts().reset_index()
        platform_count.columns = ['Platform', 'Game_Count']
        platform_count = platform_count.head(15)
        
        fig = px.bar(
            platform_count,
            x='Platform',
            y='Game_Count',
            title='Number of Games by Platform (Top 15)',
            color='Game_Count',
            color_continuous_scale='blues'
        )
        
        fig.update_layout(
            xaxis_title='Platform',
            yaxis_title='Number of Games',
            height=400,
            xaxis_tickangle=45
        )
        
        return fig
    
    def create_platform_timeline(self):
        """Create line chart for platform performance over time"""
        # Get top 10 platforms by total sales
        top_platforms = self.df.groupby('Platform')['Global_Sales'].sum().nlargest(10).index
        
        filtered_df = self.df[
            (self.df['Platform'].isin(top_platforms)) & 
            (self.df['Year'] >= 1980)
        ]
        
        platform_yearly = filtered_df.groupby(['Year', 'Platform'])['Global_Sales'].sum().reset_index()
        
        fig = px.line(
            platform_yearly,
            x='Year',
            y='Global_Sales',
            color='Platform',
            title='Top 10 Platforms Performance Over Time'
        )
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Total Sales (Millions)',
            height=400
        )
        
        return fig
    
    def create_regional_comparison(self):
        """Create grouped bar chart for regional sales comparison"""
        # Get top 10 games for regional comparison
        top_games = self.df.nlargest(10, 'Global_Sales')
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='North America',
            x=top_games['Name'],
            y=top_games['NA_Sales'],
        ))
        
        fig.add_trace(go.Bar(
            name='Europe',
            x=top_games['Name'],
            y=top_games['EU_Sales'],
        ))
        
        fig.add_trace(go.Bar(
            name='Japan',
            x=top_games['Name'],
            y=top_games['JP_Sales'],
        ))
        
        fig.add_trace(go.Bar(
            name='Other',
            x=top_games['Name'],
            y=top_games['Other_Sales'],
        ))
        
        fig.update_layout(
            title='Regional Sales Comparison (Top 10 Games)',
            xaxis_title='Game',
            yaxis_title='Sales (Millions)',
            barmode='group',
            height=400,
            xaxis_tickangle=45
        )
        
        return fig
    
    def create_regional_market_share(self):
        """Create pie chart for regional market share"""
        regional_totals = {
            'North America': self.df['NA_Sales'].sum(),
            'Europe': self.df['EU_Sales'].sum(),
            'Japan': self.df['JP_Sales'].sum(),
            'Other': self.df['Other_Sales'].sum()
        }
        
        regions = list(regional_totals.keys())
        sales = list(regional_totals.values())
        
        fig = px.pie(
            values=sales,
            names=regions,
            title='Global Market Share by Region',
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        return fig
    
    def create_regional_genre_preferences(self):
        """Create heatmap for regional genre preferences"""
        # Calculate genre sales by region
        genre_regional = self.df.groupby('Genre').agg({
            'NA_Sales': 'sum',
            'EU_Sales': 'sum', 
            'JP_Sales': 'sum',
            'Other_Sales': 'sum'
        }).reset_index()
        
        # Create heatmap data
        heatmap_data = genre_regional.set_index('Genre')
        heatmap_data.columns = ['North America', 'Europe', 'Japan', 'Other']
        
        fig = px.imshow(
            heatmap_data.T,
            title='Regional Genre Preferences Heatmap',
            color_continuous_scale='viridis',
            aspect='auto'
        )
        
        fig.update_layout(
            xaxis_title='Genre',
            yaxis_title='Region',
            height=400
        )
        
        return fig
    
    def create_yearly_sales_trends(self):
        """Create line chart for yearly sales trends"""
        yearly_sales = self.df[self.df['Year'] >= 1980].groupby('Year')['Global_Sales'].sum().reset_index()
        
        fig = px.line(
            yearly_sales,
            x='Year',
            y='Global_Sales',
            title='Global Video Game Sales Trends Over Time',
            markers=True
        )
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Total Sales (Millions)',
            height=400
        )
        
        return fig
    
    def create_publisher_analysis(self):
        """Create bar chart for top publishers"""
        publisher_sales = self.df.groupby('Publisher')['Global_Sales'].sum().reset_index()
        publisher_sales = publisher_sales.sort_values('Global_Sales', ascending=False).head(15)
        
        fig = px.bar(
            publisher_sales,
            x='Global_Sales',
            y='Publisher',
            orientation='h',
            title='Top 15 Publishers by Global Sales',
            color='Global_Sales',
            color_continuous_scale='plasma'
        )
        
        fig.update_layout(
            xaxis_title='Global Sales (Millions)',
            yaxis_title='Publisher',
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def create_game_releases_timeline(self):
        """Create bar chart for game releases over time"""
        releases_by_year = self.df[self.df['Year'] >= 1980]['Year'].value_counts().reset_index()
        releases_by_year.columns = ['Year', 'Number_of_Games']
        releases_by_year = releases_by_year.sort_values('Year')
        
        fig = px.bar(
            releases_by_year,
            x='Year',
            y='Number_of_Games',
            title='Number of Game Releases Over Time',
            color='Number_of_Games',
            color_continuous_scale='blues'
        )
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Number of Games Released',
            height=400
        )
        
        return fig
    
    def create_sales_evolution_analysis(self):
        """Create analysis comparing launch vs long-term performance"""
        # Since our dataset has single entries per game, we'll analyze patterns differently
        # We'll look at games with multiple platform releases as proxy for launch vs long-term
        
        reference_year = int(self.df['Year'].max())
        
        # Group games by name to find multi-platform releases
        game_analysis = []
        
        for game_name, game_group in self.df.groupby('Name'):
            if len(game_group) > 1:  # Multi-platform/version releases
                # Sort by year and sales
                sorted_releases = game_group.sort_values(['Year', 'Global_Sales'], ascending=[True, False])
                
                # First release (launch)
                launch_entry = sorted_releases.iloc[0]
                launch_sales = launch_entry['Global_Sales']
                launch_year = launch_entry['Year']
                
                # Later releases (long-term)
                later_releases = sorted_releases.iloc[1:]
                long_term_sales = later_releases['Global_Sales'].sum()
                
                # Calculate metrics
                total_sales = launch_sales + long_term_sales
                if total_sales > 0:
                    long_tail_ratio = long_term_sales / total_sales
                else:
                    long_tail_ratio = 0
                
                # Categorize performance pattern
                if long_tail_ratio > 0.6:
                    pattern = 'Long-term Success'
                elif long_tail_ratio > 0.3:
                    pattern = 'Balanced Performance'  
                else:
                    pattern = 'Front-loaded'
                
                game_analysis.append({
                    'Name': game_name,
                    'Launch_Sales': launch_sales,
                    'Long_term_Sales': long_term_sales,
                    'Total_Sales': total_sales,
                    'Long_tail_Ratio': long_tail_ratio,
                    'Pattern': pattern,
                    'Launch_Year': launch_year,
                    'Genre': launch_entry['Genre'],
                    'Publisher': launch_entry['Publisher']
                })
        
        if not game_analysis:
            # Fallback: analyze single-release games by sales terciles
            df_copy = self.df.copy()
            sales_terciles = df_copy['Global_Sales'].quantile([0.33, 0.67])
            
            df_copy['Performance_Pattern'] = df_copy['Global_Sales'].apply(
                lambda x: 'High Impact' if x > sales_terciles[0.67] else
                         'Moderate Impact' if x > sales_terciles[0.33] else
                         'Limited Impact'
            )
            
            fig = px.scatter(
                df_copy,
                x='Year',
                y='Global_Sales',
                color='Performance_Pattern',
                size='Global_Sales',
                title='Sales Impact Analysis (Single Release Games)',
                hover_data=['Name', 'Platform', 'Genre'],
                color_discrete_map={
                    'High Impact': '#2E8B57',
                    'Moderate Impact': '#FFD700',
                    'Limited Impact': '#FF6347'
                }
            )
        else:
            # Create DataFrame from analysis
            analysis_df = pd.DataFrame(game_analysis)
            
            fig = px.scatter(
                analysis_df,
                x='Launch_Sales',
                y='Long_term_Sales',
                color='Pattern',
                size='Total_Sales',
                title='Launch vs Long-term Sales Performance',
                hover_data=['Name', 'Genre', 'Long_tail_Ratio'],
                color_discrete_map={
                    'Front-loaded': '#FF6347',
                    'Balanced Performance': '#FFD700',
                    'Long-term Success': '#2E8B57'
                }
            )
            
            fig.update_layout(
                xaxis_title='Launch Sales (Millions)',
                yaxis_title='Long-term Sales (Millions)'
            )
        
        fig.update_layout(height=500)
        return fig
    
    def create_launch_vs_longterm_comparison(self):
        """Create comparison of games with sustained vs front-loaded success patterns"""
        # Find games with multiple releases to analyze launch vs long-term patterns
        
        pattern_analysis = []
        for game_name, game_group in self.df.groupby('Name'):
            if len(game_group) > 1:
                sorted_releases = game_group.sort_values(['Year', 'Global_Sales'], ascending=[True, False])
                
                launch_sales = sorted_releases.iloc[0]['Global_Sales']
                long_term_sales = sorted_releases.iloc[1:]['Global_Sales'].sum()
                total_sales = launch_sales + long_term_sales
                
                if total_sales > 0:
                    long_tail_ratio = long_term_sales / total_sales
                    
                    pattern_analysis.append({
                        'Name': game_name,
                        'Genre': sorted_releases.iloc[0]['Genre'],
                        'Launch_Sales': launch_sales,
                        'Long_term_Sales': long_term_sales,
                        'Long_tail_Ratio': long_tail_ratio,
                        'Total_Sales': total_sales
                    })
        
        if pattern_analysis:
            analysis_df = pd.DataFrame(pattern_analysis)
            
            # Analyze by genre
            genre_patterns = analysis_df.groupby('Genre').agg({
                'Long_tail_Ratio': 'mean',
                'Total_Sales': ['mean', 'count']
            }).round(3)
            
            genre_patterns.columns = ['Avg_Long_tail_Ratio', 'Avg_Total_Sales', 'Game_Count']
            genre_patterns = genre_patterns.reset_index()
            
            fig = px.scatter(
                genre_patterns,
                x='Avg_Long_tail_Ratio',
                y='Avg_Total_Sales',
                size='Game_Count',
                color='Genre',
                title='Genre Analysis: Long-term vs Front-loaded Success Patterns',
                hover_data=['Game_Count']
            )
            
            fig.update_layout(
                xaxis_title='Average Long-term Success Ratio',
                yaxis_title='Average Total Sales (Millions)',
                height=500
            )
            
            # Add reference lines
            fig.add_vline(x=0.3, line_dash="dash", line_color="gray", 
                         annotation_text="Balanced threshold")
            fig.add_vline(x=0.6, line_dash="dash", line_color="green", 
                         annotation_text="Long-term focused")
            
        else:
            # Fallback visualization for single-release games
            genre_analysis = self.df.groupby('Genre').agg({
                'Global_Sales': ['mean', 'std', 'count']
            }).round(2)
            
            genre_analysis.columns = ['Avg_Sales', 'Sales_Variability', 'Game_Count']
            genre_analysis = genre_analysis.reset_index()
            
            fig = px.scatter(
                genre_analysis,
                x='Sales_Variability',
                y='Avg_Sales',
                size='Game_Count',
                color='Genre',
                title='Genre Consistency vs Average Sales',
                hover_data=['Game_Count']
            )
            
            fig.update_layout(
                xaxis_title='Sales Variability (Std Dev)',
                yaxis_title='Average Sales (Millions)',
                height=500
            )
        
        return fig
    
    def create_peak_performance_timeline(self):
        """Create timeline showing when different types of games peaked"""
        # Analyze peak performance years by platform and genre
        yearly_stats = self.df[self.df['Year'] >= 1980].groupby(['Year', 'Platform']).agg({
            'Global_Sales': ['sum', 'mean', 'count']
        }).round(2)
        
        yearly_stats.columns = ['Total_Sales', 'Avg_Sales', 'Game_Count']
        yearly_stats = yearly_stats.reset_index()
        
        # Get top 10 platforms by total sales for cleaner visualization
        top_platforms = self.df.groupby('Platform')['Global_Sales'].sum().nlargest(10).index
        yearly_stats_filtered = yearly_stats[yearly_stats['Platform'].isin(top_platforms)]
        
        fig = px.line(
            yearly_stats_filtered,
            x='Year',
            y='Total_Sales',
            color='Platform',
            title='Platform Peak Performance Timeline',
            line_group='Platform'
        )
        
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Total Sales (Millions)',
            height=500
        )
        
        return fig
