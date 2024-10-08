from rest_framework import serializers
from .models import UserProfile, Video, UserVideo, UserQuestionnaire,BFTQuestionnaire,MMPI2Questionnaire,ADHD,IBT,OCIR,MDQ,GAD,BDI,ADHD,NPQ,ENNEAGRAM

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'created_at']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'user', 'video_file', 'transcript', 'emotions_summary', 'uploaded_at']


class MMPI2QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = MMPI2Questionnaire
        fields = '__all__'
class NPQSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPQ
        fields = '__all__'

class ADHDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHD
        fields = '__all__'


class ENNEAGRAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = ENNEAGRAM
        fields = '__all__'

class BDISerializer(serializers.ModelSerializer):
    class Meta:
        model = BDI
        fields = '__all__'

class GADSerializer(serializers.ModelSerializer):
    class Meta:
        model = GAD
        fields = '__all__'

class MDQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MDQ
        fields = '__all__'

class OCIRSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCIR
        fields = '__all__'

class IBTSerializer(serializers.ModelSerializer):
    class Meta:
        model = IBT
        fields = '__all__'

class UserVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVideo
        fields = ['user', 'video', 'transcript' , 'emotions']  # Ensure these fields match your model

class UserQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestionnaire
        fields = '__all__'
class BFTQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = BFTQuestionnaire
        fields = '__all__'

