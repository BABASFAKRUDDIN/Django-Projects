from .models import *
from datetime import datetime
from django.db.models import Q
import json

actors_list =[{ 'actor_id' : 'powerstar','name' : 'Pawan Kalyan'}, {'actor_id' : 'jrntr','name' : 'Jr.NTR'},{'actor_id' : 'rdj','name' : 'Robert Downey Jr'},{'actor_id' : 'rebelstar','name' : 'Prabas'},{'actor_id' : 'shruthi','name' : 'Shruthi Hassan'}]

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
        Actor.objects.create(actor_id = actor_data['actor_id'], name = actor_data['name'])
    
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

# task 1
def get_movies_by_given_movie_names(movie_names):
    return(
        get_movies_by_given_movie_ids(
            list(
                Movie.objects.filter(
                    name__in = movie_names
                ).values_list('movie_id',flat = True)
            )
        )
    )

def get_movies_by_given_movie_ids(movie_ids):
    movies_list = []
    
    for m_id in movie_ids:
        
        movie_filter = Movie.objects.filter(movie_id = m_id)
        for movie in movie_filter:
            movie_dict = dict()
            cast = Cast.objects.filter(movie = movie.movie_id)
            
            movie_dict['movie_id'] = movie.movie_id
            movie_dict['name'] = movie.name
            movie_dict['cast'] = []
            for actor in cast:
                act = dict()
                name = actor.actor.name
                actor_id = actor.actor_id
                act["actor"] = {
                    "name" : name,
                    "actor_id" : actor_id
                }
                act['role'] = actor.role
                act['is_debut_movie'] = actor.is_debut_movie
                movie_dict['cast'].append(act)
            
            movie_dict['box_office_collection_in_crores'] = movie.box_office_collection_in_crores
            movie_dict['release_date'] = str(movie.release_date)
            movie_dict['director_name'] = movie.director.name
            movie_dict['average_rating'] = movie.average_rating
            movie_dict['total_number_of_ratings'] = movie.total_number_of_ratings
            movies_list.append(movie_dict)
    return(movies_list)
    # print(json.dumps(movies_list,indent = 4))

# Task 2    
def get_movies_released_in_summer_in_given_years():
    movie_id = list(Movie.objects.filter(
                Q(release_date__year__range=[2006,2009]) &
                Q(release_date__month__gte = 5) & Q(release_date__month__lte = 7)
            ).values_list('movie_id',flat = True).distinct())
    return(get_movies_by_given_movie_names(movie_id))

# Task 3
def get_movie_names_with_actor_name_ending_with_smith():
    return(
        list(
            Movie.objects.filter(
                movie_id__in = Cast.objects.filter(
                    actor__name__endswith = 'smith'
                ).values_list('movie',flat = True)
            ).values_list('name',flat = True).distinct()
        )
    )

# Task 4
def get_movie_names_with_ratings_in_given_range():
    return(
        list(
            Movie.objects.filter(
                movie_id__in = Rating.objects.filter(
                    rating_five_count__range = [1000,3000]
                ).values('movie')
            ).values_list('name',flat = True).distinct()
        )
    )

# Task 5
def get_movie_names_with_ratings_above_given_minimum():
    """
        list(Rating.objects.filter(Q(rating_five_count__gte = 500) | Q(rating_four_count__gte = 1000) | Q(rating_three_count__gte = 2000) | Q(rating_two_count__gte = 4000) | Q(rating_one_count__gte = 8000)).values_list('movie',flat = True))
    """
    return(
        list(
            Movie.objects.filter(
                movie_id__in = list(
                    Rating.objects.filter(
                        Q(rating_five_count__gte = 500) |
                        Q(rating_four_count__gte = 1000) | 
                        Q(rating_three_count__gte = 2000) | 
                        Q(rating_two_count__gte = 4000) | 
                        Q(rating_one_count__gte = 8000)
                    ).values_list('movie',flat = True)
                ),release_date__year__gt = 2000
            ).distinct()
        )
    )

# Task 6
def get_movie_directors_in_given_year():
    return(
        list(
            Movie.objects.filter(
                release_date__year = 2000
            ).values_list('director',flat = True).distinct()
        )
    )

# Task 7
def get_actor_names_debuted_in_21st_century():
    return(
        list(
            Cast.objects.filter(
                movie__release_date__year__gt = 2000, movie__release_date__year__lte = 2100, is_debut_movie = True
            ).values_list('actor__name',flat=True)
        )
    )

# Task 8
def get_director_names_containing_big_as_well_as_movie_in_may():
    return(
        list(
            Movie.objects.filter(
                name__contains = 'big'
            ).filter(
                release_date__month = 5
            ).values_list('director',flat = True).distinct()
        )
    )

# Task 9
def get_director_names_containing_big_and_movie_in_may():
    return(
        list(
            Movie.objects.filter(
                name__contains = 'big',release_date__month = 5
            ).values_list('director',flat = True).distinct()
        )
    )

# Task 10
def reset_ratings_for_movies_in_this_year():
    Rating.objects.filter(
        movie__release_date__year = 2000
    ).update(
        rating_five_count = 0, 
        rating_four_count = 0, 
        rating_three_count = 0, 
        rating_two_count = 0, 
        rating_one_count = 0
    )