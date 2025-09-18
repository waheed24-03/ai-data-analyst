import re
import pandas as pd
import matplotlib.pyplot as plt

def intent_override(user_query: str, df: pd.DataFrame, mode: str) -> str | None:
    """
    Deterministic overrides for very common / high-value cricket queries.
    Returns a Python code string (to be executed in executor).
    """

    q = user_query.lower().strip()

    # ------------------- Batting / Toss -------------------
    if ("bat" in q and "first" in q and "most" in q) and mode == "visualize":
        return """
# Count how many times each toss winner chose to bat
bat_first = df[df['Toss Decision'].str.contains('bat', case=False, na=False)]['Toss Winner'].value_counts().sort_values(ascending=False)
plt.figure(figsize=(10,6))
bat_first.plot(kind='bar', edgecolor='black')
plt.title('Teams Choosing to Bat First Most Often')
plt.ylabel('Count')
plt.xlabel('Team')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
if len(bat_first) > 0:
    result = f"The team that chose to bat first most often is {bat_first.idxmax()} ({bat_first.max()} times)."
else:
    result = 'No data to determine the team that chose to bat first most.'
"""

    # ------------------- Best Batting Stadium -------------------
    if ("best" in q and "batting" in q and "stadium" in q) and mode in ("summarize", "analyze"):
        return """
# Compute best batting stadium by average combined score across matches
sd = df.copy()
sd['Score A'] = pd.to_numeric(sd.get('Score A'), errors='coerce')
sd['Score B'] = pd.to_numeric(sd.get('Score B'), errors='coerce')
sd = sd[~(sd['Score A'].isna() & sd['Score B'].isna())]
if 'Stadium' in sd.columns:
    avg_scores = sd.groupby('Stadium')[['Score A', 'Score B']].mean()
    avg_scores = avg_scores.fillna(0)
    avg_scores['Total Avg'] = avg_scores['Score A'] + avg_scores['Score B']
    if not avg_scores.empty:
        best_stadium = avg_scores['Total Avg'].idxmax()
        top_score = avg_scores['Total Avg'].max()
        result = f"The best batting stadium is {best_stadium} with an average combined match score of {top_score:.1f} runs."
    else:
        result = "Not enough data to determine the best batting stadium."
else:
    result = "Dataset does not include a 'Stadium' column."
"""

    # ------------------- Man of the Match -------------------
    if ("man of the match" in q or "man of match" in q or "mom" in q) and mode == "visualize":
        return """
# Robust counting of Man of the Match awards by team and player
if 'Wining Team' in df.columns and 'Man of the Match' in df.columns:
    mom_counts = df.groupby(['Wining Team', 'Man of the Match']).size().reset_index(name='Awards')
    if mom_counts.empty:
        result = "No Man of the Match records found."
    else:
        mom_counts['Label'] = mom_counts['Wining Team'].astype(str) + ' - ' + mom_counts['Man of the Match'].astype(str)
        mom_counts = mom_counts.sort_values('Awards', ascending=False)
        top_n = 30
        mom_plot = mom_counts.head(top_n).copy()
        plt.figure(figsize=(14,6))
        plt.bar(mom_plot['Label'].astype(str), mom_plot['Awards'], edgecolor='black')
        plt.xticks(rotation=90, ha='right')
        plt.ylabel('Number of Man of the Match Awards')
        plt.xlabel('Team - Player')
        plt.title('Top Players Receiving Man of the Match Awards (by Team)')
        plt.tight_layout()
        plt.show()
        max_awards = mom_plot['Awards'].max()
        top_rows = mom_plot[mom_plot['Awards'] == max_awards]
        tied_players = ", ".join(top_rows['Man of the Match'] + " (" + top_rows['Wining Team'] + ")")
        result = f"Top: {tied_players} — {max_awards} awards each."
else:
    result = "Required columns ('Wining Team' and/or 'Man of the Match') not present in dataset."
"""

    # ------------------- Best Bowler -------------------
    if ("best bowler" in q or "top bowler" in q) and mode in ("summarize", "analyze", "visualize"):
        return """
# Compute best bowler by wickets taken
possible_cols = [c for c in df.columns if re.search(r'wickets|wkt', c, flags=re.I)]
if possible_cols:
    col = possible_cols[0]
    bowler_stats = df.groupby('Bowler')[col].sum().sort_values(ascending=False)
    plt.figure(figsize=(12,6))
    bowler_stats.head(10).plot(kind='bar', edgecolor='black')
    plt.title('Top 10 Bowlers by Wickets')
    plt.ylabel('Wickets')
    plt.xlabel('Bowler')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    result = f"Best bowler is {bowler_stats.idxmax()} with {bowler_stats.max()} wickets."
else:
    result = "Dataset does not contain bowler/wickets information."
"""

    # ------------------- Most Sixes -------------------
    if ("most sixes" in q or "six hits" in q) and mode in ("summarize", "analyze", "visualize"):
        return """
# Compute most sixes by player or team
possible_cols = [c for c in df.columns if re.search(r'sixes|six', c, flags=re.I)]
if possible_cols:
    col = possible_cols[0]
    six_stats = df.groupby('Batsman')[col].sum().sort_values(ascending=False)
    plt.figure(figsize=(12,6))
    six_stats.head(10).plot(kind='bar', edgecolor='black')
    plt.title('Top 10 Six Hitters')
    plt.ylabel('Sixes')
    plt.xlabel('Batsman')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    result = f"Player with most sixes: {six_stats.idxmax()} ({six_stats.max()} sixes)."
else:
    result = "Dataset does not contain sixes information."
"""

    # ------------------- Toss vs Match Win -------------------
    if ("toss" in q and "win" in q and "match" in q) and mode in ("summarize", "analyze", "visualize"):
        return """
# Compare toss winner vs match winner
if 'Toss Winner' in df.columns and 'Wining Team' in df.columns:
    correct = (df['Toss Winner'] == df['Wining Team']).sum()
    total = len(df)
    plt.figure(figsize=(6,6))
    plt.bar(['Toss == Match Win','Toss != Match Win'], [correct, total-correct], color=['green','red'], edgecolor='black')
    plt.title('Toss Winner vs Match Winner')
    plt.ylabel('Number of Matches')
    plt.tight_layout()
    plt.show()
    pct = correct/total*100 if total>0 else 0
    result = f"Toss winner won the match {pct:.1f}% of the time."
else:
    result = "Dataset does not have Toss Winner or Wining Team columns."
"""
    
    # ------------------- NEW: Total Extras Given -------------------
    if "extra" in q and ("how many" in q or "total" in q or "show visually" in q):
        return """
# Check if the required columns exist in the DataFrame
if 'Extras A' in df.columns and 'Extras B' in df.columns:
    # Calculate the total sum of extras for each column
    total_extras_A = df['Extras A'].sum()
    total_extras_B = df['Extras B'].sum()

    # Prepare data for plotting
    teams = ['Extras by Team A', 'Extras by Team B']
    totals = [total_extras_A, total_extras_B]

    # Create a clean and clear bar chart
    plt.figure(figsize=(8, 6))
    bars = plt.bar(teams, totals, color=['#1f77b4', '#ff7f0e'], edgecolor='black')
    plt.title('Total Extras Conceded by Each Team')
    plt.ylabel('Total Extra Runs')

    # Add text labels on top of each bar for clarity
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center') 
    
    plt.tight_layout()
    plt.show()

    # Create a clear, informative summary string for the result
    result = f"Across all matches, Team A conceded a total of {total_extras_A} extras, and Team B conceded a total of {total_extras_B} extras."
else:
    result = "The dataset does not contain the required 'Extras A' and 'Extras B' columns to calculate total extras."
"""

    return None