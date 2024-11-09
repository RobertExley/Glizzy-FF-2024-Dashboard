import streamlit as st

class DashboardUI():
    def __init__(self, dataPlotter):
        st.set_page_config(layout="wide", page_title="Fantasy Football Analytics")
        self._css()
        self.plotter = dataPlotter
        self.team_metrics = dataPlotter.get_team_metrics()
        self.num_weeks = dataPlotter.calculator.get_num_weeks()

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
        self._title_cards()
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
    def _title_cards(self):
        fraud_team = max(self.team_metrics, key=lambda x: x['actualWins'] - x['expectedWins'])
        robbed_team = min(self.team_metrics, key=lambda x: x['actualWins'] - x['expectedWins'])

        # Fraud Card
        st.markdown(f"""
            <div class="simple-card fraud-card">
                <div class="card-title">💩 Current League Fraud Title</div>
                <div class="card-subtitle">{fraud_team['name']} ({fraud_team['record']}): "The Variance King"</div>
                <div class="card-section-title">Statistical Evidence:</div>
                <div class="card-stats">
                • Expected Wins: {fraud_team['expectedWins']:.1f} vs Actual: {fraud_team['actualWins']} (WAIL: +{fraud_team['wail']:.1f})<br>
                • Luck Score: {fraud_team['luck_score']:.1f} ({fraud_team['luck_rating']})<br>
                • Only winning close games ({fraud_team['close_games_record']})<br>
                • {fraud_team['below_median_wins']} below-median wins<br>
                • High volatility (StdDev: {fraud_team['weeklyStdDev']:.1f})
                </div>
                <div class="card-section-title">Analysis:</div>
                <div class="card-text">
                gautamm represents the clearest case of overperformance in the league. While they maintain a respectable fractional record (56/81) showing some genuine skill, their success is heavily luck-inflated. They've won 2.6 more games than expected - the highest positive deviation in the league. Their perfect record in close games and three below-median wins suggest they're regularly escaping with victories they statistically shouldn't secure. The high standard deviation (29.0) indicates inconsistent performance being masked by fortunate timing.
                This combination of metrics suggests gautamm's 8-1 record is significantly inflated compared to their true performance level. While they're a good team (as evidenced by their fractional record), they should realistically be closer to 5-4 or 6-3 based on their actual performance quality.
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Robbed Card
        st.markdown(f"""
            <div class="simple-card robbed-card">
                <div class="card-title">😭 Current League Robbed Title</div>
                <div class="card-subtitle">{robbed_team['name']} ({robbed_team['record']}): "Mr. Hates Variance"</div>
                <div class="card-section-title">Statistical Evidence:</div>
                <div class="card-stats">
                • League-best Average PF ({robbed_team['avgPF']:.1f})<br>
                • Expected Wins: {robbed_team['expectedWins']:.1f} vs Actual: {robbed_team['actualWins']} (WAIL: {robbed_team['wail']:.1f})<br>
                • Luck Score: {robbed_team['luck_score']:.1f} ({robbed_team['luck_rating']})<br>
                • Losing close games ({robbed_team['close_games_record']})<br>
                • High Consistency Rating (StdDev: {robbed_team['weeklyStdDev']:.1f})<br>
                • Strong Fractional Record ({robbed_team['fractional_record']['total_wins']}/{robbed_team['fractional_record']['total_wins'] + robbed_team['fractional_record']['total_losses']})
                </div>
                <div class="card-section-title">Analysis:</div>
                <div class="card-text">
                hooghost presents the strongest case for being "robbed" in the league. They lead in average points scored (150.1) with high consistency (StdDev: 18.6), yet sit at a middling 5-4 record. Their expected wins (6.8) versus actual wins (5.0) shows they're significantly underperforming their true level. The "Very Unlucky" luck score of 28.9 quantifies this misfortune.
                Their strong fractional record (56/81, tied for best in league) demonstrates they're consistently outperforming most teams, yet their record doesn't reflect this dominance. Their losing record in close games (1-2) further emphasizes how bounces aren't going their way in critical moments.
                This combination of league-leading scoring, high consistency, and poor luck metrics makes hooghost the clear choice for most "robbed" team. Their 5-4 record severely understates their true performance level, which is more befitting of a 7-2 or 8-1 team.
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
            /* Regular card styles */
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
            .trend-improving { color: #4CAF50; }
            .trend-declining { color: #f44336; }
            .trend-stable { color: #FFA726; }
            .lucky-card { background-color: rgba(255, 99, 99, 0.15); }
            .very-lucky-card { background-color: rgba(255, 99, 99, 0.25); }
            .unlucky-card { background-color: rgba(99, 149, 255, 0.15); }
            .very-unlucky-card { background-color: rgba(99, 149, 255, 0.25); }
            .neutral-card { background-color: rgba(128, 128, 128, 0.15); }

            /* Simple Title Cards Styling */
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

            .footer-text {
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                margin-top: 30px;
            }
            </style>
        """, unsafe_allow_html=True)
