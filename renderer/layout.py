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
            <div class="footer-text">
                <p><strong>Metrics Explanation:</strong></p>
                <p>• Mean-Median Gap shows scoring distribution skew</p>
                <p>• Below Median Wins indicates unsustainable success</p>
                <p>• Trend shows recent performance direction</p>
                <p>• Stability Score (0-100) shows performance consistency</p>
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
            .footer-text {
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                margin-top: 30px;
            }
            </style>
        """, unsafe_allow_html=True)