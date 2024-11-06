# Glizzy-FF-2024-Dashboard

To host the dashboard locally, input the following into Powershell. 
1. Navigate to the correct file directory first (in my case): cd C:\Users\hoon\Desktop
2. python -m streamlit run fantasy_dashboard_02.py

It should lead to this message:
      "Welcome to Streamlit!
      If you’d like to receive helpful onboarding emails, news, offers, promotions,
      and the occasional swag, please enter your email address below. Otherwise,
      leave this field blank."

The prompt you're seeing is Streamlit's first-time setup.
Skip the email signup:
  Just press Enter without typing anything. This will skip the email collection and launch your dashboard

________

**Current iteration as of 6:31am, 11/06/24**

**Updates**
- Modified expected wins calculations
- Added League Median line to weekly trend chart
- Fractional wins used as modifiers for Expected Wins, Luck Score, and Performance Score.
________

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

**PART 2 - PERFORMANCE METRICS (UPDATED)**

Base Expected Wins:
- Still start by counting weeks above median
- Example: 6 base expected wins

Mean-Median Gap Adjustment:
- Looks at the pattern of your scoring
- If you have big explosive weeks (positive gap):
      - Example: Scores like [100, 100, 100, 180]
      - Mean = 120, Median = 100, Gap = +20
      - System thinks "These explosive weeks might not continue"
      - Slightly reduces your expected wins
-If you have occasional bad weeks (negative gap):
      - Example: Scores like [120, 120, 120, 80]
      - Mean = 110, Median = 120, Gap = -10
      - System thinks "You're better than your bad weeks show"
      - Slightly increases your expected wins

Consistency Bonus/Penalty:
- Rewards teams that score reliably
- Penalizes teams that are unpredictable
- Example:
      - Team A: [100, 102, 98, 101] = Very consistent = Small bonus
      - Team B: [140, 80, 130, 70] = Very volatile = Small penalty

Final Number:
- Combines all these factors
- Results in decimal places to show detail
- Example: 5.2 Expected Wins means:
      - Base: Maybe 6 weeks above median
      - But: Some wins came from explosive weeks
      - And: Showing some inconsistency
      - So: System expects slight regression

Why This Matters:
- More accurate prediction of "deserved" wins
- Helps identify teams likely to improve or decline
- Better at spotting lucky/unlucky teams

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

Mean-Median Gap Adjustments:


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
