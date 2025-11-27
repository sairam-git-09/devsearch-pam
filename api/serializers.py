from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile, Skill, Message

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    '''tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )
    
    owner = serializers.ReadOnlyField(source='owner.username')'''
    
    tags = TagSerializer(many=True)
    owner = ProfileSerializer(many=False)
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
        
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serialized_reviews = ReviewSerializer(reviews, many=True).data
        return serialized_reviews