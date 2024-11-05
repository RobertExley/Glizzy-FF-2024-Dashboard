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

**PART 2 - PERFORMANCE METRICS**

Expected Wins:
- Count of weeks scoring above league median
- Purpose: Shows deserved wins based on scoring
- Formula: Sum of (Score > Weekly League Median)

WAIL (Wins Above Index Level):
- Actual Wins minus Expected Wins
- Purpose: Measures luck in win/loss record
- Interpretation:
  * Positive: Winning more than deserved
  * Negative: Winning less than deserved
  * Near Zero: Fair record

Below Median Wins:
- Wins when scoring below team's median
- Purpose: Identifies "lucky" wins
- High number suggests unsustainable success

Close Games:
- Games decided by <10 points
- Format: Wins-Losses in close games
- Purpose: Shows performance in tight matchups
- Helps identify luck vs skill in critical games

Performance Score (0-100):
- Composite rating using:
  * 45% Points Score (Avg PF vs League Max)
  * 35% Win Score (Win % * 100)
  * 20% Consistency Score (100 - StdDev impact)
- Purpose: Overall team quality metric

**PART 3 - LUCK AND FUTURE METRICS**

Luck Score (0-100):
Base 50 points, adjusted by:
1. WAIL Impact (±10 per win differential)
2. Below Median Wins (±7 per occurrence)
3. Close Game Record Impact (±10 max)
4. Mean-Median Gap Impact (±5)

Final Luck Rating:
- Very Lucky: >70
- Lucky: >60
- Slightly Lucky: >55
- Neutral: 45-55
- Slightly Unlucky: <45
- Unlucky: <40
- Very Unlucky: <30

Future SoS (Strength of Schedule):
- Average points of future opponents
- Compared to league average
- Shows upcoming schedule difficulty


**PART 4 - METRIC INTERACTIONS**

Key Interaction Patterns:

1. Consistency Cascade:
StdDev → Consistency Rating → Stability Score
- All measure variability differently
- Each adds context to team reliability

2. Luck Triangle:
WAIL + Close Games + Below Median Wins
- Together show if success is sustainable
- High values in all three = very lucky

3. Performance Validation:
Avg PF + Median PF + Mean-Median Gap
- Together show true scoring level
- Large gaps suggest unsustainable peaks

4. Future Projection Factors:
Stability + Luck Score + Future SoS
- Predicts likely performance changes
- Helps identify regression candidates

Example Analysis Flow:
Team A:
- High Avg PF but larger Mean-Median Gap
  → Scoring power but inconsistent
- Positive WAIL and many Below Median Wins
  → Currently overperforming
- Tough Future SoS
  → Likely regression incoming

Team B:
- Lower Avg PF but small Mean-Median Gap
  → Consistent but lower scoring
- Negative WAIL but good in Close Games
  → Possibly underperforming
- Easy Future SoS
  → Potential improvement ahead

________
**Raw Data**: https://docs.google.com/spreadsheets/d/1jzLBWRygK63oS8wwGxd1ciq2YtjBv9_dnUaAcAQEqpE/edit?gid=0#gid=0

**Week 1 - 9 Report**: https://docs.google.com/document/d/1zhu27Sl9BvwjwT5Eqkagxn2Lh7MejwqEAkzI0UYo3cM/edit?tab=t.0
