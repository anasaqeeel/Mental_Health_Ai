from rest_framework import viewsets
from .models import (
    UserProfile,
    Video,
    UserVideo,
    UserQuestionnaire,
    MHProfessional,
    MMPI2Questionnaire,
    ADHD,
    IBT,
    OCIR,
    MDQ,
    GAD,
    BDI,
    ENNEAGRAM,
    NPQ,
)
from .serializers import (
    UserProfileSerializer,
    VideoSerializer,
    MMPI2QuestionnaireSerializer,
    ENNEAGRAMSerializer,
    UserVideoSerializer,
    UserQuestionnaireSerializer,
    BFTQuestionnaireSerializer,
    ADHDSerializer,
    IBTSerializer,
    OCIRSerializer,
    MDQSerializer,
    GADSerializer,
    BDISerializer,
    NPQSerializer,
)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

import os
import subprocess
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from app.VideoAnalysis.speechToText import audio_to_text,video_to_audio
from app.VideoAnalysis.emotionDetector import analyze_emotions, summarize_emotions
from app.TextAnalysis.Diagnoser import Diagnose

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class VideoViewSet(viewsets.ModelViewSet):
    # queryset = Video.objects.all()
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video_instance = serializer.save()
            video_file = video_instance.video_file.path
            print("video file obtained: ",video_file)
            audio_file = "output_audio.wav"

            video_to_audio(video_file, audio_file)
            text_output = audio_to_text(audio_file)
            # Generate transcript
            transcript = audio_to_text(audio_file)
            video_instance.transcript = transcript

            # Perform emotion analysis
            emotions = analyze_emotions(video_instance.video_file.path,interval=5)
            summary = summarize_emotions(emotions)
            video_instance.emotions_summary = summary

            video_instance.save()
            return Response(UserVideoSerializer(video_instance).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MMPI2QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = MMPI2Questionnaire.objects.all()
    serializer_class = MMPI2QuestionnaireSerializer

class UploadVideoView(APIView):
    def post(self, request):
            serializer = UserVideoSerializer(data=request.data)
            if serializer.is_valid():
                user_video = serializer.save()
                video_file = user_video.video.path
                video_file = str(video_file)

                # Define a new path for the remuxed video
                fixed_video_file = os.path.splitext(video_file)[0] + '_fixed.mp4'

                # Set the path to ffmpeg
                ffmpeg_path = r"C:\Users\avira\OneDrive\Desktop\Github-Projects\TIET_Mental_Health\backend\ffmpeg\bin\ffmpeg.exe"

                if not os.path.isfile(ffmpeg_path):
                    return Response({"error": "FFmpeg executable not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Run ffmpeg to remux the video and fix metadata
                ffmpeg_remux_cmd = [ffmpeg_path, '-i', video_file, '-c', 'copy', fixed_video_file]

                try:
                    subprocess.run(ffmpeg_remux_cmd, check=True)
                    print(f"Remuxed video saved as: {fixed_video_file}")
                except subprocess.CalledProcessError as e:
                    print(f"Error remuxing video: {e}")
                    return Response({"error": "Failed to remux video"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Further processing: audio extraction, emotion analysis, etc.

                audio_file = os.path.splitext(fixed_video_file)[0] + '_audio.wav'
                # Step 1: Extract audio
                video_to_audio(fixed_video_file, audio_file)

                # Step 2: Generate transcript
                transcript = audio_to_text(audio_file)

                # Update the transcript field of the saved instance
                user_video.transcript = transcript

                # Step 3: Analyze emotions in the video
                emotions = analyze_emotions(fixed_video_file, interval=3)
                summary = summarize_emotions(emotions)

                user_video.emotions = emotions
                user_video.save()
                return Response({"message": "Video processed successfully"}, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ADHDViewSet(viewsets.ModelViewSet):
    queryset = ADHD.objects.all()
    serializer_class = ADHDSerializer


class IBTViewSet(viewsets.ModelViewSet):
    queryset = IBT.objects.all()
    serializer_class = IBTSerializer


class OCIRViewSet(viewsets.ModelViewSet):
    queryset = OCIR.objects.all()
    serializer_class = OCIRSerializer


class MDQViewSet(viewsets.ModelViewSet):
    queryset = MDQ.objects.all()
    serializer_class = MDQSerializer


class GADViewSet(viewsets.ModelViewSet):
    queryset = GAD.objects.all()
    serializer_class = GADSerializer


class BDIViewSet(viewsets.ModelViewSet):
    queryset = BDI.objects.all()
    serializer_class = BDISerializer
class ENNEAGRAMViewSet(viewsets.ModelViewSet):
    queryset = ENNEAGRAM.objects.all()
    serializer_class = ENNEAGRAMSerializer


class NPQViewSet(viewsets.ModelViewSet):
    queryset = NPQ.objects.all()
    serializer_class = NPQSerializer
class UserQuestionnaireCreateView(APIView):
    def post(self, request):
        serializer = UserQuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            questionnaire=serializer.save()
            diag_list=Diagnose(questionnaire.issue)
            tags=""
            for diag_tuple in diag_list:
                for diag in diag_tuple:
                    tags=tags+diag
                    tags=tags+","
            questionnaire.tags=tags
            questionnaire.save()
            return Response(UserQuestionnaireSerializer(questionnaire).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class BFTQuestionnaireCreateView(APIView):
    def post(self, request):
        serializer = BFTQuestionnaireSerializer(data=request.data)
        if serializer.is_valid():
            bft_questionnaire = serializer.save()
            return Response(BFTQuestionnaireSerializer(bft_questionnaire).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_matched_professionals(request):
    questionnaire = UserQuestionnaire.objects.order_by('-created_at').first()
    professionals = MHProfessional.objects.all()
    matched_professionals = []

    for prof in professionals:
        score = 0

        tags=questionnaire.tags
        diag_list=tags.split(',')

        specialization=prof.specialization
        spec_list=specialization.split(',')

        # Specialization and tags matching
        for diag in diag_list:
            for spec in spec_list:
                if(diag==spec):
                    score+=50

        #language matching
        if prof.language1==questionnaire.preferredLang:
            score+=30
        elif prof.language2==questionnaire.preferredLang:
            score+=20
        elif prof.language3==questionnaire.preferredLang:
            score+=10

        #therapy spec
        if prof.therapy_specification == questionnaire.typeOfTherapy:
            score += 10
    
        if prof.gender == questionnaire.providerGender:
            score += 15
        # Add more criteria based on your matching algorithm

        matched_professionals.append((prof, score))

    # Sort professionals by score and select top 3
    matched_professionals = sorted(matched_professionals, key=lambda x: x[1], reverse=True)[:3]
    matched_professionals = [prof[0] for prof in matched_professionals]

    # Serialize and return the response
    data = {
        'professionals': [
            {
                'name': prof.name,
                'photo': prof.photo.url if prof.photo else None,
                'email':prof.email,
                'phone':prof.phone,
                'therapy_specification': prof.therapy_specification,
                'gender': prof.gender,
                'language1': prof.language1,
                'language2': prof.language2,
                'language3': prof.language3,
                'specialization': prof.specialization
            } for prof in matched_professionals
        ]
    }
    return JsonResponse(data)