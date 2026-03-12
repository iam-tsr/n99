import re

movie_titles = ['The Kerala Story 2: Goes Beyond (UA16+)', 'Ishqan De Lekhe (UA13+)', "O' Romeo (A)", 'Mardaani 3 (UA16+)', 'Dhurandhar (A)', 'Hoppers (UA 7+)', 'Assi (A)', 'Border 2 (UA13+)']

def clean_titles(titles):
    cleaned_titles = [re.sub(r'\(.*?\)', '', title).strip().upper() for title in titles]
    return cleaned_titles

cleaned_titles = clean_titles(movie_titles)
print(cleaned_titles)