from django.forms import ModelForm
from .models　import House
#.modelsはmodel.pyをさす

Class House(ModelForm):
    class Meta:
      model=House
      fields=['house_station','house_walk','house_year']
