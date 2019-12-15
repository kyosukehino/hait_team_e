from django.db import models
from django.utils import timezone

class House(models.Model):#ジャンゴに元々入っているモデルの大枠らしい

  
    class Meta: #Meta情報：データベースの名前を決めるやつ
        db_table='houseimformation'
    
    house_station=models.CharField('駅',max_length=10)
    house_walk=models.IntegerField('徒歩分')
    house_year=models.IntegerField('築年数')
   # house_unknown=models..CharField('未定',max_length=10)
