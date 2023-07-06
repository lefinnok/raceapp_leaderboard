from django.db import models
from django.contrib.auth.models import User
from .fields import FloatListField

# Create your models here.

class Competitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    laps = FloatListField(blank=True)
    current_best = models.FloatField(default = -1.0, blank=True)


    class Meta:
        ordering = ['current_best']

    def __str__(self):
        return f'{self.user.username + " - " + str(self.laps) + " - " + str(self.current_best)}'
    
    def update_current_best(self):
        lap_scores = self.laps
        if lap_scores is None or len(lap_scores) < 3:
            self.current_best = -1.0
            return
        current_best_consequetives = [-1,-1,-1]
        consequetive_queue_buffer = []        
        #cumulation = 0
        previous_lap_score = -1
        for lap_score in lap_scores:
            if lap_score <= 0:
                previous_lap_score = lap_score
                continue
            if previous_lap_score <= 0:
                #when the last lap is invalid, reset
                consequetive_queue_buffer = []
            cumulation = len(consequetive_queue_buffer)
            if cumulation < 2:
                consequetive_queue_buffer.append(lap_score)
            elif cumulation == 2:
                consequetive_queue_buffer.append(lap_score)
                if sum(consequetive_queue_buffer) < sum(current_best_consequetives) or sum(current_best_consequetives) < 0:
                    current_best_consequetives = consequetive_queue_buffer.copy()
            else:
                consequetive_queue_buffer.pop(0)
                consequetive_queue_buffer.append(lap_score)
                if sum(consequetive_queue_buffer) < sum(current_best_consequetives) or sum(current_best_consequetives) < 0:
                    current_best_consequetives = consequetive_queue_buffer.copy()
            previous_lap_score = lap_score
        
        if current_best_consequetives == [-1,-1,-1]:
            self.current_best = -1.0
        else:
            self.current_best = round(sum(current_best_consequetives),3)
        self.save()
        