import numpy as np
class SleeperMetricsCalculator:
    def __init__(self, weekly_scores, past_weekly_matchups, future_weekly_matchups, fractional_wins, actual_wins):
        self.weekly_scores = weekly_scores
        self.past_weekly_matchups = past_weekly_matchups
        self.future_weekly_matchups = future_weekly_matchups
        self.fractional_wins = fractional_wins
        self.actual_wins = actual_wins
        self.num_weeks = len(next(iter(self.weekly_scores.values())))
    
    def _get_opponent_for_week(self, team, week, matchups_dict):
        """Get a team's opponent for a specific week"""
        matchups = matchups_dict[week]
        for matchup in matchups:
            if team in matchup:
                return matchup[0] if matchup[1] == team else matchup[1]
        return None
    
    def get_num_weeks(self):
        return self.num_weeks

    def get_weekly_scores(self):
        return self.weekly_scores
    
    def get_fractional_wins(self):
        return self.fractional_wins

    def calculate_enhanced_expected_wins(self, name):
        """Calculate expected wins using fractional data to weigh performance quality"""
        weekly_medians = []
        adjusted_wins = 0
        scores = self.weekly_scores[name]
        
        # Calculate weekly medians
        for week in range(self.num_weeks):
            week_scores = [team_scores[week] for team_scores in self.weekly_scores.values()]
            weekly_medians.append(np.median(week_scores))
            
            # Get fractional score for the week
            fractional_score = self.fractional_wins[name][week]
            
            if scores[week] > weekly_medians[week]:
                # Above median: weight by how impressive the performance was
                quality_modifier = (fractional_score / self.num_weeks)  # Scale of 0 to 1
                adjusted_wins += 0.7 + (0.3 * quality_modifier)  # Base win (0.7) plus quality bonus
            else:
                # Below median: partial credit based on how close they were
                quality_modifier = (fractional_score / self.num_weeks)  # Scale of 0 to 1
                adjusted_wins += 0.3 * quality_modifier  # Partial credit for strong below-median performance
        
        return round(adjusted_wins, 1)

    def calculate_enhanced_luck_score(self, team_name):
        """Calculate luck score incorporating quality wins and tough losses"""
        scores = self.weekly_scores[team_name]
        team_median = np.median(scores)
        
        base_score = 50
        luck_adjustments = []
        below_median_wins = 0
        close_games_won = 0
        close_games_lost = 0
        
        for week in range(self.num_weeks):
            opponent = self._get_opponent_for_week(team_name, week + 1, self.past_weekly_matchups)
            team_score = scores[week]
            opp_score = self.weekly_scores[opponent][week]
            fractional_score = self.fractional_wins[team_name][week]
            
            won_game = team_score > opp_score
            
            if won_game:
                if team_score < team_median:
                    below_median_wins += 1
                    
                # Quality win analysis
                if fractional_score <= 3:  # Won despite low fractional score
                    luck_adjustments.append(5)  # Lucky win
                elif fractional_score >= 7:  # Won with high fractional score
                    luck_adjustments.append(-1)  # Expected win
            else:
                # Tough loss analysis
                if fractional_score >= 7:  # Lost despite high fractional score
                    luck_adjustments.append(-5)  # Very unlucky
                elif fractional_score <= 3:  # Lost with low fractional score
                    luck_adjustments.append(1)  # Expected loss
            
            # Track close games
            if abs(team_score - opp_score) < 10:
                if won_game:
                    close_games_won += 1
                else:
                    close_games_lost += 1
        
        # Calculate expected wins
        expected_wins = self.calculate_enhanced_expected_wins(team_name)
        wail = self.actual_wins[team_name] - expected_wins
        
        # Combine all luck components
        luck_score = base_score
        luck_score += sum(luck_adjustments)  # Quality wins/tough losses impact
        luck_score += (wail * 8)  # WAIL impact
        luck_score += (below_median_wins * 4)  # Below median wins impact
        
        # Close games impact
        if (close_games_won + close_games_lost) > 0:
            close_game_ratio = close_games_won / (close_games_won + close_games_lost)
            luck_score += ((close_game_ratio - 0.5) * 16)
        
        luck_score = max(0, min(100, luck_score))
        
        return {
            'luck_score': round(luck_score, 1),
            'luck_rating': 'Very Lucky' if luck_score > 70 else
                        'Lucky' if luck_score > 60 else
                        'Slightly Lucky' if luck_score > 55 else
                        'Very Unlucky' if luck_score < 30 else
                        'Unlucky' if luck_score < 40 else
                        'Slightly Unlucky' if luck_score < 45 else
                        'Neutral',
            'close_games_record': f"{close_games_won}-{close_games_lost}",
            'below_median_wins': below_median_wins
        }

    def calculate_performance_score(self, name):
        """Calculate performance score using fractional data as quality modifier"""
        scores = self.weekly_scores[name]
        mean = np.mean(scores)
        std_dev = np.std(scores)
    
        
        # Base components
        max_avg_points = max(np.mean(team_scores) for team_scores in self.weekly_scores.values())
        base_points_score = (mean / max_avg_points) * 100
        win_score = (self.actual_wins[name] / self.num_weeks) * 100
        consistency_score = 100 - ((std_dev / 30) * 100)
        
        # Calculate quality of points using fractional data
        weekly_quality_scores = []
        for week in range(self.num_weeks):
            fractional_score = self.fractional_wins[name][week]
            quality_modifier = fractional_score / self.num_weeks  # Scale of 0 to 1
            weekly_quality_scores.append(quality_modifier)
        
        avg_quality = np.mean(weekly_quality_scores)
        quality_adjusted_points = base_points_score * (0.7 + (0.3 * avg_quality))
        
        # Final weighted score
        perf_score = (
            (quality_adjusted_points * 0.50) +  # Points scored with quality adjustment
            (win_score * 0.30) +                # Actual wins
            (consistency_score * 0.20)          # Consistency
        )
        
        return round(perf_score, 1)

    def calculate_future_sos(self, team_name):
        """Calculate strength of future schedule"""
        future_opponents = []
        for week in range(10, 15):
            opponent = self._get_opponent_for_week(team_name, week, self.future_weekly_matchups)
            future_opponents.append(opponent)
        
        opponent_avgs = [np.mean(self.weekly_scores[opp]) for opp in future_opponents]
        league_avg = np.mean([np.mean(scores) for scores in self.weekly_scores.values()])
        
        return {
            'future_sos': round(np.mean(opponent_avgs), 2),
            'vs_league_avg': round(np.mean(opponent_avgs) - league_avg, 2),
            'week_by_week': [(week, opp, round(np.mean(self.weekly_scores[opp]), 2)) 
                            for week, opp in zip(range(10, 15), future_opponents)]
        }

    def calculate_fractional_record(self, name):
        return {
            "total_wins": sum(self.fractional_wins[name]),
            "total_losses": (self.num_weeks * (len(self.weekly_scores) - 1)) - sum(self.fractional_wins[name])
        }

    def calculate_metrics(self, name):
        """Calculate all metrics for a team"""
        scores = self.weekly_scores[name]
        mean = np.mean(scores)
        median = np.median(scores)
        std_dev = np.std(scores)
        
        # Calculate trend metrics
        rolling_avg = []
        for i in range(len(scores)-2):
            avg = np.mean(scores[i:i+3])
            rolling_avg.append(avg)
        
        recent_trend = np.polyfit(range(4), scores[-4:], 1)[0]
        
        if abs(recent_trend) < 2:
            trend = 'Stable'
        elif recent_trend > 0:
            trend = 'Improving'
        else:
            trend = 'Declining'
        
        stability = 100 - (np.std(rolling_avg) / np.mean(rolling_avg) * 100)
        
        consistency_rating = (
            'High' if std_dev <= 20 else
            'Medium' if std_dev <= 25 else
            'Low'
        )
        
        enhanced_expected_wins = self.calculate_enhanced_expected_wins(name)
        wail = self.actual_wins[name] - enhanced_expected_wins
        perf_score = self.calculate_performance_score(name)
        luck_metrics = self.calculate_enhanced_luck_score(name)
        future_metrics = self.calculate_future_sos(name)
        fractional_record = self.calculate_fractional_record(name)
        
        return {
            'name': name,
            'record': f"{self.actual_wins[name]}-{self.num_weeks-self.actual_wins[name]}",
            'avgPF': round(mean, 2),
            'medianPF': round(median, 2),
            'mean_median_gap': round(mean - median, 2),
            'expectedWins': enhanced_expected_wins,
            'actualWins': self.actual_wins[name],
            'wail': round(wail, 2),
            'weeklyStdDev': round(std_dev, 1),
            'consistency': consistency_rating,
            'trend': trend,
            'trend_stability': round(stability, 1),
            'perfScore': perf_score,
            'luck_score': luck_metrics['luck_score'],
            'luck_rating': luck_metrics['luck_rating'],
            'close_games_record': luck_metrics['close_games_record'],
            'below_median_wins': luck_metrics['below_median_wins'],
            'future_sos': future_metrics['future_sos'],
            'future_schedule': future_metrics['week_by_week'],
            'fractional_record': fractional_record
        }
    
    def calculate_metrics_all_teams(self):
        team_metrics =  [
            self.calculate_metrics(name) for name, scores in self.weekly_scores.items()
        ]
        team_metrics.sort(key=lambda x: x['perfScore'], reverse=True)
        return team_metrics
