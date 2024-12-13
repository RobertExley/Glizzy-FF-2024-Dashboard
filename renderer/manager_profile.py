import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

class ManagerProfile:
    def __init__(self, calculator):
        """Initialize ManagerProfile with calculator instance."""
        self.calculator = calculator

    def create_performance_timeline(self, manager_name):
        """Generate interactive performance timeline visualization."""
        # Retrieve manager's weekly scores
        weekly_scores = self.calculator.get_weekly_scores()[manager_name]
        num_weeks = len(weekly_scores)
        weeks = list(range(1, num_weeks + 1))

        # Calculate weekly medians
        weekly_medians = []
        all_scores = self.calculator.get_weekly_scores()
        for week in range(num_weeks):
            week_scores = [scores[week] for scores in all_scores.values()]
            weekly_medians.append(np.median(week_scores))

        # Get matchup results and details
        matchup_results = []
        for week in range(num_weeks):
            opponent = None
            for matchup in self.calculator.past_weekly_matchups.get(week + 1, []):
                if manager_name in matchup:
                    opponent = matchup[0] if matchup[1] == manager_name else matchup[1]
                    opponent_score = all_scores[opponent][week]
                    result = "W" if weekly_scores[week] > opponent_score else "L"
                    matchup_results.append({
                        'week': week + 1,
                        'opponent': opponent,
                        'score': weekly_scores[week],
                        'opp_score': opponent_score,
                        'result': result
                    })
                    break

        # Create figure
        fig = go.Figure()

        # Add manager's score line
        fig.add_trace(go.Scatter(
            x=weeks,
            y=weekly_scores,
            name=manager_name,
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(
                size=12,
                color=['#22c55e' if mr['result'] == 'W' else '#ef4444' for mr in matchup_results],
                line=dict(width=2, color='white')
            ),
            hovertemplate=(
                "<b>Week %{x}</b><br>" +
                f"{manager_name}: %{{y:.1f}}<br>" +
                "<extra></extra>"
            )
        ))

        # Add league median line
        fig.add_trace(go.Scatter(
            x=weeks,
            y=weekly_medians,
            name='League Median',
            mode='lines',
            line=dict(
                color='rgba(255, 255, 255, 0.5)',
                width=2,
                dash='dash'
            ),
            hovertemplate="League Median: %{y:.1f}<extra></extra>"
        ))

        # Customize layout with theme-consistent styling
        fig.update_layout(
            title=dict(
                text=f"{manager_name}'s Weekly Performance",
                font=dict(size=24)
            ),
            height=400,  # Fixed height
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=True,
            hovermode='x unified',
            xaxis=dict(
                title="Week",
                gridcolor='rgba(255,255,255,0.1)',
                tickmode='linear',
                tick0=1,
                dtick=1,
                showgrid=True
            ),
            yaxis=dict(
                title="Points Scored",
                gridcolor='rgba(255,255,255,0.1)',
                zeroline=False,
                showgrid=True
            ),
            margin=dict(t=50, r=20, b=50, l=50)
        )

        # Update y-axis range for better visualization
        scores_range = max(weekly_scores) - min(weekly_scores)
        y_min = min(weekly_scores) - (scores_range * 0.1)
        y_max = max(weekly_scores) + (scores_range * 0.1)
        fig.update_yaxes(range=[y_min, y_max])

        return fig

    def render_profile(self, manager_name):
        """Render complete manager profile with metrics and visualizations."""
        # Retrieve manager metrics
        metrics = next(
            (team for team in self.calculator.calculate_metrics_all_teams() 
             if team['name'] == manager_name),
            None
        )
        
        if not metrics:
            st.error(f"No metrics found for {manager_name}")
            return

        # Display performance timeline
        st.plotly_chart(
            self.create_performance_timeline(manager_name),
            use_container_width=True,
            config={'displayModeBar': False}
        )

        # Performance Metrics Layout
        st.subheader("Season Stats")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Record", metrics['record'])

        with col2:
            st.metric("Average Points For", f"{metrics['avgPF']:.2f}")

        with col3:
            st.metric("Performance Score", f"{metrics['perfScore']:.1f}")

        with col4:
            st.metric("Expected Wins", f"{metrics['expectedWins']:.1f}")

        with col5:
            st.metric("WAIL", f"{metrics['wail']:.2f}")

        with col6:
            st.metric("Luck Score", f"{metrics['luck_score']:.1f}")
            
        # Detailed Statistics
        st.subheader("Detailed Statistics")
        col7, col8, col9 = st.columns(3)
        
        with col7:
            st.metric("Consistency Rating", metrics['consistency'])
            st.metric("Weekly StdDev", f"{metrics['weeklyStdDev']:.1f}")
            
        with col8:
            st.metric("Close Games Record", metrics['close_games_record'])
            st.metric("Below Median Wins", str(metrics['below_median_wins']))

        with col9:
            st.metric("Performance Trend", metrics['trend'])
            st.metric("Trend Stability", f"{metrics['trend_stability']:.1f}")