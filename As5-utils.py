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
                }                act['role']  = actor.role
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
