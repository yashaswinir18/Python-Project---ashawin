import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

#scrape movie data from IMDb based on genre
def scrape_data(genre):

    url = f'https://www.imdb.com/search/title/?genres={genre.lower()}'

    try:
        response = requests.get(url)
        response.raise_for_status()  #  exception if there's an HTTP error
    except requests.exceptions.RequestException as e:
        print(e)
        print('exception occured')
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract movie data
    movie_data = []
    for movie in soup.find_all('div', class_='lister-item'):
        title = movie.find('h3', class_='lister-item-header').a.text
        movie_data.append({'Title': title})
    return movie_data

# save movie data to a CSV file
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Frecommend a movie based on genre
def recommend_movie(data):
    if not data:
        return "No movies found for this genre."
    recommended_movie = random.choice(data)
    return recommended_movie

if __name__ == "__main__":
    print("* Movie Suggestion App *")

    while True:
        user_genre = input("Enter a movie genre: ")
        scraped_data = scrape_data(user_genre)

        if scraped_data is None:
            print("Error: Failed to fetch movie data.")
        else:
            save_to_csv(scraped_data, 'movie_data.csv')
            movie_data = pd.read_csv('movie_data.csv')

            recommended_movie = recommend_movie(scraped_data)
            print("Recommended Movie:")
            print(f"Title: {recommended_movie['Title']}")

            another = input("Do you want another recommendation? (y/n): ")
            if another.lower() != "y":
                break

