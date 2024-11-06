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

# Actual wins
actual_wins = {
    'Gautam': 8, 'hoon': 5, 'Azhar': 5, 'Abdullah': 4,
    'Sangmin': 4, 'Veen': 4, 'Liam': 5, 'Yeef': 4,
    'Neil': 4, 'Archer': 2
}

# Total fractional records
total_fractional_records = {
    'Veen': '37/81',
    'Azhar': '46/81',
    'hoon': '56/81',
    'Sangmin': '41/81',
    'Neil': '26/81',
    'Gautam': '57/81',
    'Abdullah': '47/81',
    'Liam': '36/81',
    'Yeef': '37/81',
    'Archer': '23/81'
}

# Weekly fractional records
weekly_fractional_records = {
    'Veen': [9, 0, 1, 8, 4, 5, 0, 1, 9],
    'Azhar': [8, 2, 6, 4, 5, 6, 8, 2, 5],
    'hoon': [7, 5, 9, 2, 7, 9, 6, 4, 7],
    'Sangmin': [6, 4, 8, 6, 1, 1, 9, 0, 6],
    'Neil': [5, 1, 3, 3, 2, 2, 1, 5, 4],
    'Gautam': [4, 9, 5, 5, 5, 4, 4, 8, 8],
    'Abdullah': [3, 8, 7, 7, 6, 7, 3, 3, 3],
    'Liam': [2, 6, 2, 9, 0, 0, 7, 8, 2],
    'Yeef': [1, 7, 4, 1, 8, 8, 2, 6, 0],
    'Archer': [0, 3, 0, 0, 3, 3, 5, 7, 2]
}

# Calculate fractional records
fractional_records = {}
for team in total_fractional_records:
    wins, losses = map(int, total_fractional_records[team].split('/'))
    win_pct = wins / (wins + losses)
    fractional_records[team] = {
        'record': f"{wins}-{losses}",
        'win_pct': round(win_pct, 3),
        'total_wins': wins,
        'total_losses': losses
    }

def get_opponent_for_week(team, week, matchups_dict):
    """Get a team's opponent for a specific week"""
    matchups = matchups_dict[week]
    for matchup in matchups:
        if team in matchup:
            return matchup[0] if matchup[1] == team else matchup[1]
    return None

def calculate_enhanced_expected_wins(scores, name):
    """Calculate expected wins using fractional data to weigh performance quality"""
    weekly_medians = []
    adjusted_wins = 0
    
    # Calculate weekly medians
    for week in range(len(scores)):
        week_scores = [team_scores[week] for team_scores in weekly_scores.values()]
        weekly_medians.append(np.median(week_scores))
        
        # Get fractional score for the week
        fractional_score = weekly_fractional_records[name][week]
        
        if scores[week] > weekly_medians[week]:
            # Above median: weight by how impressive the performance was
            quality_modifier = (fractional_score / 9)  # Scale of 0 to 1
            adjusted_wins += 0.7 + (0.3 * quality_modifier)  # Base win (0.7) plus quality bonus
        else:
            # Below median: partial credit based on how close they were
            quality_modifier = (fractional_score / 9)  # Scale of 0 to 1
            adjusted_wins += 0.3 * quality_modifier  # Partial credit for strong below-median performance
    
    return round(adjusted_wins, 1)

def calculate_enhanced_luck_score(team_name):
    """Calculate luck score incorporating quality wins and tough losses"""
    scores = weekly_scores[team_name]
    team_median = np.median(scores)
    
    base_score = 50
    luck_adjustments = []
    below_median_wins = 0
    close_games_won = 0
    close_games_lost = 0
    
    for week in range(9):
        opponent = get_opponent_for_week(team_name, week + 1, weekly_matchups)
        team_score = scores[week]
        opp_score = weekly_scores[opponent][week]
        fractional_score = weekly_fractional_records[team_name][week]
        
        won_game = team_score > opp_score
        
        if won_game:
            if team_score < team_median:
                below_median_wins += 1
                
            # Quality win analysis
            if fractional_score <= 3:  # Won despite low fractional score
                luck_adjustments.append(5)  # Lucky win
            elif fractional_score >= 7:  # Won with high fractional score
                luck_adjustments.append(-1)  # Expected win
        else:
            # Tough loss analysis
            if fractional_score >= 7:  # Lost despite high fractional score
                luck_adjustments.append(-5)  # Very unlucky
            elif fractional_score <= 3:  # Lost with low fractional score
                luck_adjustments.append(1)  # Expected loss
        
        # Track close games
        if abs(team_score - opp_score) < 10:
            if won_game:
                close_games_won += 1
            else:
                close_games_lost += 1
    
    # Calculate expected wins
    expected_wins = calculate_enhanced_expected_wins(scores, team_name)
    wail = actual_wins[team_name] - expected_wins
    
    # Combine all luck components
    luck_score = base_score
    luck_score += sum(luck_adjustments)  # Quality wins/tough losses impact
    luck_score += (wail * 8)  # WAIL impact
    luck_score += (below_median_wins * 4)  # Below median wins impact
    
    # Close games impact
    if (close_games_won + close_games_lost) > 0:
        close_game_ratio = close_games_won / (close_games_won + close_games_lost)
        luck_score += ((close_game_ratio - 0.5) * 16)
    
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
        'below_median_wins': below_median_wins
    }

def calculate_performance_score(scores, name):
    """Calculate performance score using fractional data as quality modifier"""
    mean = np.mean(scores)
    std_dev = np.std(scores)
    
    # Base components
    max_avg_points = max(np.mean(team_scores) for team_scores in weekly_scores.values())
    base_points_score = (mean / max_avg_points) * 100
    win_score = (actual_wins[name] / 9) * 100
    consistency_score = 100 - ((std_dev / 30) * 100)
    
    # Calculate quality of points using fractional data
    weekly_quality_scores = []
    for week, score in enumerate(scores):
        fractional_score = weekly_fractional_records[name][week]
        quality_modifier = fractional_score / 9  # Scale of 0 to 1
        weekly_quality_scores.append(quality_modifier)
    
    avg_quality = np.mean(weekly_quality_scores)
    quality_adjusted_points = base_points_score * (0.7 + (0.3 * avg_quality))
    
    # Final weighted score
    perf_score = (
        (quality_adjusted_points * 0.50) +  # Points scored with quality adjustment
        (win_score * 0.30) +                # Actual wins
        (consistency_score * 0.20)          # Consistency
    )
    
    return round(perf_score, 1)

def calculate_future_sos(team_name):
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
    """Calculate all metrics for a team"""
    mean = np.mean(scores)
    median = np.median(scores)
    std_dev = np.std(scores)
    
    # Calculate trend metrics
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
    
    consistency_rating = (
        'High' if std_dev <= 20 else
        'Medium' if std_dev <= 25 else
        'Low'
    )
    
    enhanced_expected_wins = calculate_enhanced_expected_wins(scores, name)
    wail = actual_wins[name] - enhanced_expected_wins
    perf_score = calculate_performance_score(scores, name)
    luck_metrics = calculate_enhanced_luck_score(name)
    future_metrics = calculate_future_sos(name)
    
    return {
        'name': name,
        'record': f"{actual_wins[name]}-{9-actual_wins[name]}",
        'avgPF': round(mean, 2),
        'medianPF': round(median, 2),
        'mean_median_gap': round(mean - median, 2),
        'expectedWins': enhanced_expected_wins,
        'actualWins': actual_wins[name],
        'wail': round(wail, 2),
        'weeklyStdDev': round(std_dev, 1),
        'consistency': consistency_rating,
        'trend': trend,
        'trend_stability': round(stability, 1),
        'perfScore': perf_score,
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

def create_trend_chart(team_metrics):
    fig = go.Figure()
    
    # Calculate weekly league medians
    weekly_medians = []
    for week in range(9):
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
        margin=dict(r=150)
    )
    
    return fig

# Display dashboard
st.title('Fantasy Football Analytics Dashboard')

# Sort teams by fractional win percentage
sorted_teams = sorted(
    fractional_records.items(),
    key=lambda x: x[1]['total_wins'] / (x[1]['total_wins'] + x[1]['total_losses']),
    reverse=True
)
sorted_team_names = [team[0] for team in sorted_teams]

# Total Fractional Records Chart
fig_fractional_total = go.Figure()
fig_fractional_total.add_trace(go.Bar(
    name='Fractional Wins',
    x=sorted_team_names,
    y=[fractional_records[team]['total_wins'] for team in sorted_team_names],
    marker_color='#ffc658'
))
fig_fractional_total.add_trace(go.Bar(
    name='Fractional Losses',
    x=sorted_team_names,
    y=[fractional_records[team]['total_losses'] for team in sorted_team_names],
    marker_color='#ff7f7f'
))

fig_fractional_total.update_layout(
    title='Total Fractional Record Distribution',
    barmode='stack',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white'
)

st.plotly_chart(fig_fractional_total, use_container_width=True)

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
                <span class="metrics">
                    Perf Score: {team['perfScore']} | 
                    Luck Score: {team['luck_score']} | 
                    Fractional: {fractional_records[team['name']]['record']}
                </span>
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
