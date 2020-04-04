from .models import *
from datetime import datetime
from django.db.models import Q
import json
from django.db.models import Count,Avg,Max,Min

def profile():
    def decorator(func):
        def handler(*args, **kwargs):
            import line_profiler
            profiler = line_profiler.LineProfiler()
            profiler.enable_by_count()
            profiler.add_function(func)
            result = func(*args, **kwargs)
            profiler.print_stats()
            return result

        handler.__doc__ = func.__doc__
        return handler

    return decorator
    
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

directors_list = ['Venky Atluri', 'Puri Jagannath', 'Raja Mouli', 'Cristopher Nolan', 'Markk Webb','Harish Shankar', 'SJ Surya']

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


# TASK 1
# @profile()
def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    Actor.objects.bulk_create([
        Actor(
            actor_id = actor_data['actor_id'],
            name = actor_data['name'],
            gender = actor_data['gender']
        )for actor_data in actors_list
    ])
    
    Director.objects.bulk_create([
        Director(
            name = director_data
        )for director_data in directors_list
    ])
    
    directors = list(Director.objects.all())
    
    Movie.objects.bulk_create([
        Movie(
            movie_id = movie_data['movie_id'],
            name = movie_data['name'],
            release_date = movie_data['release_date'],
            box_office_collection_in_crores = movie_data['box_office_collection_in_crores'],
            director = [d for d in directors if d.name == movie_data['director_name']][0]
            # director = Director.objects.get(name = movie_data['director_name'])
        ) for movie_data in movies_list
    ])
    
    
    for movie in movies_list:
        Cast.objects.bulk_create([
            Cast(
                movie_id = movie['movie_id'],
                actor_id = cast['actor_id'],
                role = cast['role'],
                is_debut_movie = cast['is_debut_movie']
            )for cast in movie['actors']
        ])
    
    Rating.objects.bulk_create([
        Rating(
            movie_id = rating['movie_id'],
            rating_one_count = rating['rating_one_count'],
            rating_two_count = rating['rating_two_count'],
            rating_three_count = rating['rating_three_count'],
            rating_four_count = rating['rating_four_count'],
            rating_five_count = rating['rating_five_count']
        )for rating in movie_rating_list
    ])


# TASK 2
# @profile()
def remove_all_actors_from_given_movie(movie_object):
    # actors_to_remove = list(Actor.objects.filter(movie = movie_object))
    # movie_object.actors.remove(*actors_to_remove)
    movie_object.actors.clear()

# TASK 3
def get_all_rating_objects_for_given_movies(movie_objs):
    return(
        list(
            Rating.objects.filter(movie__in = movie_objs)
        )
    )

# TASK 4
# NOT COMPLETED...
def get_movies_by_given_movie_names(movie_names):
    
    movies_list = []
    if len(movie_names) == 0:
        movie_filter=[]
        
    elif isinstance(movie_names[0],Movie):
        from django.db.models import prefetch_related_objects
        movie_filter = movie_names
        prefetch_related_objects(movie_filter)
        flag = 1
    else:
        flag = 0
        movie_filter = Movie.objects.select_related().filter(name__in = movie_names)
    for movie in movie_filter:
            movie_dict = dict()
            # cast = Cast.objects.filter(movie = movie.movie_id)
            if flag == 1:
                cast = movie.cast_set.filter(actor__gender = 'FEMALE')
            else:
                cast = movie.cast_set.all()
            
            movie_dict['movie_id'] = movie.movie_id
            movie_dict['name'] = movie.name
            movie_dict['cast'] = []
            for actor in cast:
                act = dict()
                act["actor"] = {
                    "name" : actor.actor.name,
                    "actor_id" : actor.actor.actor_id
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
    return movies_list

# TASK 5
def get_all_actor_objects_acted_in_given_movies(movie_objs):
    return(
        list(
            Actor.objects.filter(movie__in = movie_objs).distinct()
        )
    )

# TASK 6
def get_female_cast_details_from_movies_having_more_than_five_female_cast():
    from django.db.models import Count,Q
    return(
        get_movies_by_given_movie_names(
            list(
                Movie.objects.annotate( 
                    female_count = Count( 
                        'actors', distinct = True, filter = Q(actors__gender = 'FEMALE') 
                    ) 
                ).filter(female_count__gte = 6)
            )
        )
    )

# TASK 7
def get_actor_movies_released_in_year_greater_than_or_equal_to_2000():
    pass
    # Movie.objects.values('actors').prefetch('cast_set')
    
# TASK 8
def reset_ratings_for_movies_in_given_year(year):
    
    Rating.objects.filter(
        movie__release_date__year = year
    ).update(
        rating_one_count = 0,
        rating_two_count = 0,
        rating_three_count = 0,
        rating_four_count = 0,
        rating_five_count = 0
    )

# ADDITIONAL TASKS

# TASK 9
def get_movies_released_in_summer_in_given_years():
    movie_id = list(Movie.objects.filter(
                Q(release_date__year__range=[2006,2009]) &
                Q(release_date__month__gte = 5) & Q(release_date__month__lte = 7)
            ).values_list('movie_id',flat = True).distinct())
    return(get_movies_by_given_movie_names(movie_id))

# TASK 10
#@query_debugger
def get_movies_by_given_movie_names(movie_names,gender=''):
    list_of_movies=[]
    if(len(movie_names)==0):
        movie_list=[]
    elif(isinstance(movie_names[0],Movie)):
        from django.db.models import prefetch_related_objects
        movie_list=movie_names
        prefetch_related_objects(movie_list,'cast_set')
    else:
        movie_list=list(Movie.objects.prefetch_related('cast_set').select_related('rating','director').filter(name__in=movie_names))
    for m in movie_list:
        
            try:
                one,two,three,four,five=m.rating.rating_one_count,m.rating.rating_two_count,m.rating.rating_three_count,m.rating.rating_four_count,m.rating.rating_five_count
                s=one+two+three+four+five
                t=one*1+two*2+three*3+four*4+five*5
                rating_list=[t/s,s]
                print(rating_list)
            except:
                rating_list=[0,0]
    
            cast_list=[]
            if(gender==''):
                c=m.cast_set.all()
            else:
                c=m.cast_set.filter(actor__gender='FEMALE')
            for actor in c:
                act=dict()
                name=actor.actor.name
                actor_id = actor.actor_id
                act['actor']  ={
                    'name' : name,
                    'actor_id' : actor_id
                }
                act['role']  = actor.role
                act['is_debut_movie']  = actor.is_debut_movie
                cast_list.append(act)
            temp={}
            temp['movie_id']=m.movie_id
            temp['name']=m.name
            temp['cast']=cast_list
            temp['box_office_collection_in_crores']=m.box_office_collection_in_crores
            temp['release_date']=str(m.release_date)
            temp['director_name']=m.director.name
            temp['average_rating']=rating_list[0]
            temp['total_number_of_ratings']=rating_list[1]
            list_of_movies.append(temp)
    
    return list_of_movies




