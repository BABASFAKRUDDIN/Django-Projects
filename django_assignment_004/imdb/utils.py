from .models import *
from datetime import datetime
from django.db.models import Q
import json
from django.db.models import Count,Avg,Max,Min

actors_list =[{ 'actor_id' : 'powerstar','name' : 'Pawan Kalyan','gender':'MALE'}, {'actor_id' : 'jrntr','name' : 'Jr.NTR','gender':'MALE'},{'actor_id' : 'rdj','name' : 'Robert Downey Jr','gender':'MALE'},{'actor_id' : 'rebelstar','name' : 'Prabas','gender':'MALE'},{'actor_id' : 'shruthi','name' : 'Shruthi Hassan','gender':'FEMALE'}]

movies_list = [
    {
        'movie_id' : 'Tholi','name' : 'Tholiprema','actors' : [{'actor_id' : 'powerstar','role' : 'hero','is_debut_movie' : False}],'box_office_collection_in_crores' : 20.3,'release_date' : '2000-3-3','director_name' :'Venky Atluri'
    },
    {
        'movie_id' : 'Gabber','name' : 'Gabber Sing','actors' : [{'actor_id' : 'powerstar','role' : 'hero','is_debut_movie' : False},{'actor_id' : 'shruthi','role' : 'heroine','is_debut_movie' : False}],'box_office_collection_in_crores' : 40.3,'release_date' : '2005-3-3','director_name' :'Harish Shankar'
    },
    {
        'movie_id' : 'Khushi','name' : 'Khushi','actors' : [{'actor_id' : 'powerstar','role' : 'hero','is_debut_movie' : False}],'box_office_collection_in_crores' : 40.3,'release_date' : '2003-3-3','director_name' :'SJ Surya'
    },
    {
        'movie_id' : 'Baahubali','name' : 'Baahubali','actors' : [{'actor_id' : 'rebelstar','role' : 'hero','is_debut_movie' : False}],'box_office_collection_in_crores' : 50.3,'release_date' : '2013-3-3','director_name' :'Raja Mouli'
    },
    {
        'movie_id' : 'Baahubali2','name' : 'Baahubali2','actors' : [{'actor_id' : 'rebelstar','role' : 'hero','is_debut_movie' : False}],'box_office_collection_in_crores' : 60.3,'release_date' : '2016-3-3','director_name' :'Raja Mouli'
    },
    {
        'movie_id' : 'BB2','name' : 'Baahubali2','actors' : [{'actor_id' : 'rebelstar','role' : 'hero','is_debut_movie' : False}],'box_office_collection_in_crores' : 60.3,'release_date' : '2016-3-3','director_name' :'Raja Mouli'
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

def populate_actors(actors_list = []):
    for actor_data in actors_list:
        Actor.objects.create(actor_id = actor_data['actor_id'], name = actor_data['name'],gender = actor_data['gender'])

def populate_directors(director_list = []):
    for director_data in director_list:
        Director.objects.create(name = director_data)

def populate_movies(movies_list = []):
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

def populate_movie_rating(movie_rating_list = []):
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

def populate():
    print("Populating Actors...")
    populate_actors(actors_list)
    print("Populating Directors...")
    populate_directors(director_list)
    print("Populating Movies...")
    populate_movies(movies_list)
    print("Populating Ratings...")
    populate_movie_rating(movie_rating_list)


# TASK 1
def get_average_box_office_collections():
    val = Movie.objects.aggregate(
            avg_coll = Avg('box_office_collection_in_crores')
        )
    try:
        round_val = round(val['avg_coll'],3)
    except:
        return 0
    return(round_val)

# TASK 2
def get_movies_with_distinct_actors_count():
    return(
        list(
            Movie.objects.annotate(
                actors_count = Count('actors',distinct = True)
            )
        )
    )

# TASK 3
def get_male_and_female_actors_count_for_each_movie():
    return(list(
        Movie.objects.annotate(
            male_actors_count = Count(
                'actors', distinct = True, filter = Q(actors__gender = 'MALE')
            )
        ).annotate(
            female_actors_count = Count(
                'actors', distinct = True, filter = Q(actors__gender = 'FEMALE')
            )
        )
    ))

# TASK 4
def get_roles_count_for_each_movie():
    return(
        list(
            Movie.objects.annotate(
                roles_count = Count('cast__role',distinct = True)
            )
        )
    )

# TASK 5
def get_role_frequency():
    cast= Cast.objects.values('role').annotate(actor = Count('actor',distinct = True))
    cast_dict = {}
    for item in cast:
        cast_dict[item['role']] = item['actor']
    return(cast_dict)

# TASK 6
def get_role_frequency_in_order():
    return(
        list(
            Cast.objects.values_list('role').annotate(
                actor = Count('actor',distinct = True)
            ).order_by('-movie__release_date')
        )
    )

# TASK 7
def get_no_of_movies_and_distinct_roles_for_each_actor():
    return(
        list(
            Actor.objects.annotate(
                movies_count = Count('cast__movie', distinct = True)
            ).annotate(roles_count = Count('cast__role', distinct = True))
        )
    )

# TASK 8
def get_movies_with_atleast_forty_actors():
    return(
        list(
            Movie.objects.annotate(
                actors_count = Count('actors')
            ).filter(actors_count__gte = 40)
        )
    )

# TASK 9
def get_average_no_of_actors_for_all_movies():
    val = Movie.objects.annotate(
            num_of_actors = Count('actors')
        ).aggregate(avg = Avg('num_of_actors'))
    try:
        round_val = round(val['avg'],3)
    except:
        return 0
    return round_val
