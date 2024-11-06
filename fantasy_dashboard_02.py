import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Page config
st.set_page_config(layout="wide", page_title="Fantasy Football Analytics")

# CSS styling
st.markdown("""
    <style>
    .stat-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    .team-name {
        font-size: 20px;
        font-weight: bold;
        color: white;
    }
    .metrics {
        color: white;
        font-size: 16px;
    }
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }
    .metric-value {
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 5px;
    }
    .trend-improving {
        color: #4CAF50;
    }
    .trend-declining {
        color: #f44336;
    }
    .trend-stable {
        color: #FFA726;
    }
    .lucky-card {
        background-color: rgba(255, 99, 99, 0.15);
    }
    .very-lucky-card {
        background-color: rgba(255, 99, 99, 0.25);
    }
    .unlucky-card {
        background-color: rgba(99, 149, 255, 0.15);
    }
    .very-unlucky-card {
        background-color: rgba(99, 149, 255, 0.25);
    }
    .neutral-card {
        background-color: rgba(128, 128, 128, 0.15);
    }
    .footer-text {
        color: rgba(255, 255, 255, 0.7);
        font-size: 14px;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Weekly matchups data
weekly_matchups = {
    1: [('hoon', 'Archer'), ('Abdullah', 'Gautam'), ('Yeef', 'Liam'), ('Veen', 'Neil'), ('Azhar', 'Sangmin')],
    2: [('hoon', 'Abdullah'), ('Archer', 'Gautam'), ('Yeef', 'Neil'), ('Azhar', 'Liam'), ('Veen', 'Sangmin')],
    3: [('hoon', 'Gautam'), ('Archer', 'Abdullah'), ('Veen', 'Yeef'), ('Liam', 'Sangmin'), ('Azhar', 'Neil')],
    4: [('hoon', 'Sangmin'), ('Yeef', 'Gautam'), ('Abdullah', 'Liam'), ('Archer', 'Neil'), ('Veen', 'Azhar')],
    5: [('hoon', 'Azhar'), ('Gautam', 'Liam'), ('Abdullah', 'Yeef'), ('Veen', 'Archer'), ('Neil', 'Sangmin')],
    6: [('hoon', 'Liam'), ('Neil', 'Gautam'), ('Veen', 'Abdullah'), ('Archer', 'Azhar'), ('Yeef', 'Sangmin')],
    7: [('hoon', 'Yeef'), ('Veen', 'Gautam'), ('Abdullah', 'Azhar'), ('Archer', 'Sangmin'), ('Neil', 'Liam')],
    8: [('hoon', 'Neil'), ('Azhar', 'Gautam'), ('Abdullah', 'Sangmin'), ('Archer', 'Yeef'), ('Veen', 'Liam')],
    9: [('hoon', 'Veen'), ('Gautam', 'Sangmin'), ('Abdullah', 'Neil'), ('Archer', 'Liam'), ('Yeef', 'Azhar')]
}

# Future matchups
future_matchups = {
    10: [('hoon', 'Archer'), ('Abdullah', 'Gautam'), ('Yeef', 'Liam'), ('Veen', 'Neil'), ('Azhar', 'Sangmin')],
    11: [('hoon', 'Abdullah'), ('Archer', 'Gautam'), ('Yeef', 'Neil'), ('Azhar', 'Liam'), ('Veen', 'Sangmin')],
    12: [('hoon', 'Gautam'), ('Archer', 'Abdullah'), ('Veen', 'Yeef'), ('Liam', 'Sangmin'), ('Azhar', 'Neil')],
    13: [('hoon', 'Sangmin'), ('Yeef', 'Gautam'), ('Abdullah', 'Liam'), ('Archer', 'Neil'), ('Veen', 'Azhar')],
    14: [('hoon', 'Azhar'), ('Gautam', 'Liam'), ('Abdullah', 'Yeef'), ('Veen', 'Archer'), ('Neil', 'Sangmin')]
}

# Raw weekly scores
weekly_scores = {
    'Gautam': [110.86, 200.12, 126.26, 123.64, 163.68, 127.42, 120.96, 174.5, 165.1],
    'hoon': [160.36, 132.82, 179.06, 113.28, 147.38, 165.62, 141.74, 146.86, 163.74],
    'Azhar': [163.48, 110.76, 136.64, 119.3, 142.64, 140.1, 154.42, 137.14, 140.48],
    'Abdullah': [108.68, 176.14, 137.18, 147.68, 143.62, 142.56, 119.34, 140.96, 131.96],
    'Sangmin': [127.72, 124.08, 152.08, 123.92, 129.32, 117.62, 167.54, 103.76, 146],
    'Veen': [170.26, 99.2, 99.9, 156.1, 135.84, 131.28, 75.74, 135.6, 168.4],
    'Liam': [107.52, 139.72, 104.34, 174.22, 99.7, 97.46, 150.56, 170.44, 121],
    'Yeef': [90.04, 141.44, 126.08, 98.8, 156.16, 144.32, 118.8, 151.64, 113.5],
    'Neil': [126.6, 103.4, 115.38, 114.84, 135.34, 118.5, 109.46, 148.78, 135.44],
    'Archer': [81.24, 114.16, 90.92, 97.92, 135.66, 125, 140.1, 158.6, 121.5]
}

# Actual wins
actual_wins = {
    'Gautam': 8, 'hoon': 5, 'Azhar': 5, 'Abdullah': 4,
    'Sangmin': 4, 'Veen': 4, 'Liam': 5, 'Yeef': 4,
    'Neil': 4, 'Archer': 2
}

def calculate_enhanced_expected_wins(scores, all_weekly_scores):
    """Calculate expected wins with sophisticated mean-median gap analysis"""
    team_mean = np.mean(scores)
    team_median = np.median(scores)
    mean_median_gap = team_mean - team_median
    
    # Calculate weekly medians and league averages
    weekly_medians = []
    for week in range(len(scores)):
        week_scores = [team_scores[week] for team_scores in all_weekly_scores.values()]
        weekly_medians.append(np.median(week_scores))
    
    # Base expected wins calculation
    base_expected_wins = sum(1 for i, score in enumerate(scores) if score > weekly_medians[i])
    
    # Calculate mean-median gap percentile
    league_gaps = [np.mean(team_scores) - np.median(team_scores) 
                  for team_scores in all_weekly_scores.values()]
    gap_percentile = sum(1 for gap in league_gaps 
                        if abs(gap) < abs(mean_median_gap)) / len(league_gaps)
    
    # Calculate adjustments based on gap analysis
    if mean_median_gap > 0:  # Right-skewed distribution (occasional high scores)
        gap_adjustment = -0.15 * gap_percentile * base_expected_wins
    else:  # Left-skewed distribution (occasional low scores)
        gap_adjustment = 0.15 * gap_percentile * base_expected_wins
    
    # Consistency adjustment
    weekly_cv = np.std(scores) / np.mean(scores)
    league_cvs = [np.std(team_scores) / np.mean(team_scores) 
                 for team_scores in all_weekly_scores.values()]
    avg_cv = np.mean(league_cvs)
    consistency_adjustment = 0.1 * (avg_cv - weekly_cv) * base_expected_wins
    
    # Calculate final expected wins
    enhanced_expected_wins = base_expected_wins + gap_adjustment + consistency_adjustment
    
    return max(0, min(len(scores), enhanced_expected_wins))

def calculate_performance_trends(scores):
    """Calculate performance trends and stability"""
    rolling_avg = []
    for i in range(len(scores)-2):
        avg = np.mean(scores[i:i+3])
        rolling_avg.append(avg)
    
    recent_trend = np.polyfit(range(4), scores[-4:], 1)[0]
    
    if abs(recent_trend) < 2:
        trend = 'Stable'
    elif recent_trend > 0:
        trend = 'Improving'
    else:
        trend = 'Declining'
    
    stability = 100 - (np.std(rolling_avg) / np.mean(rolling_avg) * 100)
    
    return {
        'rolling_averages': rolling_avg,
        'trend': trend,
        'stability': round(stability, 1),
        'trend_strength': abs(recent_trend)
    }

def get_opponent_for_week(team, week, matchups_dict):
    """Get a team's opponent for a specific week"""
    matchups = matchups_dict[week]
    for matchup in matchups:
        if team in matchup:
            return matchup[0] if matchup[1] == team else matchup[1]
    return None

def calculate_luck_score(team_name, weekly_scores, actual_wins, weekly_matchups):
    """Calculate enhanced luck score using both mean and median"""
    team_scores = weekly_scores[team_name]
    team_mean = np.mean(team_scores)
    team_median = np.median(team_scores)
    mean_median_gap = team_mean - team_median
    
    below_median_wins = 0
    median_to_mean_wins = 0
    close_games_won = 0
    close_games_lost = 0
    
    for week in range(1, 10):
        opponent = get_opponent_for_week(team_name, week, weekly_matchups)
        opp_score = weekly_scores[opponent][week-1]
        team_score = team_scores[week-1]
        
        won_game = team_score > opp_score
        
        if won_game:
            if team_score < team_median:
                below_median_wins += 1
            elif team_score < team_mean:
                median_to_mean_wins += 1
        
        if abs(team_score - opp_score) < 10:
            if won_game:
                close_games_won += 1
            else:
                close_games_lost += 1
    
    expected_wins = calculate_enhanced_expected_wins(team_scores, weekly_scores)
    wail = actual_wins[team_name] - expected_wins
    
    base_score = 50
    luck_score = base_score + (wail * 10)
    luck_score += (below_median_wins * 7)
    luck_score += (median_to_mean_wins * 3)
    
    total_close = close_games_won + close_games_lost
    if total_close > 0:
        close_game_ratio = close_games_won / total_close
        luck_score += ((close_game_ratio - 0.5) * 20)
    
    league_gaps = [np.mean(scores) - np.median(scores) for scores in weekly_scores.values()]
    avg_gap = np.mean(league_gaps)
    if abs(mean_median_gap) > abs(avg_gap):
        luck_score += 5 if mean_median_gap > 0 else -5
    
    luck_score = max(0, min(100, luck_score))
    
    return {
        'luck_score': round(luck_score, 1),
        'luck_rating': 'Very Lucky' if luck_score > 70 else
                      'Lucky' if luck_score > 60 else
                      'Slightly Lucky' if luck_score > 55 else
                      'Very Unlucky' if luck_score < 30 else
                      'Unlucky' if luck_score < 40 else
                      'Slightly Unlucky' if luck_score < 45 else
                      'Neutral',
        'close_games_record': f"{close_games_won}-{close_games_lost}",
        'below_median_wins': below_median_wins,
        'mean_median_gap': round(mean_median_gap, 2)
    }

def calculate_future_sos(team_name, weekly_scores, future_matchups):
    """Calculate strength of future schedule"""
    future_opponents = []
    for week in range(10, 15):
        opponent = get_opponent_for_week(team_name, week, future_matchups)
        future_opponents.append(opponent)
    
    opponent_avgs = [np.mean(weekly_scores[opp]) for opp in future_opponents]
    league_avg = np.mean([np.mean(scores) for scores in weekly_scores.values()])
    
    return {
        'future_sos': round(np.mean(opponent_avgs), 2),
        'vs_league_avg': round(np.mean(opponent_avgs) - league_avg, 2),
        'week_by_week': [(week, opp, round(np.mean(weekly_scores[opp]), 2)) 
                        for week, opp in zip(range(10, 15), future_opponents)]
    }

def calculate_metrics(scores, name):
    mean = np.mean(scores)
    median = np.median(scores)
    std_dev = np.std(scores)
    
    trends = calculate_performance_trends(scores)
    
    consistency_rating = (
        'High' if std_dev <= 20 else
        'Medium' if std_dev <= 25 else
        'Low'
    )
    
    enhanced_expected_wins = calculate_enhanced_expected_wins(scores, weekly_scores)
    wail = actual_wins[name] - enhanced_expected_wins
    
    max_avg_points = max(np.mean(team_scores) for team_scores in weekly_scores.values())
    points_score = (mean / max_avg_points) * 100
    win_score = (actual_wins[name] / 9) * 100
    consistency_score = 100 - ((std_dev / 30) * 100)
    perf_score = (points_score * 0.45) + (win_score * 0.35) + (consistency_score * 0.20)
    
    luck_metrics = calculate_luck_score(name, weekly_scores, actual_wins, weekly_matchups)
    future_metrics = calculate_future_sos(name, weekly_scores, future_matchups)
    
    return {
        'name': name,
        'record': f"{actual_wins[name]}-{9-actual_wins[name]}",
        'avgPF': round(mean, 2),
        'medianPF': round(median, 2),
        'mean_median_gap': round(mean - median, 2),
        'expectedWins': round(enhanced_expected_wins, 1),
        'actualWins': actual_wins[name],
        'wail': round(wail, 2),
        'weeklyStdDev': round(std_dev, 1),
        'consistency': consistency_rating,
        'trend': trends['trend'],
        'trend_stability': trends['stability'],
        'perfScore': round(perf_score, 1),
        'luck_score': luck_metrics['luck_score'],
        'luck_rating': luck_metrics['luck_rating'],
        'close_games_record': luck_metrics['close_games_record'],
        'below_median_wins': luck_metrics['below_median_wins'],
        'future_sos': future_metrics['future_sos'],
        'future_schedule': future_metrics['week_by_week']
    }

    # Calculate metrics for all teams
team_metrics = [calculate_metrics(scores, name) for name, scores in weekly_scores.items()]
team_metrics.sort(key=lambda x: x['perfScore'], reverse=True)

# Create performance trend visualization
def create_trend_chart(team_metrics):
    fig = go.Figure()
    
    # Calculate weekly league medians
    weekly_medians = []
    for week in range(9):  # 9 weeks of data
        week_scores = [weekly_scores[team][week] for team in weekly_scores]
        weekly_medians.append(np.median(week_scores))
    
    # Add team lines
    for team in team_metrics:
        scores = weekly_scores[team['name']]
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
        margin=dict(r=150)  # Add right margin for legend
    )
    
    return fig

# Display dashboard
st.title('Fantasy Football Analytics Dashboard')

# Performance vs Expected Wins Chart
fig_wins = go.Figure()
fig_wins.add_trace(go.Bar(
    name='Expected Wins',
    x=[team['name'] for team in team_metrics],
    y=[team['expectedWins'] for team in team_metrics],
    marker_color='#8884d8'
))
fig_wins.add_trace(go.Bar(
    name='Actual Wins',
    x=[team['name'] for team in team_metrics],
    y=[team['actualWins'] for team in team_metrics],
    marker_color='#82ca9d'
))

fig_wins.update_layout(
    title='Performance vs. Expected Wins',
    barmode='group',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white'
)

st.plotly_chart(fig_wins, use_container_width=True)

# Scoring Trends Chart
st.plotly_chart(create_trend_chart(team_metrics), use_container_width=True)

# Future Schedule Heatmap
schedule_data = []
for team in team_metrics:
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

st.plotly_chart(fig_schedule, use_container_width=True)

# Team Cards
for team in team_metrics:
    luck_class = (
        'very-lucky-card' if team['luck_score'] > 70 else
        'lucky-card' if team['luck_score'] > 60 else
        'very-unlucky-card' if team['luck_score'] < 30 else
        'unlucky-card' if team['luck_score'] < 40 else
        'neutral-card'
    )
    
    st.markdown(f"""
        <div class="stat-card {luck_class}">
            <div class="card-header">
                <span class="team-name">{team['name']} ({team['record']})</span>
                <span class="metrics">Perf Score: {team['perfScore']} | Luck Score: {team['luck_score']}</span>
            </div>
            <div class="metric-grid">
                <div>
                    <div class="metric-value">Avg PF: {team['avgPF']}</div>
                    <div class="metric-value">Median PF: {team['medianPF']}</div>
                    <div class="metric-value">Mean-Median Gap: {team['mean_median_gap']}</div>
                </div>
                <div>
                    <div class="metric-value">Expected Wins: {team['expectedWins']}</div>
                    <div class="metric-value">WAIL: {team['wail']}</div>
                    <div class="metric-value">Below Median Wins: {team['below_median_wins']}</div>
                </div>
                <div>
                    <div class="metric-value">Luck Rating: {team['luck_rating']}</div>
                    <div class="metric-value">Close Games: {team['close_games_record']}</div>
                    <div class="metric-value trend-{team['trend'].lower()}">{team['trend']} (Stability: {team['trend_stability']})</div>
                </div>
                <div>
                    <div class="metric-value">Future SoS: {team['future_sos']}</div>
                    <div class="metric-value">Consistency: {team['consistency']}</div>
                    <div class="metric-value">StdDev: {team['weeklyStdDev']}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer-text">
        <p><strong>Metrics Explanation:</strong></p>
        <p>• Mean-Median Gap shows scoring distribution skew</p>
        <p>• Below Median Wins indicates unsustainable success</p>
        <p>• Trend shows recent performance direction</p>
        <p>• Stability Score (0-100) shows performance consistency</p>
    </div>
""", unsafe_allow_html=True)
