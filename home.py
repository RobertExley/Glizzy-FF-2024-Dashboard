from calculator.calculator import SleeperMetricsCalculator
from data_collector.data_collector import SleeperDataCollector
from renderer.layout import DashboardUI
from renderer.plotter import DataPlotter
import streamlit as st

LEAGUE_ID = '1124814690363400192'

st.set_page_config(
    page_title="Fantasy Football Analytics",
    page_icon="🏈",
    layout="wide",
)

# Initialize session state if needed
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    
def load_data():
    if not st.session_state.data_loaded:
        # Get any data that is needed
        sleeperData = SleeperDataCollector(LEAGUE_ID)

        # Weekly matchups data and raw scores
        all_weekly_matchups, weekly_scores = sleeperData.get_all_weekly_matchups_and_scores()

        # Get current week
        current_week = sleeperData.get_current_week()

        # Split matchups into past and future
        past_weekly_matchups, future_weekly_matchups = sleeperData.split_weekly_matchups(all_weekly_matchups, current_week)

        # Calculate metrics
        calculator = SleeperMetricsCalculator(
            weekly_scores=weekly_scores,
            past_weekly_matchups=past_weekly_matchups,
            future_weekly_matchups=future_weekly_matchups,
            fractional_wins=sleeperData.get_weekly_fractional_records(weekly_scores=weekly_scores),
            actual_wins=sleeperData.get_wins()
        )

        # Store in session state
        st.session_state.calculator = calculator
        st.session_state.usernames = sleeperData.get_usernames()
        st.session_state.data_loaded = True

def main():
    # Load data
    load_data()

    st.title('Fantasy Football Analytics Dashboard')
    st.markdown("""
    Welcome to the Fantasy Football Analytics Dashboard! This dashboard provides comprehensive analysis 
    of your fantasy football league's performance metrics, trends, and insights.
    """)

    if st.session_state.data_loaded:
        # Plot metrics
        plotter = DataPlotter(calculator=st.session_state.calculator, usernames=st.session_state.usernames)

        # Build dashboard
        dashboard = DashboardUI(plotter)
        dashboard.render()

if __name__ == "__main__":
    main()