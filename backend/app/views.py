from rest_framework import viewsets

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import (
    UserProfile, UserQuestionnaire, ENNEAGRAM, NPQ, ADHD, 
    BFTQuestionnaire, MMPI2Questionnaire, BDI, GAD, OCIR, MDQ, IBT
)
from rest_framework import status
from rest_framework.response import Response

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

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile, ADHD, GAD, MDQ  # Ensure MDQ is imported

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile, ADHD, GAD, MDQ, BDI  # Ensure BDI is imported

class QuestionnaireReportPDFView(APIView):
    def get(self, request, user_id, questionnaire_type):
        # Log the request
        print(f"Received request for report generation. User ID: {user_id}, Questionnaire Type: {questionnaire_type}")

        # Fetch the user's profile by firebase_uid (not by the 'id')
        try:
            user_profile = UserProfile.objects.get(firebase_uid=user_id)
        except UserProfile.DoesNotExist:
            print(f"UserProfile not found for user_id: {user_id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the corresponding questionnaire data based on the questionnaire_type
        questionnaire = None
        if questionnaire_type == "ADHD":
            try:
                questionnaire = ADHD.objects.filter(user=user_profile).first()
                if not questionnaire:
                    print(f"ADHD Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "ADHD Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            except ADHD.DoesNotExist:
                print(f"ADHD Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "ADHD Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
        
        elif questionnaire_type == "GAD":
            try:
                questionnaire = GAD.objects.filter(user=user_profile).first()
                if not questionnaire:
                    print(f"GAD Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "GAD Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            except GAD.DoesNotExist:
                print(f"GAD Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "GAD Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)

        elif questionnaire_type == "MDQ":
            try:
                questionnaire = MDQ.objects.filter(user=user_profile).first()
                if not questionnaire:
                    print(f"MDQ Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "MDQ Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            except MDQ.DoesNotExist:
                print(f"MDQ Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "MDQ Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)

        elif questionnaire_type == "BDI":
            try:
                questionnaire = BDI.objects.filter(user=user_profile).first()
                if not questionnaire:
                    print(f"BDI Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "BDI Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            except BDI.DoesNotExist:
                print(f"BDI Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "BDI Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
        if questionnaire_type == "NPQ":
            try:
                questionnaire = NPQ.objects.filter(user=user_profile.firebase_uid).first()
                if not questionnaire:
                    print(f"NPQ Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "NPQ Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            except NPQ.DoesNotExist:
                print(f"NPQ Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "NPQ Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
        elif questionnaire_type == "BFT":
            try:
                questionnaire = BFTQuestionnaire.objects.filter(user=user_profile.firebase_uid).first()
                if not questionnaire:
                    print(f"BFT Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "BFT Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            except BFTQuestionnaire.DoesNotExist:
                print(f"BFT Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "BFT Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
        elif questionnaire_type == "OCIR":
            try:
                questionnaire = OCIR.objects.filter(user=user_profile).first()
                if not questionnaire:
                    print(f"OCIR Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "OCIR Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            except OCIR.DoesNotExist:
                print(f"OCIR Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "OCIR Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
        elif questionnaire_type == "MMPI2Questionnaire":
            try:
                questionnaire = MMPI2Questionnaire.objects.filter(user=user_profile).first()
                if not questionnaire:
                    print(f"OCIR Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "OCIR Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            except MMPI2Questionnaire.DoesNotExist:
                print(f"OCIR Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "OCIR Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
        elif questionnaire_type == "ENNEAGRAM":
            try:
                questionnaire = ENNEAGRAM.objects.filter(user=user_profile).first()
                if not questionnaire:
                    print(f"OCIR Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "OCIR Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            except ENNEAGRAM.DoesNotExist:
                print(f"OCIR Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "OCIR Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)


        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{questionnaire_type}_Report_{user_id}.pdf"'

        # Generate the PDF content
        p = canvas.Canvas(response, pagesize=letter)
        p.drawString(100, 750, f"{questionnaire_type} Report for User: {user_profile.name}")

        if questionnaire_type == "ADHD":
            p.drawString(100, 730, f"Trouble Wrapping Up Final Details: {questionnaire.troubleWrappingUpFinalDetails}")
            p.drawString(100, 710, f"Difficulty Getting Organized: {questionnaire.difficultyGettingOrganized}")
            p.drawString(100, 690, f"Problems Remembering Appointments: {questionnaire.problemsRememberingAppointments}")
            p.drawString(100, 670, f"Avoid Delaying Thought-Intensive Tasks: {questionnaire.avoidDelayingThoughtIntensiveTasks}")
            p.drawString(100, 650, f"Fidget or Squirm When Sitting: {questionnaire.fidgetOrSquirmWhenSitting}")
            p.drawString(100, 630, f"Feel Overly Active or Compelled: {questionnaire.feelOverlyActiveCompelled}")
            p.drawString(100, 610, f"Make Careless Mistakes: {questionnaire.makeCarelessMistakes}")
            p.drawString(100, 590, f"Difficulty Keeping Attention: {questionnaire.difficultyKeepingAttention}")
            p.drawString(100, 570, f"Difficulty Concentrating on Direct Speech: {questionnaire.difficultyConcentratingOnDirectSpeech}")
            p.drawString(100, 550, f"Misplace or Difficulty Finding Things: {questionnaire.misplaceOrDifficultyFindingThings}")

        elif questionnaire_type == "GAD":
            p.drawString(100, 730, f"Feeling Nervous: {questionnaire.feelingNervous}")
            p.drawString(100, 710, f"Inability to Control Worrying: {questionnaire.inabilityToControlWorrying}")
            p.drawString(100, 690, f"Excessive Worrying: {questionnaire.excessiveWorrying}")
            p.drawString(100, 670, f"Trouble Relaxing: {questionnaire.troubleRelaxing}")
            p.drawString(100, 650, f"Restlessness: {questionnaire.restlessness}")
            p.drawString(100, 630, f"Irritability: {questionnaire.irritability}")
            p.drawString(100, 610, f"Fear of Something Awful: {questionnaire.fearOfSomethingAwful}")

        elif questionnaire_type == "MDQ":
            p.drawString(100, 730, f"Feel Dependent On Others: {questionnaire.feelDependentOnOthers}")
            p.drawString(100, 710, f"Avoid Independent Decision Making: {questionnaire.avoidIndependentDecisionMaking}")
            p.drawString(100, 690, f"Feel Weak Or Tired: {questionnaire.feelWeakOrTired}")
            p.drawString(100, 670, f"Difficulty Concentrating: {questionnaire.difficultyConcentrating}")
            p.drawString(100, 650, f"Feel Dissatisfied With Self: {questionnaire.feelDissatisfiedWithSelf}")
            p.drawString(100, 630, f"Consider Self A Failure: {questionnaire.considerSelfAFailure}")
            p.drawString(100, 610, f"Trouble Controlling Temper: {questionnaire.troubleControllingTemper}")
            p.drawString(100, 590, f"Hesitate When Making Decisions: {questionnaire.hesitateWhenMakingDecisions}")
            p.drawString(100, 570, f"Rely On Others For Decisions: {questionnaire.relyOnOthersForDecisions}")
            p.drawString(100, 550, f"Feel Hyper To The Point Of Concern: {questionnaire.feelHyperToThePointOfConcern}")
            p.drawString(100, 530, f"Irritability Leading To Conflict: {questionnaire.irritabilityLeadingToConflict}")
            p.drawString(100, 510, f"Increased Self Confidence: {questionnaire.increasedSelfConfidence}")
            p.drawString(100, 490, f"Less Sleep Than Usual: {questionnaire.lessSleepThanUsual}")
            p.drawString(100, 470, f"More Talkative Than Usual: {questionnaire.moreTalkativeThanUsual}")
            p.drawString(100, 450, f"Racing Thoughts: {questionnaire.racingThoughts}")
            p.drawString(100, 430, f"Easily Distracted: {questionnaire.easilyDistracted}")
            p.drawString(100, 410, f"More Energy Than Usual: {questionnaire.moreEnergyThanUsual}")
            p.drawString(100, 390, f"More Active Than Usual: {questionnaire.moreActiveThanUsual}")
            p.drawString(100, 370, f"More Social Than Usual: {questionnaire.moreSocialThanUsual}")
        
        if questionnaire_type == "NPQ":
            p.drawString(100, 730, f"Feel Dependent On Others: {questionnaire.feelDependentOnOthers}")
            p.drawString(100, 710, f"Avoid Independent Decisions: {questionnaire.avoidIndependentDecisions}")
            p.drawString(100, 690, f"Feel Weak Or Tired: {questionnaire.feelWeakOrTired}")
            p.drawString(100, 670, f"Find It Difficult To Concentrate: {questionnaire.findItDifficultToConcentrate}")
            p.drawString(100, 650, f"Frequently Dissatisfied With Self: {questionnaire.frequentlyDissatisfiedWithSelf}")
            p.drawString(100, 630, f"Consider Self A Failure: {questionnaire.considerSelfAFailure}")
            p.drawString(100, 610, f"Trouble Controlling Temper: {questionnaire.troubleControllingTemper}")
            p.drawString(100, 590, f"Hesitate When Making Decisions: {questionnaire.hesitateWhenMakingDecisions}")
            p.drawString(100, 570, f"Rely On Others For Decisions: {questionnaire.relyOnOthersForDecisions}")
        elif questionnaire_type == "BFT":
            p.drawString(100, 730, f"Talks A Lot: {questionnaire.talksALot}")
            p.drawString(100, 710, f"Notices Weak Points: {questionnaire.noticesWeakPoints}")
            p.drawString(100, 690, f"Does Things Carefully: {questionnaire.doesThingsCarefully}")
            p.drawString(100, 670, f"Is Sad/Depressed: {questionnaire.isSadDepressed}")
            p.drawString(100, 650, f"Is Original: {questionnaire.isOriginal}")
            p.drawString(100, 630, f"Keeps Thoughts to Themselves: {questionnaire.keepsThoughtsToThemselves}")
            p.drawString(100, 610, f"Is Helpful Not Selfish: {questionnaire.isHelpfulNotSelfish}")
            p.drawString(100, 590, f"Is Careless: {questionnaire.isCareless}")
            p.drawString(100, 570, f"Is Relaxed: {questionnaire.isRelaxed}")
            p.drawString(100, 550, f"Is Curious: {questionnaire.isCurious}")
        elif questionnaire_type == "OCIR":
            p.drawString(100, 730, f"Saved Too Many Things: {questionnaire.savedTooManyThings}")
            p.drawString(100, 710, f"Check Things More Often: {questionnaire.checkThingsMoreOften}")
            p.drawString(100, 690, f"Upset If Not Arranged Properly: {questionnaire.upsetIfNotArrangedProperly}")
            p.drawString(100, 670, f"Compelled To Count: {questionnaire.compelledToCount}")
            p.drawString(100, 650, f"Difficult To Touch Touched Objects: {questionnaire.difficultToTouchTouchedObjects}")
            p.drawString(100, 630, f"Difficult To Control Thoughts: {questionnaire.difficultToControlThoughts}")
            p.drawString(100, 610, f"Collect Unnecessary Things: {questionnaire.collectUnnecessaryThings}")
            p.drawString(100, 590, f"Repeatedly Check Items: {questionnaire.repeatedlyCheckItems}")
            p.drawString(100, 570, f"Upset If Others Change Arrangement: {questionnaire.upsetIfOthersChangeArrangement}")
            p.drawString(100, 550, f"Feel Compelled To Repeat Numbers: {questionnaire.feelCompelledToRepeatNumbers}")


        elif questionnaire_type == "BDI":
            p.drawString(100, 730, f"Feelings Of Sadness: {questionnaire.feelingsOfSadness}")
            p.drawString(100, 710, f"Thoughts About Future: {questionnaire.thoughtsAboutFuture}")
            p.drawString(100, 690, f"Definition Of Success: {questionnaire.definitionOfSuccess}")
            p.drawString(100, 670, f"Ability To Experience Pleasure: {questionnaire.abilityToExperiencePleasure}")
            p.drawString(100, 650, f"Negative Self Statements: {questionnaire.negativeSelfStatements}")
            p.drawString(100, 630, f"Feelings Of Punishment: {questionnaire.feelingsOfPunishment}")
            p.drawString(100, 610, f"Disappointments In Self: {questionnaire.disappointmentsInSelf}")
            p.drawString(100, 590, f"Handling Self Criticism: {questionnaire.handlingSelfCriticism}")
            p.drawString(100, 570, f"Thoughts Of Self Harm: {questionnaire.thoughtsOfSelfHarm}")
            p.drawString(100, 550, f"Frequency Of Crying: {questionnaire.frequencyOfCrying}")
        elif questionnaire_type == "ENNEAGRAM":
            p.drawString(100, 730, f"Creative Artistic View: {questionnaire.creativeArtisticView}")
            p.drawString(100, 710, f"Feel Different From Others: {questionnaire.feelDifferentFromOthers}")
            p.drawString(100, 690, f"Experience Melancholy: {questionnaire.experienceMelancholy}")
            p.drawString(100, 670, f"Overly Sensitive: {questionnaire.overlySensitive}")
            p.drawString(100, 650, f"Feel Something Is Missing: {questionnaire.feelSomethingIsMissing}")
            p.drawString(100, 630, f"Feel Envious Of Others: {questionnaire.feelEnviousOfOthers}")
            p.drawString(100, 610, f"Thrive In Creative Environments: {questionnaire.thriveInCreativeEnvironments}")
            p.drawString(100, 590, f"Become Withdrawn When Misunderstood: {questionnaire.canBecomeWithdrawnWhenMisunderstood}")
            p.drawString(100, 570, f"Romantic Longing: {questionnaire.romanticLonging}")
            p.drawString(100, 550, f"Caught In Fantasy World: {questionnaire.caughtInFantasyWorld}")
            p.drawString(100, 530, f"Enjoy Unique Elegant Things: {questionnaire.enjoyUniqueElegantThings}")
            p.drawString(100, 510, f"Moody When Stressed: {questionnaire.moodyWhenStressed}")
            p.drawString(100, 490, f"Reflective And Search For Meaning: {questionnaire.reflectiveAndSearchForMeaning}")
            p.drawString(100, 470, f"Strive To Be Unique: {questionnaire.striveToBeUnique}")
            p.drawString(100, 450, f"Manners And Good Taste: {questionnaire.mannersAndGoodTaste}")
            p.drawString(100, 430, f"Seen As Overly Dramatic: {questionnaire.seenAsOverlyDramatic}")
            p.drawString(100, 410, f"Important To Understand Feelings: {questionnaire.importantToUnderstandFeelings}")
        elif questionnaire_type == "MMPI2Questionnaire":
            p.drawString(100, 730, f"Rarely Worry About Health: {questionnaire.rarelyWorryAboutHealth}")
            p.drawString(100, 710, f"Always Tell The Truth: {questionnaire.alwaysTellTruth}")
            p.drawString(100, 690, f"Feel Tired Most Of The Time: {questionnaire.feelTiredMostOfTheTime}")
            p.drawString(100, 670, f"Feel Punished Without Cause: {questionnaire.feelPunishedWithoutCause}")
            p.drawString(100, 650, f"Bothered By Upset Stomach: {questionnaire.botheredByUpsetStomach}")
            p.drawString(100, 630, f"Get A Lot Of Headaches: {questionnaire.getLotOfHeadaches}")
            p.drawString(100, 610, f"Like To Arrange Flowers: {questionnaire.likeToArrangeFlowers}")
            p.drawString(100, 590, f"Someone Has It In For Me: {questionnaire.someoneHasItInForMe}")
            p.drawString(100, 570, f"Often Disturbing Thoughts: {questionnaire.oftenDisturbingThoughts}")
            p.drawString(100, 550, f"Hear Things Others Can't Hear: {questionnaire.hearThingsOthersCantHear}")
            p.drawString(100, 530, f"Am Happier Than Most People: {questionnaire.amHappierThanMostPeople}")
            p.drawString(100, 510, f"Am Easily Embarrassed: {questionnaire.amEasilyEmbarrassed}")

        p.showPage()
        p.save()
        print(f"PDF report generated successfully for user: {user_profile.name}, questionnaire type: {questionnaire_type}")

        return response


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
    def create(self, request, *args, **kwargs):
        # Get the user by firebase_uid passed from the frontend
        user_profile = UserProfile.objects.get(firebase_uid=request.data['user'])  # Ensure this exists
        adhd_data = request.data.copy()  # Create a mutable copy of the data
        adhd_data['user'] = user_profile.id  # Assign the user profile to the 'user' field
        
        serializer = self.get_serializer(data=adhd_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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