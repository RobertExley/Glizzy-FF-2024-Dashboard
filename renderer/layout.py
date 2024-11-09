import streamlit as st

class DashboardUI():
    def __init__(self, dataPlotter):
        st.set_page_config(layout="wide", page_title="Fantasy Football Analytics")
        self._css()
        self.plotter = dataPlotter
        self.team_metrics = dataPlotter.get_team_metrics()

    def render(self):
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

    def _css(self):
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


