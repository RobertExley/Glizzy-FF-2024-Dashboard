import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

class ManagerProfile:
    def __init__(self, calculator):
        self.calculator = calculator

    def create_performance_timeline(self, manager_name):
        weekly_scores = self.calculator.get_weekly_scores()[manager_name]
        num_weeks = len(weekly_scores)
        weeks = list(range(1, num_weeks + 1))

        weekly_medians = []
        all_scores = self.calculator.get_weekly_scores()
        for week in range(num_weeks):
            week_scores = [scores[week] for scores in all_scores.values()]
            weekly_medians.append(np.median(week_scores))

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

        fig = go.Figure()
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

        fig.update_layout(
            title=dict(
                text=f"{manager_name}'s Weekly Performance",
                font=dict(size=24)
            ),
            height=400,
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

        scores_range = max(weekly_scores) - min(weekly_scores)
        y_min = min(weekly_scores) - (scores_range * 0.1)
        y_max = max(weekly_scores) + (scores_range * 0.1)
        fig.update_yaxes(range=[y_min, y_max])

        return fig

    def render_profile(self, manager_name):
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

        # Define base CSS styles
        st.markdown('''
        <style>
        .stats-container {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 12px;
            padding: 25px;
            margin: 30px 0;
        }
        .stats-header {
            color: #64B5F6;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 25px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(100, 181, 246, 0.3);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }
        .stat-card {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 15px;
            display: flex;
            flex-direction: column;
            transition: all 0.2s ease;
        }
        .stat-card:hover {
            transform: translateY(-2px);
            border-color: rgba(100, 181, 246, 0.3);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stat-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 14px;
            margin-bottom: 8px;
        }
        .stat-value {
            color: white;
            font-size: 20px;
            font-weight: bold;
        }
        </style>
        ''', unsafe_allow_html=True)

        # Generate statistics HTML
        stats_html = f'''
        <div class="stats-container">
            <h3 class="stats-header">Season Stats</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-label">Record</span>
                    <span class="stat-value">{metrics['record']}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Expected Wins</span>
                    <span class="stat-value">{metrics['expectedWins']:.1f}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">WAIL</span>
                    <span class="stat-value">{metrics['wail']:.2f}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Fractional Record</span>
                    <span class="stat-value">{metrics['fractional_record']['total_wins']}/{metrics['fractional_record']['total_wins'] + metrics['fractional_record']['total_losses']}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Average Points For</span>
                    <span class="stat-value">{metrics['avgPF']:.2f}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Median PF</span>
                    <span class="stat-value">{metrics['medianPF']:.2f}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Mean-Median Gap</span>
                    <span class="stat-value">{metrics['mean_median_gap']:.2f}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Below Median Wins</span>
                    <span class="stat-value">{metrics['below_median_wins']}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Luck Rating</span>
                    <span class="stat-value">{metrics['luck_rating']}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Consistency</span>
                    <span class="stat-value">{metrics['consistency']}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">Close Games Record</span>
                    <span class="stat-value">{metrics['close_games_record']}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">StdDev</span>
                    <span class="stat-value">{metrics['weeklyStdDev']:.1f}</span>
                </div>
            </div>
        </div>
        '''

        st.markdown(stats_html, unsafe_allow_html=True)
