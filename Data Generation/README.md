### Data Generation Methods

Our Data Generation Was Conducted using 2 external tools:
  1) The RiotGames API provided by Riot Games, the developers of League of Legends
  2) Cassiopeia, a third party tool developed as a wrapper for the RiotGames API to make it easier to work with

We created 3 scripts for our data collection
  - 2 of these scripts, collect_matches_recursive.py and collect_matches_sequential.py, were used to generate matchFiles, generic files       that contained match data stored using pickle https://docs.python.org/3/library/pickle.html
  - The final script, load_matches.py, loaded the relevent match data from a matchFile into a csv file for easy importing into a jupyter  
    notebook using pandas dataframes
