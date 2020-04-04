from imdb.models import *
from django.db import connection, reset_queries
import time
import functools


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


def query_debugger(func):

    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        end_queries = len(connection.queries)
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start)}s")
        return result

    return inner_func

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

#Task-1
#@profile()
def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    Actor.objects.bulk_create([ Actor(actor_id=actor['actor_id'],
        name=actor['name'],gender=actor['gender']
    ) for actor in actors_list ])
    
    Director.objects.bulk_create([ Director(name=director
    ) for director in directors_list ])
    
    director_list=Director.objects.all().values_list()
    
    movie_list=[]
    cast_list=[]
    for movie in movies_list:
        for id,name in director_list:
            if(name==movie['director_name']):
                director_obj=id
                break
        movie_list.append (Movie(movie_id=movie['movie_id'],
        name=movie['name'],
        box_office_collection_in_crores=movie['box_office_collection_in_crores'],
        release_date=movie['release_date'],
        director_id=director_obj))
        for cast in movie['actors']:
            cast_list.append(Cast(actor_id=cast['actor_id'],
            movie_id=movie['movie_id'],
            role=cast['role'],is_debut_movie=cast['is_debut_movie']))
    Movie.objects.bulk_create(movie_list)
    Cast.objects.bulk_create(cast_list)
        
    Rating.objects.bulk_create([ 
        Rating(movie_id=mr['movie_id'],
        rating_one_count=mr["rating_one_count"]
        ,rating_two_count=mr["rating_two_count"],
        rating_three_count=mr["rating_three_count"]
        ,rating_four_count=mr["rating_four_count"],
        rating_five_count=mr["rating_five_count"] ) 
        for mr in  movie_rating_list
        ])
        
#Task-2
def remove_all_actors_from_given_movie(movie_object):
    movie_object=movie_object.actors.clear()
    
#Task-3
def get_all_rating_objects_for_given_movies(movie_objs):
    return list(Rating.objects.filter(movie__in=movie_objs))
#Task-4
'''@query_debugger
def get_movies_by_given_movie_names(movie_names,gender=''):
    list_of_movies=[]
    if(len(movie_names)==0):
        movie_list=[]
    elif(isinstance(movie_names[0],Movie)):
        from django.db.models import prefetch_related_objects
        movie_list=movie_names
        prefetch_related_objects(movie_list,'cast_set')
    else:
        movie_list=Movie.objects.prefetch_related('cast_set').filter(name__in=movie_names)
    for m in movie_list:    
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
            temp['average_rating']=get_average_rating_of_movie(m)
            temp['total_number_of_ratings']=sum_of_rating(m)
            list_of_movies.append(temp)
    
    return list_of_movies'''

#Task-5
def get_all_actor_objects_acted_in_given_movies(movie_objs):
    return Actor.objects.filter(movie__in=movie_objs).distinct()

#Task-6
def get_female_cast_details_from_movies_having_more_than_five_female_cast():
    from django.db.models import Count,Q
    female_count=Count('actors',distinct=True,filter=Q(actors__gender='FEMALE'))
    cast_list1=Cast.objects.select_related('movie__rating','movie__director','actor').filter(
        movie__in=Movie.objects.annotate(female_actors_count=female_count).filter(female_actors_count__gt=5),actor__gender='FEMALE')
    list_of_movies=[]
    
    for cast in cast_list1:
            m=cast.movie   
            try:
                one,two,three,four,five=m.rating.rating_one_count,m.rating.rating_two_count,m.rating.rating_three_count,m.rating.rating_four_count,m.rating.rating_five_count
                s=one+two+three+four+five
                t=one*1+two*2+three*3+four*4+five*5
                rating_list=[t/s,s]
            except:
                rating_list=[0,0]
            
            
            cast_list=[]
    
            actor_dict={}
            actor_dict['name']=cast.actor.name
            actor_dict['actor_id']=cast.actor_id
            
            cast_dict={}
            cast_dict['actor']=actor_dict
            cast_dict['role']= cast.role
            cast_dict['is_debut_movie']=cast.is_debut_movie
            cast_list.append(cast_dict)
            
            #print(list_of_movies[-1]['movie_id'],m.movie_id)  
            #print(len(list_of_movies))
            temp={}
            temp['movie_id']=m.movie_id
            temp['name']=m.name
            temp['cast']=cast_list
            temp['box_office_collection_in_crores']=m.box_office_collection_in_crores
            temp['release_date']=str(m.release_date)
            temp['director_name']=m.director.name
            temp['average_rating']=rating_list[0]
            temp['total_number_of_ratings']=rating_list[1]
            flag=0
            for d in list_of_movies:
                #print(m.movie_id,d['movie_id'])
                if(d['movie_id'] == m.movie_id):
                    d['cast'].append(cast_dict)
                    flag=1
                    break
            if(flag==0):
                list_of_movies.append(temp)
    
    return list_of_movies

    
    
    


#Task-8
def reset_ratings_for_movies_in_given_year(year):
    return Rating.objects.filter(movie__release_date__year=year).update(rating_five_count=0,
        rating_four_count=0,
        rating_three_count=0,
        rating_two_count=0,
        rating_one_count=0,
    )
#Task-7    
def get_actor_movies_released_in_year_greater_than_or_equal_to_2000():
    from django.db.models import Prefetch
    actors_list= Actor.objects.prefetch_related(
        Prefetch('movie_set',queryset=Movie.objects.filter(
            release_date__year__gte=2000).select_related(
                'rating','director').prefetch_related(
                    Prefetch('cast_set',to_attr='cast_attr')),
                    to_attr='movie_attr')
                    ).filter(movie__release_date__year__gte=2000).distinct()
    l=[]
    for actors in actors_list:
        a={}
        
        a['name']=actors.name
        a['actor_id']=actors.actor_id
        movie_list=[]
        for movie in actors.movie_attr:
            try:
                one,two,three,four,five=movie.rating.rating_one_count,movie.rating.rating_two_count,movie.rating.rating_three_count,movie.rating.rating_four_count,movie.rating.rating_five_count
                s=one+two+three+four+five
                t=one*1+two*2+three*3+four*4+five*5
                rating_list=[t/s,s]
            except:
                rating_list=[0,0]
            
            
            cast_list=[]
            for cast in movie.cast_attr:
                act=dict()
                if(cast.actor_id == actors.actor_id):
                    act['role']  = cast.role
                    act['is_debut_movie']  = cast.is_debut_movie
                    cast_list.append(act)
            temp={}
            temp['movie_id']=movie.movie_id
            temp['name']=movie.name
            temp['cast']=cast_list
            temp['box_office_collection_in_crores']=movie.box_office_collection_in_crores
            temp['release_date']=str(movie.release_date)
            temp['director_name']=movie.director.name
            temp['average_rating']=rating_list[0]
            temp['total_number_of_ratings']=rating_list[1]
            movie_list.append(temp)
        
        a['movies']=movie_list
        l.append(a)
    return l
#Task-4
def get_movies_by_given_movie_names(movie_names):
    list_of_movies=[]
    #print('yes')
    #from django.db.models import Prefetch
    cast_list1=Cast.objects.select_related('movie__rating','movie__director','actor').filter(movie__name__in=movie_names)
    for cast in cast_list1:
            m=cast.movie   
            try:
                one,two,three,four,five=m.rating.rating_one_count,m.rating.rating_two_count,m.rating.rating_three_count,m.rating.rating_four_count,m.rating.rating_five_count
                s=one+two+three+four+five
                t=one*1+two*2+three*3+four*4+five*5
                rating_list=[t/s,s]
            except:
                rating_list=[0,0]
            
            
            cast_list=[]
    
            actor_dict={}
            actor_dict['name']=cast.actor.name
            actor_dict['actor_id']=cast.actor_id
            
            cast_dict={}
            cast_dict['actor']=actor_dict
            cast_dict['role']= cast.role
            cast_dict['is_debut_movie']=cast.is_debut_movie
            cast_list.append(cast_dict)
            
            #print(list_of_movies[-1]['movie_id'],m.movie_id)  
            #print(len(list_of_movies))
            temp={}
            temp['movie_id']=m.movie_id
            temp['name']=m.name
            temp['cast']=cast_list
            temp['box_office_collection_in_crores']=m.box_office_collection_in_crores
            temp['release_date']=str(m.release_date)
            temp['director_name']=m.director.name
            temp['average_rating']=rating_list[0]
            temp['total_number_of_ratings']=rating_list[1]
            flag=0
            for d in list_of_movies:
                #print(m.movie_id,d['movie_id'])
                if(d['movie_id'] == m.movie_id):
                    d['cast'].append(cast_dict)
                    flag=1
                    break
            if(flag==0):
                list_of_movies.append(temp)
    
    return list_of_movies
    
'''
cast_list=Cast.objects.prefetch_related(Prefetch('movie',to_attr='movie_list'),Prefetch('movie__director',to_attr='director_attr'),Prefetch('actor',to_attr='actor_attr'),Prefetch(movie__rating,to_attr=mr_attr)).filter(movie__in=['Movie 1'])
cast_list=Cast.objects.select_related('movie__rating','movie__director','movie__rating').filter(movie__name__in=['Movie 1'])
