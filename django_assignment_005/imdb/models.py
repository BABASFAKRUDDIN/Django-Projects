from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length = 100,primary_key = True)
    
    def __str__(self):
        return f'{self.name}'

class Actor(models.Model):
    actor_id = models.CharField(max_length = 100, primary_key = True)
    name = models.CharField(max_length = 100)
    gender = models.CharField(max_length = 10,
        choices = (
            ('MALE','MALE'),
            ('FEMALE','FEMALE')
        )
    )
    def __str__(self):
        return f'{self.actor_id} {self.name}'

    # @property
    # def name(self):
    #     return f'{self.name}'
        
class Movie(models.Model):
    movie_id = models.CharField(max_length = 100,primary_key = True)
    name = models.CharField(max_length = 100)
    release_date = models.DateField()
    box_office_collection_in_crores = models.FloatField()
    director = models.ForeignKey(
        Director,
        on_delete = models.CASCADE
    )
    actors = models.ManyToManyField(Actor, through = 'Cast')
    
    def __str__(self):
        return f'{self.movie_id} {self.name} {self.release_date} {self.box_office_collection_in_crores} {self.director}'
        
    @property
    def average_rating(self):
        try:
            r = Rating.objects.get(movie = self)
        except:
            return(0)
        r_count_list = [r.rating_one_count, 
                        r.rating_two_count*2, 
                        r.rating_three_count*3, 
                        r.rating_four_count*4, 
                        r.rating_five_count*5]
        r_list = [r.rating_one_count, 
                  r.rating_two_count, 
                  r.rating_three_count, 
                  r.rating_four_count, 
                  r.rating_five_count]
        if all(val == 0 for val in r_list):
            return(0)
        return(sum(r_count_list)/sum(r_list))
    
    @property
    def total_number_of_ratings(self):
        try:
            r = Rating.objects.get(movie = self)
        except:
            return(0)
        r_count_list = [r.rating_one_count, 
                        r.rating_two_count,
                        r.rating_three_count, 
                        r.rating_four_count, 
                        r.rating_five_count]
        return sum(r_count_list)
    
    
class Cast(models.Model):
    actor = models.ForeignKey(
        Actor,
        on_delete = models.CASCADE,
    )
    movie = models.ForeignKey(
        Movie,
        on_delete = models.CASCADE,
    )
    role = models.CharField(max_length = 50)
    is_debut_movie = models.BooleanField(default = False)

class Rating(models.Model):
    movie = models.OneToOneField(
        Movie,
        on_delete = models.CASCADE
    )
    # rating = models.IntegerField(choices = choice_rating, default = 0)
    rating_one_count = models.IntegerField(default = 0)
    rating_two_count = models.IntegerField(default = 0)
    rating_three_count = models.IntegerField(default = 0)
    rating_four_count = models.IntegerField(default = 0)
    rating_five_count = models.IntegerField(default = 0)