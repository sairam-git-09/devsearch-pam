from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/<id>'},
        {'POST': '/api/projects/<id>/vote'},
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]

    # safe=False allows non-dict (list) to be serialized
    return Response(routes)



@api_view(['GET'])
def getProjects(request):
    
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def getProject(request, pk):
    
    projects = Project.objects.get(id = pk)
    serializer = ProjectSerializer(projects, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    
    project = Project.objects.get(id = pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )
    
    review.value = data['value']
    review.save()
    project.getVoteCount
    serializer = ProjectSerializer(project, many=False)
    
    return Response(serializer.data)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removetags(request):
    
    project_id = request.data.get('project_id')
    tag_id = request.data.get('tag_id')
   
    project = Project.objects.get(id=project_id)
    tag = Tag.objects.get(id=tag_id)
    
    project.tags.remove(tag)
    
    return Response({'detail': 'Tag removed from project'})
    