# fantasy_football-drafting_model.py

1 - We are going to be coming up with a draft model for a snake draft. 

2 - We are going to be calculating something known as value over replacement for each player in the draft pool, and then sort them in descending order. This will be the basis of our ranking model. To begin this post, we'll talk about what value over replacement is and why it's actually really effective and ranking players for the draft. If I decide to make this thing a series, we'll also include ADP data in our final DataFrame and look for gaps in ADP rank and VOR rank (the point of this is that we'll be looking for bargains/steals).

3 - This draft model works for the standard, half-ppr, and ppr formats. I'll be working in PPR as that's my main league format, but this code here can easily be extended to the other formats.

4 - We are going to be scraping the data from FantasyPros. FantasyPros provides us two things that we need for our model - ADP data and projection. Moreover, the projection data hosted on Fantasypros is a combination of 4 different sources.

That's all the background info you need for now. Let's talk about VOR, what it is, and why you should use it.
