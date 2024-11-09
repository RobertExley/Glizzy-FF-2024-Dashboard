import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

class DataPlotter:
    def __init__(self, calculator, usernames):
        self.calculator = calculator
        self.weekly_scores = calculator.get_weekly_scores()
        self.fractional_wins = calculator.get_fractional_wins()
        self.num_weeks = calculator.get_num_weeks()
        self.team_metrics = calculator.calculate_metrics_all_teams()

    def get_team_metrics(self):
        return self.team_metrics

    def create_trend_chart(self):
        fig = go.Figure()
        
        # Calculate weekly league medians
        weekly_medians = []
        for week in range(self.num_weeks):
            week_scores = [self.weekly_scores[team][week] for team in self.weekly_scores]
            weekly_medians.append(np.median(week_scores))
        
        # Add team lines
        for team in self.team_metrics:
            scores = self.weekly_scores[team['name']]
            fig.add_trace(go.Scatter(
                x=list(range(1, 10)),
                y=scores,
                name=team['name'],
                mode='lines+markers'
            ))
        
        # Add league median line
        fig.add_trace(go.Scatter(
            x=list(range(1, 10)),
            y=weekly_medians,
            name='League Median',
            mode='lines',
            line=dict(
                color='rgba(255, 255, 255, 0.5)',
                width=2,
                dash='dash'
            ),
            hovertemplate='Week %{x}<br>League Median: %{y:.1f}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Scoring Trends by Week',
            xaxis_title='Week',
            yaxis_title='Points',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.02
            ),
            margin=dict(r=150)
        )
        
        return fig
    
    def create_performance_and_expected_wins_chart(self):
        # Performance vs Expected Wins Chart
        fig_wins = go.Figure()
        fig_wins.add_trace(go.Bar(
            name='Expected Wins',
            x=[team['name'] for team in self.team_metrics],
            y=[team['expectedWins'] for team in self.team_metrics],
            marker_color='#8884d8'
        ))
        fig_wins.add_trace(go.Bar(
            name='Actual Wins',
            x=[team['name'] for team in self.team_metrics],
            y=[team['actualWins'] for team in self.team_metrics],
            marker_color='#82ca9d'
        ))

        fig_wins.update_layout(
            title='Performance vs. Expected Wins',
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )

        return fig_wins
    
    def create_fractional_records_chart(self):
        # Sort teams by fractional win percentage

        sorted_team_names = sorted(
            [team['name'] for team in self.team_metrics],
            key=lambda name: next(
                team['fractional_record']['total_wins'] 
                for team in self.team_metrics 
                if team['name'] == name
            ),
            reverse=True
        )

        total_fractional_games = self.num_weeks * (len(sorted_team_names) - 1)

        team_metrics_dict = {team['name']: team for team in self.team_metrics}

        # Total Fractional Records Chart
        fig_fractional_total = go.Figure()
        fig_fractional_total.add_trace(go.Bar(
            name='Fractional Wins',
            x=sorted_team_names,
            y=[team_metrics_dict[team]['fractional_record']['total_wins'] for team in sorted_team_names],
            marker_color='#ffc658',
            text=[f"{team_metrics_dict[team]['fractional_record']['total_wins']}/{total_fractional_games}" for team in sorted_team_names],
            textposition='auto',
            hoverinfo='text'
        ))
        fig_fractional_total.add_trace(go.Bar(
            name='Fractional Losses',
            x=sorted_team_names,
            y=[f"{team_metrics_dict[team]['fractional_record']['total_losses']}" for team in sorted_team_names],
            marker_color='#ff7f7f',
            text=[f"{team_metrics_dict[team]['fractional_record']['total_losses']}/{total_fractional_games}" for team in sorted_team_names],
            textposition='auto',
            hoverinfo='text'
        ))

        num_ticks = 5
        tick_interval = round(total_fractional_games / (num_ticks - 1))  # -1 because we include 0
        
        # Generate tick values from 0 to total_possible_wins
        tick_vals = list(range(0, total_fractional_games + 1, tick_interval))
        if tick_vals[-1] != total_fractional_games:
            tick_vals.append(total_fractional_games)
        
        # Convert to strings for tick labels
        tick_text = [str(val) for val in tick_vals]

        fig_fractional_total.update_layout(
            title='Total Fractional Records',
            barmode='stack',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            yaxis=dict(
                title='Fractional Wins / Losses',
                range=[0, total_fractional_games],
                tickvals=tick_vals,
                ticktext=tick_text
            )
        )

        return fig_fractional_total

    def create_future_schedule_heatmap(self):
        schedule_data = []
        for team in self.team_metrics:
            team_data = {'Team': team['name']}
            for week, opp, score in team['future_schedule']:
                team_data[f'Week {week}'] = score
            schedule_data.append(team_data)

        schedule_df = pd.DataFrame(schedule_data)
        schedule_df.set_index('Team', inplace=True)

        fig_schedule = px.imshow(
            schedule_df,
            title='Remaining Schedule Difficulty (Opponent Avg. Points)',
            color_continuous_scale='RdYlBu_r'
        )
        fig_schedule.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )

        return fig_schedule