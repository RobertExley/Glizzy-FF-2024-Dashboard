import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from data_collector.data_collector import SleeperDataCollector

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

LEAGUE_ID = '1124814690363400192'

sleeperData = SleeperDataCollector(LEAGUE_ID)

# Weekly matchups data and raw scores
ALL_WEEKLY_MATCHUPS, WEEKLY_SCORES = sleeperData.get_all_weekly_matchups_and_scores()

CURRENT_WEEK = sleeperData.get_current_week()
COMPLETED_WEEKS = CURRENT_WEEK - 1

PAST_WEEKLY_MATCHUPS = { k:v for k, v in ALL_WEEKLY_MATCHUPS.items() if k < CURRENT_WEEK }
FUTURE_MATCHUPS = { k:v for k,v in ALL_WEEKLY_MATCHUPS.items() if k >= CURRENT_WEEK }

USERNAMES = sleeperData.get_usernames()

# Actual wins
ACTUAL_WINS = sleeperData.get_wins()

# Weekly fractional wins (how many teams a team would beat in a given week)
WEEKLY_FRACTIONAL_WINS = sleeperData.get_weekly_fractional_records(weekly_scores=WEEKLY_SCORES)

# Calculate fractional records
fractional_records = {}
for team, wins in WEEKLY_FRACTIONAL_WINS.items():
    wins = sum(wins)
    losses = (COMPLETED_WEEKS * (len(USERNAMES) - 1)) - wins
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
    for week in range(COMPLETED_WEEKS):
        print(week)
        week_scores = [team_scores[week] for team_scores in WEEKLY_SCORES.values()]
        weekly_medians.append(np.median(week_scores))
        
        # Get fractional score for the week
        fractional_score = WEEKLY_FRACTIONAL_WINS[name][week]
        
        if scores[week] > weekly_medians[week]:
            # Above median: weight by how impressive the performance was
            quality_modifier = (fractional_score / COMPLETED_WEEKS)  # Scale of 0 to 1
            adjusted_wins += 0.7 + (0.3 * quality_modifier)  # Base win (0.7) plus quality bonus
        else:
            # Below median: partial credit based on how close they were
            quality_modifier = (fractional_score / COMPLETED_WEEKS)  # Scale of 0 to 1
            adjusted_wins += 0.3 * quality_modifier  # Partial credit for strong below-median performance
    
    return round(adjusted_wins, 1)

def calculate_enhanced_luck_score(team_name):
    """Calculate luck score incorporating quality wins and tough losses"""
    scores = WEEKLY_SCORES[team_name]
    team_median = np.median(scores)
    
    base_score = 50
    luck_adjustments = []
    below_median_wins = 0
    close_games_won = 0
    close_games_lost = 0
    
    for week in range(COMPLETED_WEEKS):
        opponent = get_opponent_for_week(team_name, week + 1, PAST_WEEKLY_MATCHUPS)
        team_score = scores[week]
        opp_score = WEEKLY_SCORES[opponent][week]
        fractional_score = WEEKLY_FRACTIONAL_WINS[team_name][week]
        
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
    wail = ACTUAL_WINS[team_name] - expected_wins
    
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
    
    print(f"PERFORMANCE: {name}")
    # Base components
    max_avg_points = max(np.mean(team_scores) for team_scores in WEEKLY_SCORES.values())
    print(f"max avg pts = {max_avg_points}")
    base_points_score = (mean / max_avg_points) * 100
    print(f"base pts score = {base_points_score}")
    win_score = (ACTUAL_WINS[name] / COMPLETED_WEEKS) * 100
    print(f"win_score = {win_score}")
    consistency_score = 100 - ((std_dev / 30) * 100)
    print(f"consistency_score = {consistency_score}")
    
    # Calculate quality of points using fractional data
    weekly_quality_scores = []
    for week in range(COMPLETED_WEEKS):
        fractional_score = WEEKLY_FRACTIONAL_WINS[name][week]
        quality_modifier = fractional_score / COMPLETED_WEEKS  # Scale of 0 to 1
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
        opponent = get_opponent_for_week(team_name, week, FUTURE_MATCHUPS)
        future_opponents.append(opponent)
    
    opponent_avgs = [np.mean(WEEKLY_SCORES[opp]) for opp in future_opponents]
    league_avg = np.mean([np.mean(scores) for scores in WEEKLY_SCORES.values()])
    
    return {
        'future_sos': round(np.mean(opponent_avgs), 2),
        'vs_league_avg': round(np.mean(opponent_avgs) - league_avg, 2),
        'week_by_week': [(week, opp, round(np.mean(WEEKLY_SCORES[opp]), 2)) 
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
    wail = ACTUAL_WINS[name] - enhanced_expected_wins
    perf_score = calculate_performance_score(scores, name)
    luck_metrics = calculate_enhanced_luck_score(name)
    future_metrics = calculate_future_sos(name)
    
    return {
        'name': name,
        'record': f"{ACTUAL_WINS[name]}-{COMPLETED_WEEKS-ACTUAL_WINS[name]}",
        'avgPF': round(mean, 2),
        'medianPF': round(median, 2),
        'mean_median_gap': round(mean - median, 2),
        'expectedWins': enhanced_expected_wins,
        'actualWins': ACTUAL_WINS[name],
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
team_metrics = [calculate_metrics(scores, name) for name, scores in WEEKLY_SCORES.items()]
team_metrics.sort(key=lambda x: x['perfScore'], reverse=True)

def create_trend_chart(team_metrics):
    fig = go.Figure()
    
    # Calculate weekly league medians
    weekly_medians = []
    for week in range(COMPLETED_WEEKS):
        week_scores = [WEEKLY_SCORES[team][week] for team in WEEKLY_SCORES]
        weekly_medians.append(np.median(week_scores))
    
    # Add team lines
    for team in team_metrics:
        scores = WEEKLY_SCORES[team['name']]
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

# Process total fractional records
fractional_records = {}
for team, wins in WEEKLY_FRACTIONAL_WINS.items():
    wins = sum(wins)
    losses = (COMPLETED_WEEKS * (len(USERNAMES) - 1)) - wins
    fractional_records[team] = {
        'total_wins': wins,
        'total_losses': losses
    }

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
    marker_color='#ffc658',
    text=[f"{fractional_records[team]['total_wins']}/81" for team in sorted_team_names],
    textposition='auto',
    hoverinfo='text'
))
fig_fractional_total.add_trace(go.Bar(
    name='Fractional Losses',
    x=sorted_team_names,
    y=[81 - fractional_records[team]['total_wins'] for team in sorted_team_names],
    marker_color='#ff7f7f',
    text=[f"{81 - fractional_records[team]['total_wins']}/81" for team in sorted_team_names],
    textposition='auto',
    hoverinfo='text'
))

fig_fractional_total.update_layout(
    title='Total Fractional Records',
    barmode='stack',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    yaxis=dict(
        title='Fractional Wins / Losses',
        range=[0, 81],
        tickvals=[0, 20, 40, 60, 81],
        ticktext=['0', '20', '40', '60', '81']
    )
)

st.plotly_chart(fig_fractional_total, use_container_width=True)

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
    
    # Construct the fractional record string
    fractional_record = f"{fractional_records[team['name']]['total_wins']}/81"
    
    st.markdown(f"""
        <div class="stat-card {luck_class}">
            <div class="card-header">
                <span class="team-name">{team['name']} ({team['record']})</span>
                <span class="metrics">
                    Perf Score: {team['perfScore']} | 
                    Luck Score: {team['luck_score']} | 
                    Fractional: {fractional_record}
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
