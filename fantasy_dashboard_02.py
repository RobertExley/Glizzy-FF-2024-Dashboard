from calculator.calculator import SleeperMetricsCalculator
from data_collector.data_collector import SleeperDataCollector
from renderer.layout import DashboardUI
from renderer.plotter import DataPlotter

LEAGUE_ID = '1124814690363400192' # Set this to your league

def main():

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

    # Plot metrics
    plotter = DataPlotter(calculator=calculator, usernames=sleeperData.get_usernames())

    # Build dashboard
    dashboard = DashboardUI(plotter)
    dashboard.render()

if __name__=="__main__":
    main()