import streamlit as st
from .manager_profile import ManagerProfile

class DashboardUI:
    def __init__(self, dataPlotter):
        self._css()
        self.plotter = dataPlotter
        self.team_metrics = dataPlotter.get_team_metrics()
        self.num_weeks = dataPlotter.calculator.get_num_weeks()

    def render(self):
        fig_wins = self.plotter.create_performance_and_expected_wins_chart()
        st.plotly_chart(fig_wins, use_container_width=True)

        fig_fractional_total = self.plotter.create_fractional_records_chart()
        st.plotly_chart(fig_fractional_total, use_container_width=True)

        fig_trend_chart = self.plotter.create_trend_chart()
        st.plotly_chart(fig_trend_chart, use_container_width=True)

        fig_schedule = self.plotter.create_future_schedule_heatmap()
        st.plotly_chart(fig_schedule, use_container_width=True)

        self._team_cards()
        self._footer()
    
    def _render_dashboard(self):
        st.title('Fantasy Football Analytics Dashboard')

        fig_wins = self.plotter.create_performance_and_expected_wins_chart()
        st.plotly_chart(fig_wins, use_container_width=True)

        fig_fractional_total = self.plotter.create_fractional_records_chart()
        st.plotly_chart(fig_fractional_total, use_container_width=True)

        fig_trend_chart = self.plotter.create_trend_chart()
        st.plotly_chart(fig_trend_chart, use_container_width=True)

        fig_schedule = self.plotter.create_future_schedule_heatmap()
        st.plotly_chart(fig_schedule, use_container_width=True)

        self._team_cards()
        self._footer()
    
    def _render_manager_profile(self, manager_name):
        profile = ManagerProfile(self.plotter.calculator, manager_name)
        profile.render()
    def _team_cards(self):
        for team in self.team_metrics:
            luck_class = (
                'very-lucky-card' if team['luck_score'] > 70 else
                'lucky-card' if team['luck_score'] > 60 else
                'very-unlucky-card' if team['luck_score'] < 30 else
                'unlucky-card' if team['luck_score'] < 40 else
                'neutral-card'
            )
        
            total_games = team['fractional_record']['total_wins'] + team['fractional_record']['total_losses']
            fractional_record = f"{team['fractional_record']['total_wins']}/{total_games}"
            
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

    def _footer(self):
        st.markdown("""
    <div class="footer-container">
        <div class="footer-text">
            <p><strong>Performance Score (perfScore)</strong></p>
            <p>• Weighted composite of points scored (50% - quality adjusted), actual wins (30%), and consistency (20%)</p>
            <p>• Points are adjusted by "quality of points" multiplier derived from fractional wins</p>
            <p>• Provides a holistic assessment of a team's performance level</p>
            <p>• Higher values indicate stronger overall performance in key areas</p>
        </div>       
        <div class="footer-text">                     
            <p><strong>Enhanced Expected Wins (expectedWins)</strong></p>
            <p>• Sum of weekly fractional wins with a quality adjustment</p>
            <p>• Above median scores get a 0.7 base win plus fractional bonus</p>
            <p>• Below median scores get fractional credit only</p>
            <p>• Estimates "true" win total based on quality of performance</p>
            <p>• Compare to actual wins to evaluate over/under performance</p>
        </div>
        <div class="footer-text">
            <p><strong>Wins Above/Below Expectation (WAIL)</strong></p>
            <p>• Difference between actual wins and enhanced expected wins</p>
            <p>• Positive values indicate wins above expectation (lucky)</p>
            <p>• Negative values indicate wins below expectation (unlucky)</p>
            <p>• Useful for quantifying the impact of luck on a team's record</p>
        </div>       
        <div class="footer-text">
            <p><strong>Consistency Rating & Weekly Standard Deviation</strong></p>
            <p>• weeklyStdDev: Standard deviation of weekly scores</p>
            <p>• consistency: 'High' (<= 20), 'Medium' (20-25), 'Low' (> 25)</p>
            <p>• Measures the variability in a team's weekly performance</p>
            <p>• Lower stdDev and 'High' consistency imply steady, reliable scoring</p>
            <p>• High variations make a team's output less predictable week-to-week</p>
        </div>
        <div class="footer-text">
            <p><strong>Performance Trend &amp; Stability</strong></p>
            <p>• trend: Slope of scores over last 4 weeks</p>
            <p>&nbsp;&nbsp;- 'Improving' (&gt; 2), 'Declining' (&lt; -2), or 'Stable'</p>
            <p>• trend_stability: 100 - (CoV of 3wk rolling avg)</p>
            <p>&nbsp;&nbsp;- CoV = (stdDev / mean) * 100</p>
            <p>• Identifies if a team is improving, declining, or holding steady</p>
            <p>• trend_stability quantifies how volatile the trend is</p>
            <p>• Useful for projecting if recent performance will continue</p>
        </div>
        <div class="footer-text">
            <p><strong>Luck Score & Rating </strong></p>
            <p>• luck_score: 0-100 composite of luck factors</p>
            <p>&nbsp;&nbsp;- Base: 50</p>
            <p>&nbsp;&nbsp;- Quality Wins / Tough Losses: +/- 1-5 each</p>
            <p>&nbsp;&nbsp;- WAIL: +/- 8 per win above/below expected</p>
            <p>&nbsp;&nbsp;- Below Median Wins: + 4 each</p>
            <p>&nbsp;&nbsp;- Close Game Record: +/- 16 * (win% - 50%)</p>
            <p>• luck_rating: Qualitative rating based on luck_score</p>
            <p>• Quantifies how lucky or unlucky a team's results have been</p>
            <p>• Incorporates multiple factors for a comprehensive luck assessment</p>
        </div>
        <div class="footer-text">
            <p><strong>Future Strength of Schedule</strong></p>
            <p>• future_sos: Average points scored by remaining opponents</p>
            <p>• future_schedule: List of matchups + opp avg score</p>
            <p>• Measures the difficulty of a team's remaining schedule</p>
            <p>• Helpful for predicting how a team's performance may change</p>
            <p>• Higher future_sos implies a tougher remaining schedule</p>
        </div>
    </div>
""", unsafe_allow_html=True)

    def _css(self):
        st.markdown("""
            <style>
            /* Standard Card Styling */
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
            
            /* Trend Indicators */
            .trend-improving { color: #4CAF50; }
            .trend-declining { color: #f44336; }
            .trend-stable { color: #FFA726; }
            
            /* Luck-based Card Styling */
            .lucky-card { background-color: rgba(255, 99, 99, 0.15); }
            .very-lucky-card { background-color: rgba(255, 99, 99, 0.25); }
            .unlucky-card { background-color: rgba(99, 149, 255, 0.15); }
            .very-unlucky-card { background-color: rgba(99, 149, 255, 0.25); }
            .neutral-card { background-color: rgba(128, 128, 128, 0.15); }

            /* Title Cards Styling */
            .simple-card {
                padding: 20px;
                border-radius: 8px;
                margin: 10px 0;
                background-color: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            .fraud-card {
                border-left: 4px solid rgba(255, 99, 99, 0.5);
            }
            .robbed-card {
                border-left: 4px solid rgba(99, 149, 255, 0.5);
                margin-top: 30px;
            }
            .card-title {
                font-size: 24px;
                font-weight: bold;
                color: white;
                margin-bottom: 15px;
            }
            .card-subtitle {
                font-size: 18px;
                color: rgba(255, 255, 255, 0.9);
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            .card-section-title {
                font-size: 16px;
                font-weight: bold;
                color: white;
                margin: 20px 0 10px 0;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .card-stats {
                color: rgba(255, 255, 255, 0.9);
                line-height: 1.8;
                padding: 15px;
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 6px;
                font-size: 14px;
            }
            .card-text {
                color: rgba(255, 255, 255, 0.9);
                line-height: 1.6;
                padding: 15px;
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 6px;
                font-size: 14px;
                text-align: justify;
            }

            /* Profile Card Styling */
            .profile-card {
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 8px;
                padding: 20px;
                margin: 10px 0;
                text-align: center;
            }
            .profile-card h3 {
                color: white;
                margin-bottom: 10px;
                font-size: 18px;
            }
            .big-stat {
                font-size: 24px;
                font-weight: bold;
                color: white;
                margin: 15px 0;
            }
            .stat-detail {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                margin: 5px 0;
            }

            /* Footer Styling */
            .footer-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 20px;
                padding: 20px;
                border-radius: 8px;
            }
            .footer-text {
                flex-basis: calc(33.33% - 20px);
                padding: 15px;
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 6px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .footer-text p {
                margin-bottom: 10px;
            }
            .footer-text strong {
                color: white;
                font-size: 16px;
                display: block;
                margin-bottom: 10px;
            }
            </style>
        """, unsafe_allow_html=True)