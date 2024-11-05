# Glizzy-FF-2024-Dashboard

To host the dashboard locally, input the following into Powershell. 
1. Navigate to the correct file directory first (in my case): cd C:\Users\hoon\Desktop
2. python -m streamlit run fantasy_dashboard.py

It should lead to this message:
      "Welcome to Streamlit!
      If you’d like to receive helpful onboarding emails, news, offers, promotions,
      and the occasional swag, please enter your email address below. Otherwise,
      leave this field blank."

The prompt you're seeing is Streamlit's first-time setup.
Skip the email signup:
  Just press Enter without typing anything. This will skip the email collection and launch your dashboard

________

**Current iteration as of 11:15 AM, 11/05/2024**

**PART 1 - CORE STATISTICAL CALCULATIONS**

1. Basic Statistics:

Avg PF (Points For):
- Raw mean of all weekly scores
- Purpose: Baseline measure of scoring power
- Limitation: Can be skewed by outliers
Example: Team scores [100, 100, 100, 180]
Avg PF = 120, but not representative of typical performance

Median PF:
- Middle value of all scores when ordered
- Purpose: Shows "typical" performance level
- Value: Less affected by outliers
Example: Same team [100, 100, 100, 180]
Median PF = 100, better shows usual performance

Mean-Median Gap:
- Calculation: Avg PF - Median PF
- Purpose: Identifies scoring distribution skew
- Interpretation:
  * Large Positive Gap: Some huge scoring weeks
  * Small Gap: Consistent scoring
  * Negative Gap: Few underperformance weeks
Example: 
[100, 100, 100, 180] → Gap = +20 (explosive)
[100, 105, 110, 115] → Gap = +2.5 (consistent)

2. Consistency Metrics:

Standard Deviation (StdDev):
- Measures score dispersion around mean
- Lower = more consistent
- Formula: sqrt(sum((x - mean)²)/n)

Consistency Rating:
- Based on StdDev thresholds:
  * High: StdDev ≤ 20
  * Medium: StdDev ≤ 25
  * Low: StdDev > 25
- Purpose: Simplified consistency indicator

Stability Score:
- Based on 3-week rolling averages
- Higher score = more stable performance
- Formula: 100 - (StdDev of rolling avg / Mean * 100)




________
**Raw Data**: https://docs.google.com/spreadsheets/d/1jzLBWRygK63oS8wwGxd1ciq2YtjBv9_dnUaAcAQEqpE/edit?gid=0#gid=0

**Week 1 - 9 Report**: https://docs.google.com/document/d/1zhu27Sl9BvwjwT5Eqkagxn2Lh7MejwqEAkzI0UYo3cM/edit?tab=t.0
