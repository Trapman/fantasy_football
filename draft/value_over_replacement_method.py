"""
Our first step is to find our replacement players. We'll find this using ADP data provided by FantasyPros. We have to scrape this data. 
We'll be working with PPR data
"""

from bs4 import BeautifulSoup as BS
import requests

BASE_URL = "https://www.fantasypros.com/nfl/adp/ppr-overall.php"

def make_adp_df():
    res = requests.get(BASE_URL)
    if res.ok:
        soup = BS(res.content, 'html.parser')
        table = soup.find('table', {'id': 'data'})
        df = pd.read_html(str(table))[0]
        print('Output after reading the html:\n\n', df.head(), '\n') # so you can see the output at this point
        df = df[['Player Team (Bye)', 'POS', 'AVG']]
        print('Output after filtering:\n\n', df.head(), '\n')
        df['PLAYER'] = df['Player Team (Bye)'].apply(lambda x: ' '.join(x.split()[:-2])) # removing the team and position
        df['POS'] = df['POS'].apply(lambda x: x[:2]) # removing the position rank
        
        df = df[['PLAYER', 'POS', 'AVG']].sort_values(by='AVG')
        
        print('Final output: \n\n', df.head())
        
        return df
        
    else:
        print('oops, something didn\'t work right', res.status_code)
        
df = make_adp_df()

"""
What we need now is to cutoff our df at 100, and find the last RB, QB, TE, and WR chosen up to that point (on average),
and append them to a dictionary we'll call replacement_players.
"""

replacement_players = {
    'RB': '',
    'WR': '',
    'TE': '',
    'QB': ''
}

for _, row in df[:100].iterrows():
    position = row['POS']
    player = row['PLAYER']
    replacement_players[position] = player

"""
Now that we have our replacement players, we have to get projection data. We're going to scrape PPR projection data from FantasyPros, 
and then replace the player name values in our dicitonary with their projected points.
"""

# each position has a different associated URL. We'll create a string format here and loop through the possible positions
BASE_URL = 'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft'

def make_projection_df():
    
    # we are going to concatenate our individual position dfs into this larger final_df
    final_df = pd.DataFrame()
    
    #url has positions in lower case
    for position in ['rb', 'qb', 'te', 'wr']:
        
        res = requests.get(BASE_URL.format(position=position)) # format our url with the position
        if res.ok:
            soup = BS(res.content, 'html.parser')
            table = soup.find('table', {'id': 'data'})
            df = pd.read_html(str(table))[0]
            
            df.columns = df.columns.droplevel(level=0) # our data has a multi-level column index. The first column level is useless so let's drop it.
            df['PLAYER'] = df['Player'].apply(lambda x: ' '.join(x.split()[:-1])) # fixing player name to not include team
            # if you're not doing PPR, don't include this. If you're doing Half PPR,
            # multiply receptions * 1/2
            if 'REC' in df.columns:
                df['FPTS'] = df['FPTS'] + df['REC'] # add receptions if they're in there. 
            
            df['POS'] = position.upper() # add a position column
            
            df = df[['PLAYER', 'POS', 'FPTS']]
            final_df = pd.concat([final_df, df]) # iteratively add to our final_df
        else:
            print('oops something didn\'t work right', res.status_code)
            return
    
    final_df = final_df.sort_values(by='FPTS', ascending=False) # sort df in descending order on FPTS column
    
    return final_df
            
df = make_projection_df()
df.head()

"""
So we have replacement players, we have projected points, what's left to do now is calculate our replacement values for each 
position from our replacement_players dictionary, 
and then calculate a new column for our final df called VOR, and sort that table in descending order.
"""
replacement_values = {
    'RB': 0,
    'WR': 0,
    'QB': 0,
    'TE': 0
}

for position, player in replacement_players.items():
    replacement_values[position] = df.loc[df['PLAYER'] == player].values[0, -1]
    
replacement_values
