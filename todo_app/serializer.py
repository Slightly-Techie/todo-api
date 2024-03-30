from rest_framework import serializers
from .models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ['id', 'title', 'description', 'completed', 'date_created']


# class ToDoViewSet(viewsets.ModelViewSet):
#     queryset = ToDo.objects.all()
#     serializer_class = ToDoSerializer
