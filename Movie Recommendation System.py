# FILL IN ALL THE FUNCTIONS IN THIS TEMPLATE
# MAKE SURE YOU TEST YOUR FUNCTIONS WITH MULTIPLE TEST CASES
# ASIDE FROM THE SAMPLE FILES PROVIDED TO YOU, TEST ON YOUR OWN FILES

# WHEN DONE, SUBMIT THIS FILE TO CANVAS

from collections import defaultdict
from collections import Counter


# YOU MAY NOT CODE ANY OTHER IMPORTS

# ------ TASK 1: READING DATA  --------

# 1.1
def read_ratings_data(f):
    movie_ratings_dict = {}
    for line in open(f):
        movie, rating, _ = line.strip().rsplit("|")
        movie_ratings_dict.setdefault(movie.strip(), []).append(float(rating))
    return movie_ratings_dict


# 1.2
def read_movie_genre(f):
    movie_genre_dict = {}
    for line in open(f):
        genre, _, movie = line.strip().rsplit("|")
        movie_genre_dict[movie.strip()] = genre.strip()
    return movie_genre_dict


# ------ TASK 2: PROCESSING DATA --------

# 2.1
def create_genre_dict(d):
    genre_dict = {}
    for movie, genre in d.items():
        if genre in genre_dict:
            genre_dict[genre].append(movie)
        else:
            genre_dict[genre] = [movie]
    return genre_dict


# 2.2
def calculate_average_rating(d):
    average_ratings = {}
    for movie, ratings in d.items():
        average_rating = round(sum(ratings) / len(ratings), 1)
        average_ratings[movie] = average_rating
    return average_ratings


# ------ TASK 3: RECOMMENDATION --------

# 3.1
def get_popular_movies(d, n=10):
    sorted_movies = sorted(d.items(), key=lambda x: x[1], reverse=True)
    top_n_movies = sorted_movies[:n]
    return dict(sorted_movies)

    # parameter d: dictionary that maps movie to average rating
    # parameter n: integer (for top n), default value 10
    # return: dictionary that maps movie to average rating,
    # in ranked order from highest to lowest average rating
    # WRITE YOUR CODE BELOW


# 3.2
def filter_movies(d, thres_rating=3):
    filtered_movies = {movie: rating for movie, rating in d.items() if rating >= thres_rating}
    return filtered_movies
    # parameter d: dictionary that maps movie to average rating
    # parameter thres_rating: threshold rating, default value 3
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW


# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    if genre not in genre_to_movies:
        return {}
    movies_in_genre = {movie: rating for movie, rating in movie_to_average_rating.items() if
                       movie in genre_to_movies[genre]}

    sorted_movies = sorted(movies_in_genre.items(), key=lambda x: x[1], reverse=True)

    top_n_movies = sorted_movies[:n]

    return dict(top_n_movies)


# parameter genre: genre name (e.g. "Comedy")
# parameter genre_to_movies: dictionary that maps genre to movies
# parameter movie_to_average_rating: dictionary  that maps movie to average rating
# parameter n: integer (for top n), default value 5
# return: dictionary that maps movie to average rating
# WRITE YOUR CODE BELOW


# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    if genre not in genre_to_movies:
        return None

    # Filter movies in the specified genre
    movies_in_genre = {movie: rating for movie, rating in movie_to_average_rating.items() if
                       movie in genre_to_movies[genre]}


    if movies_in_genre:
        average_rating = round(sum(movies_in_genre.values()) / len(movies_in_genre), 1)
        return average_rating
    else:
        return None


# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    genre_ratings = {}

    for genre in genre_to_movies:
        rating = get_genre_rating(genre, genre_to_movies, movie_to_average_rating)
        if rating is not None:
            genre_ratings[genre] = rating

    sorted_genres = sorted(genre_ratings.items(), key=lambda x: x[1], reverse=True)

    if len(sorted_genres) <= n:
        return dict(sorted_genres)
    else:
        return dict(sorted_genres[:n])

    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps genre to average rating
    # WRITE YOUR CODE BELOW
    pass


# ------ TASK 4: USER FOCUSED  --------

# 4.1
def read_user_ratings(f):
    user_ratings = {}
    for line in open(f):
        movie, rating, user_id = line.strip().split('|')
        rating = float(rating)
        user_id = user_id.strip()

        if user_id not in user_ratings:
            user_ratings[user_id] = []

        user_ratings[user_id].append((movie, rating))

    return user_ratings


# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    genre_ratings = {}
    genre_counts = {}

    if user_id in user_to_movies:

        for movie, rating in user_to_movies[user_id]:

            genre = movie_to_genre.get(movie)
            if genre:

                genre_ratings[genre] = genre_ratings.get(genre, 0) + rating
                genre_counts[genre] = genre_counts.get(genre, 0) + 1


        genre_averages = {genre: genre_ratings[genre] / genre_counts[genre] for genre in genre_ratings if genre_counts[genre] > 0}

        if not genre_averages:
            print(f"No ratings found for user {user_id}.")
            return None

        max_average_rating = max(genre_averages.values())
        top_genres = [genre for genre, average_rating in genre_averages.items() if average_rating == max_average_rating]

        return top_genres[0]

    else:
        print(f"No ratings found for user {user_id}.")
        return None
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
    # WRITE YOUR CODE BELOW

# 4.3
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    top_genre = get_user_genre(user_id, user_to_movies, movie_to_genre)

    if top_genre is None:
        print(f"No top genre found for user {user_id}.")
        return {}

    unrated_movies = [(movie, movie_to_average_rating[movie]) for movie, genre in movie_to_genre.items() if
                      genre == top_genre and movie not in [rated_movie for rated_movie, _ in
                                                           user_to_movies.get(user_id, [])]]

    sorted_unrated_movies = sorted(unrated_movies, key=lambda x: x[1], reverse=True)

    return dict(sorted_unrated_movies[:3])

    # Example usage:
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # parameter movie_to_average_rating: dictionary that maps movie to average rating
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW


# -------- main function for your testing -----
def main():
    d1 = read_ratings_data("rating.txt")
    print(d1)
    d2 = read_movie_genre("Genre.txt")
    print(d2)
    d3 = create_genre_dict(d2)
    print(d3)
    d4 = calculate_average_rating(d1)
    print(d4)
    d5 = get_popular_movies(d4, n=10)
    print(d5)
    d6 = filter_movies(d5)
    print(d6)
    d7 = get_popular_in_genre("Comedy", d3, d4, n=5)
    print(d7)
    d8 = get_genre_rating("Comedy", d3, d4)  # Returns int
    print(d8)
    d9 = genre_popularity(d3, d4, n=5)
    print(d9)
    d10 = read_user_ratings("rating.txt")
    print(d10)
    d11 = get_user_genre("11", d10, d2)
    print(d11)
    d12 = recommend_movies("11", d10, d2, d4)
    print(d12)
    # write all your test code here
    # this function will be ignored by us when grading


# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions

# program will start at the following main() function call
# when you execute hw1.py
main()