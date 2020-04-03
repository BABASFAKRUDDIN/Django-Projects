from .models import *
from datetime import datetime
import statistics


actors_list =[{ 'actor_id' : 'powerstar','name' : 'Pawan Kalyan'}, {'actor_id' : 'jrntr','name' : 'Jr.NTR'},{'actor_id' : 'rdj','name' : 'Robert Downey Jr'},{'actor_id' : 'rebelstar','name' : 'Prabas'}]
  

movies_list = [
{
'movie_id' : 'Tholi','name' : 'Tholiprema','actors' : [{'actor_id' : 'powerstar','role' : 'hero','is_debut_movie' : False}],'box_office_collection_in_crores' : 20.3,'release_date' : '2000-3-3','director_name' :'Venky Atluri'
},
{
'movie_id' : 'Gabber','name' : 'Gabber Sing','actors' : [{'actor_id' : 'powerstar','role' : 'hero','is_debut_movie' : False}],'box_office_collection_in_crores' : 40.3,'release_date' : '2005-3-3','director_name' :'Harish Shankar'
},
{
'movie_id' : 'Khushi','name' : 'Khushi','actors' : [{'actor_id' : 'powerstar','role' : 'hero','is_debut_movie' : False}],'box_office_collection_in_crores' : 40.3,'release_date' : '2003-3-3','director_name' :'SJ Surya'
},
{
'movie_id' : 'Baahubali','name' : 'Baahubali','actors' : [{'actor_id' : 'rebelstar','role' : 'hero','is_debut_movie' : False}],'box_office_collection_in_crores' : 50.3,'release_date' : '2013-3-3','director_name' :'Raja Mouli'
},
{
'movie_id' : 'Baahubali2','name' : 'Baahubali2','actors' : [{'actor_id' : 'rebelstar','role' : 'hero','is_debut_movie' : False}],'box_office_collection_in_crores' : 60.3,'release_date' : '2016-3-3','director_name' :'Raja Mouli'
}

]

    
director_list = ['Venky Atluri', 'Puri Jagannath', 'Raja Mouli', 'Cristopher Nolan', 'Markk Webb','Harish Shankar', 'SJ Surya']

    
movie_rating_list = [
    {
        'movie_id' : 'Tholi',
        "rating_one_count": 4,
        "rating_two_count": 5,
        "rating_three_count": 3,
        "rating_four_count": 5,
        "rating_five_count": 4
    },
    {
        'movie_id' : 'Gabber',
        "rating_one_count": 4,
        "rating_two_count": 5,
        "rating_three_count": 3,
        "rating_four_count": 5,
        "rating_five_count": 4
    },
    {
        'movie_id' : 'Baahubali2',
        "rating_one_count": 4,
        "rating_two_count": 5,
        "rating_three_count": 3,
        "rating_four_count": 5,
        "rating_five_count": 4
    }
]


# task_2
# Populate DB
def populate_database(actors_list = [], movies_list = [], directors_list = [], movie_rating_list = []):
    #actor
    for actor_data in actors_list:
        Actor.objects.create(actor_id = actor_data['actor_id'], name = actor_data['name'])
    
    #direcor
    for director_data in directors_list:
        Director.objects.create(name = director_data)
    
    #movie
    for movie_data in movies_list:
        m = Movie.objects.create(
            movie_id = movie_data['movie_id'],
            name = movie_data['name'],
            release_date = movie_data['release_date'],
            box_office_collection_in_crores = movie_data['box_office_collection_in_crores'],
            director = Director.objects.get(name = movie_data['director_name'])
        )
        for actor in movie_data['actors']:
            Cast.objects.create(actor = Actor.objects.get(actor_id = actor['actor_id']),
                movie = m,
                role = actor['role'],
                is_debut_movie = actor['is_debut_movie']
            )
    
    #rating
    for rating in movie_rating_list:
        m = Movie.objects.get(movie_id = rating['movie_id'])
        Rating.objects.create(
            movie = m,
            rating_one_count = rating['rating_one_count'],
            rating_two_count = rating['rating_two_count'],
            rating_three_count = rating['rating_three_count'],
            rating_four_count = rating['rating_four_count'],
            rating_five_count = rating['rating_five_count']
        )


#task 3

def get_no_of_distinct_movies_actor_acted(actor_id):
    """
    return(Cast.objects.filter(
        actor = Actor.objects.get(
            actor_id = actor_id
        )
    ).distinct().count())
    """
    return(Movie.objects.filter(
        actors__actor_id = actor_id
    ).distinct().count())
#task 4

def get_movies_directed_by_director(director_obj):
    return(list(
        Movie.objects.filter(
        director = director_obj
    )))

#task 5

def get_average_rating_of_movie(movie_obj):
    try:
        r = Rating.objects.get(movie = movie_obj)
    except:
        return(0)
    r_count_list = [r.rating_one_count, r.rating_two_count*2, r.rating_three_count*3, r.rating_four_count*4, r.rating_five_count*5]
    r_list = [r.rating_one_count, r.rating_two_count, r.rating_three_count, r.rating_four_count, r.rating_five_count]
    if all(val == 0 for val in r_list):
        return(0)
    return(sum(r_count_list)/sum(r_list))

#task 6

def delete_movie_rating(movie_obj):
    rating_movie = Rating.objects.get(movie_id = movie_obj.movie_id)
    rating_movie.delete()

#task 7
def get_all_actor_objects_acted_in_given_movies(movie_objs):
    return (list(
        Actor.objects.filter(
            movie__in = movie_objs
        ).distinct()
    ))

#task 8

def update_director_for_given_movie(movie_obj, director_obj):
    movie_obj.director = director_obj
    movie_obj.save()

#task 9

def get_distinct_movies_acted_by_actor_whose_name_contains_john():
    return(list(
            Movie.objects.filter(
                actors__name__contains = 'john'
            ).distinct()
        )
    )

#task 10

def remove_all_actors_from_given_movie(movie_obj):
    movie_obj.actors.clear()
    
#task 11

def get_all_rating_objects_for_given_movies(movie_objs):
    return(list(
        Rating.objects.filter(
            movie__in = movie_objs
        )
    ))
    