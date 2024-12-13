# Glizzy-FF-2024-Dashboard

To host the dashboard locally, input the following into Powershell. 
1. Navigate to the correct file directory first (in my case): cd C:\Users\hoon\Desktop
2. pip install -r requirements.txt
3. python -m streamlit run fantasy_dashboard_02.py

It should lead to this message:
      "Welcome to Streamlit!
      If you’d like to receive helpful onboarding emails, news, offers, promotions,
      and the occasional swag, please enter your email address below. Otherwise,
      leave this field blank."

The prompt you're seeing is Streamlit's first-time setup.
Skip the email signup:
  Just press Enter without typing anything. This will skip the email collection and launch your dashboard

________

**Current iteration as of 11/09/24**

**Updates**
- Modified expected wins calculations
- Added League Median line to weekly trend chart
- Fractional wins used as modifiers for Expected Wins, Luck Score, and Performance Score.
- Fractional wins visualizer
- League Fraud & Robbed Cards added
- complete refactor. there are now three packages -- data_collector, calculator, and renderer (which included plotter and layout). using these will make it way easier to add metrics or anything else in the future and keep developing. developers can just use the functions without thinking about each step. i will add documentation as to what each ones output looks like soon
- use api calls to future proof -> zero need to manually input any data (other than league ID)
- can support any sleeper league (see global var in fantasy_dashboard)
- re-did code logic around fractional records to make it more similar to other metrics
- way more readable now, broken up into parts
- fixed some issues with previous data that were a result of manual data entry
- added requirements.txt and gitignore

________
**Model info (WIP. Will complete once the model finds itself in a more optimal place before Week 10)**


________
**Raw Data**: https://docs.google.com/spreadsheets/d/1jzLBWRygK63oS8wwGxd1ciq2YtjBv9_dnUaAcAQEqpE/edit?gid=0#gid=0

**Week 1 - 9 Report**: https://docs.google.com/document/d/1zhu27Sl9BvwjwT5Eqkagxn2Lh7MejwqEAkzI0UYo3cM/edit?tab=t.0
