from django.shortcuts import render,get_object_or_404

from rest_framework.generics import ListAPIView
from rest_framework import authentication,permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from course_management.serializers import CourseSerializer
from course_management.models import Course
from accounts.permissions import IsOwner

# Create your views here.

class CourseListCreateView(APIView):
    
    authentication_classes = [authentication.TokenAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]
    
    # serializer_class = CourseSerializer
    
    # def get_queryset(self):
    #     return Course.objects.filter(trainer=self.request.user)
    
    def get(self,request):
        
        qs = Course.objects.filter(trainer=request.user)
        
        serializer_instance = CourseSerializer(qs,many=True)
        
        return Response(serializer_instance.data)
    
    def post(self,request):
        
        form_data = request.data
        
        serializer_instance = CourseSerializer(data=form_data)
        
        if serializer_instance.is_valid():
            serializer_instance.save(trainer=request.user)
            return Response(serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
        
class CourseRetrieveUpdateDeleteView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwner]
    
    def get(self,request,pk=None):
        qs = get_object_or_404(Course,id=pk)
        self.check_object_permissions(request,qs)
        serializer_instance = CourseSerializer(qs)
        return Response(serializer_instance.data)
    
    def put(self,request,pk=None): # patch(self,request,pk=None)
        form_data = request.data
        
        instance = get_object_or_404(Course,id=pk)
        self.check_object_permissions(request,instance)
        
        serilaizer_instance = CourseSerializer(data=form_data,instance=instance) # add => partial = True (for patch)
        
        if serilaizer_instance.is_valid():
            serilaizer_instance.save()
            return Response(serilaizer_instance.data)
        else:
            return Response(serilaizer_instance.errors)
        
    def delete(self,request,pk=None):
        instance = get_object_or_404(Course,id=pk)
        self.check_object_permissions(request,instance)
        instance.delete()
        return Response({"message":"deleted.."})        