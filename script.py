import requests
from random import randint
from bs4 import BeautifulSoup

class MovieSelector:
    def __init__(self):
        self.movies = [] # resulting list of lists containing the top movies

    def __compare_movies(self, movie):
        return movie[2] # custom comparator

    def __valid_year(self, year):
        if len(year) < 6: return False
        year = year[1:5] # converting to valid format
        # checks if the given string represents a year
        for c in year:
            if c < '0' or c > '9': return False

        return True

    def __scrape_top_rated_movies(self):
        url = "https://www.imdb.com/chart/top/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
 
        movie_tags = soup.select("td.titleColumn a")
        year_tags = soup.select("td.titleColumn span[class=secondaryInfo]")
        rating_tags = soup.select("td.posterColumn span[name=ir]")

        movie_titles = [tag.text.strip() for tag in movie_tags]
        movie_years = [int(tag.text[1:5]) for tag in year_tags if self.__valid_year(tag.text)]
        movie_ratings = [float(tag["data-value"]) for tag in rating_tags]
        response.close()
        assert len(movie_titles) == len(movie_years) and len(movie_titles) == len(movie_ratings)
        # stores the top 250 rated movies

        for i in range(len(movie_titles)):
            tmp = [movie_titles[i], movie_years[i], movie_ratings[i]]
            self.movies.append(tmp)

    def __scrape_most_popular_movies(self):
        url = "https://www.imdb.com/chart/moviemeter?sort=ir,desc&mode=simple&page=1"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
 
        movie_tags = soup.select("td.titleColumn a")
        year_tags = soup.select("td.titleColumn span[class=secondaryInfo]")
        rating_tags = soup.select("td.posterColumn span[name=ir]")

        movie_titles = [tag.text.strip() for tag in movie_tags]
        movie_years = [int(tag.text[1:5]) for tag in year_tags if self.__valid_year(tag.text)]
        movie_ratings = [float(tag["data-value"]) for tag in rating_tags]
        response.close()
        assert len(movie_titles) >= 50 and len(movie_years) >= 50 and len(movie_ratings) >= 50
        # stores the top 50 most popular movies, then updates their
        # rating if they had already been scraped as the top rated movies

        for i in range(50):
            movie_found = False

            for movie in self.movies:
                if movie[0] == movie_titles[i]:
                    movie_found = True
                    movie[2] = (movie[2] + movie_ratings[i]) / 2 # updates rating
                    break

            if not movie_found: # not in the 'top rated movies' list
                tmp = [movie_titles[i], movie_years[i], movie_ratings[i]]
                self.movies.append(tmp)

    def __scrape_movies(self): # scraping from two sources
        self.__scrape_top_rated_movies()
        self.__scrape_most_popular_movies()

    def select_movies(self):
        self.__scrape_movies()
        self.movies.sort(key=self.__compare_movies, reverse=True) # sorts in descending order of rating

        try:
            file_name = "Top Movies.csv"
            headers = "Title,Year,Rating\n"
            f = open(file_name, 'w') # write movies in a .csv file
            f.write(headers)

            for movie in self.movies:
                if movie[2] == 10.0:
                    rating = "10.00"
                else:
                    rating = str(movie[2])
                    rating = rating[0:4]

                f.write(movie[0].replace(',', '.') + ',' + str(movie[1]) + ',' + rating + '\n')

            size = len(self.movies)
            print(size, "movies with the best ratings on IMDb are added in the Top Movies.csv file.")
            rnd = randint(0, size - 1)
            print("Recommended movie:", self.movies[rnd][0], '(' + str(self.movies[rnd][1]) + "), with rating", "%.2f." %self.movies[rnd][2])
        except:
            print("Error: couldn't create a file!")
        finally:
            print("\nPress Enter or X to close this window...")
            input()

        f.close()


ms = MovieSelector()
ms.select_movies()