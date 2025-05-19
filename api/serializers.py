#form,modelform
#serializer,modelserializer

from rest_framework import serializers
from bookapp.models import Book
class BookSerializer(serializers.Serializer):
    title=serializers.CharField()
    author=serializers.CharField()
    price=serializers.IntegerField()
    published_date=serializers.DateField()

    def create(self, validated_data):
            # Create a new Book object
        return Book.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
            # Update the book instance with the validated data
            instance.title = validated_data.get('title', instance.title)
            instance.author = validated_data.get('author', instance.author)
            instance.price = validated_data.get('price', instance.price)
            instance.published_date = validated_data.get('published_date', instance.published_date)
            instance.save()
            return instance
    
   