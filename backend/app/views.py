from rest_framework import viewsets


from datetime import datetime
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from .models import (
    UserProfile, ADHD, GAD, MDQ, BDI, NPQ,
    BFTQuestionnaire, OCIR, MMPI2Questionnaire, ENNEAGRAM
)


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

from reportlab.platypus import Paragraph
from reportlab.lib.units import inch

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
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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

from datetime import datetime
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import (
    UserProfile, ADHD, GAD, MDQ, BDI, NPQ,
    BFTQuestionnaire, OCIR, MMPI2Questionnaire, ENNEAGRAM
)


import logging

# Configure logging
logger = logging.getLogger(__name__)

class QuestionnaireReportPDFView(APIView):
    def get(self, request, user_id, questionnaire_type):
        date_today = datetime.now().strftime("%B %d, %Y")
        logger.info(f"Received request for report generation. User ID: {user_id}, Questionnaire Type: {questionnaire_type}")

        # Fetch the user's profile by firebase_uid
        try:
            user_profile = UserProfile.objects.get(firebase_uid=user_id)
            logger.info(f"Fetched UserProfile: {user_profile}")
        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile not found for user_id: {user_id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Mapping of questionnaire types to their respective model classes and filter logic
        questionnaire_models = {
            "ADHD": {"model": ADHD, "filter_key": "user", "filter_value": user_profile},
            "GAD": {"model": GAD, "filter_key": "user", "filter_value": user_profile},
            "MDQ": {"model": MDQ, "filter_key": "user", "filter_value": user_profile},
            "BDI": {"model": BDI, "filter_key": "user", "filter_value": user_profile},
            "NPQ": {"model": NPQ, "filter_key": "user", "filter_value": user_profile.firebase_uid},
            "BFT": {"model": BFTQuestionnaire, "filter_key": "user", "filter_value": user_profile.firebase_uid},
            "OCIR": {"model": OCIR, "filter_key": "user", "filter_value": user_profile},
            "MMPI2": {"model": MMPI2Questionnaire, "filter_key": "user", "filter_value": user_profile},
            "ENNEAGRAM": {"model": ENNEAGRAM, "filter_key": "user", "filter_value": user_profile}
        }

        # Validate the questionnaire type
        model_info = questionnaire_models.get(questionnaire_type.upper())
        if not model_info:
            logger.error(f"Unsupported questionnaire type: {questionnaire_type}")
            return Response({"error": "Unsupported questionnaire type"}, status=status.HTTP_400_BAD_REQUEST)

        model_class = model_info["model"]
        filter_kwargs = {model_info["filter_key"]: model_info["filter_value"]}

        # Determine ordering field: use 'created_at' if exists, else 'id'
        ordering_field = '-created_at' if hasattr(model_class, 'created_at') else '-id'

        # Fetch the most recent questionnaire entry
        try:
            queryset = model_class.objects.filter(**filter_kwargs).order_by(ordering_field)
            questionnaire = queryset.first()
            if not questionnaire:
                logger.warning(f"{questionnaire_type} Questionnaire not found for user: {user_profile.name}")
                return Response({"error": f"{questionnaire_type} Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            logger.info(f"Fetched {questionnaire_type} Questionnaire with id: {questionnaire.id}")
        except Exception as e:
            logger.exception(f"Error fetching {questionnaire_type} Questionnaire: {str(e)}")
            return Response({"error": f"Error fetching {questionnaire_type} Questionnaire"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{questionnaire_type}_Report_{user_id}.pdf"'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=18, spaceAfter=10))
        styles.add(ParagraphStyle(name='SubtitleStyle', fontName='Helvetica-Oblique', fontSize=12, spaceAfter=20))
        styles.add(ParagraphStyle(name='DateStyle', fontName='Helvetica', fontSize=10, spaceAfter=5))
        styles.add(ParagraphStyle(name='SectionTitle', fontName='Helvetica-Bold', fontSize=14, spaceAfter=10))
        styles.add(ParagraphStyle(name='QuestionStyle', fontName='Helvetica-Bold', fontSize=12, spaceAfter=2))
        styles.add(ParagraphStyle(name='AnswerStyle', fontName='Helvetica', fontSize=12, leftIndent=20, spaceAfter=10))

        story = []

        # Header
        story.append(Paragraph("Mental Health Report", styles['TitleStyle']))
        story.append(Paragraph("Therapy is Healing", styles['SubtitleStyle']))

        # Date
        story.append(Paragraph(f"Date: {date_today}", styles['DateStyle']))
        story.append(Spacer(1, 12))

        # Line Separator
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color='black'))
        story.append(Spacer(1, 12))

        # Section Title
        story.append(Paragraph(f"{questionnaire_type.upper()} Questionnaire", styles['SectionTitle']))

        # Helper function to add question and answer
        def add_question_answer(question, answer):
            story.append(Paragraph(question, styles['QuestionStyle']))
            story.append(Paragraph(str(answer), styles['AnswerStyle']))
            story.append(Spacer(1, 6))

        # Add content based on questionnaire type
        if questionnaire_type.upper() == "ADHD":
            add_question_answer("Trouble Wrapping Up Final Details:", questionnaire.troubleWrappingUpFinalDetails)
            add_question_answer("Difficulty Getting Organized:", questionnaire.difficultyGettingOrganized)
            add_question_answer("Problems Remembering Appointments:", questionnaire.problemsRememberingAppointments)
            add_question_answer("Avoid Delaying Thought-Intensive Tasks:", questionnaire.avoidDelayingThoughtIntensiveTasks)
            add_question_answer("Fidget or Squirm When Sitting:", questionnaire.fidgetOrSquirmWhenSitting)
            add_question_answer("Feel Overly Active or Compelled:", questionnaire.feelOverlyActiveCompelled)
            add_question_answer("Make Careless Mistakes:", questionnaire.makeCarelessMistakes)
            add_question_answer("Difficulty Keeping Attention:", questionnaire.difficultyKeepingAttention)
            add_question_answer("Difficulty Concentrating on Direct Speech:", questionnaire.difficultyConcentratingOnDirectSpeech)
            add_question_answer("Misplace or Difficulty Finding Things:", questionnaire.misplaceOrDifficultyFindingThings)

        elif questionnaire_type.upper() == "GAD":
            add_question_answer("Feeling Nervous:", questionnaire.feelingNervous)
            add_question_answer("Inability to Control Worrying:", questionnaire.inabilityToControlWorrying)
            add_question_answer("Excessive Worrying:", questionnaire.excessiveWorrying)
            add_question_answer("Trouble Relaxing:", questionnaire.troubleRelaxing)
            add_question_answer("Restlessness:", questionnaire.restlessness)
            add_question_answer("Irritability:", questionnaire.irritability)
            add_question_answer("Fear of Something Awful:", questionnaire.fearOfSomethingAwful)

        elif questionnaire_type.upper() == "MDQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decision Making:", questionnaire.avoidIndependentDecisionMaking)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Difficulty Concentrating:", questionnaire.difficultyConcentrating)
            add_question_answer("Feel Dissatisfied With Self:", questionnaire.feelDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)
            add_question_answer("Feel Hyper To The Point Of Concern:", questionnaire.feelHyperToThePointOfConcern)
            add_question_answer("Irritability Leading To Conflict:", questionnaire.irritabilityLeadingToConflict)
            add_question_answer("Increased Self Confidence:", questionnaire.increasedSelfConfidence)
            add_question_answer("Less Sleep Than Usual:", questionnaire.lessSleepThanUsual)
            add_question_answer("More Talkative Than Usual:", questionnaire.moreTalkativeThanUsual)
            add_question_answer("Racing Thoughts:", questionnaire.racingThoughts)
            add_question_answer("Easily Distracted:", questionnaire.easilyDistracted)
            add_question_answer("More Energy Than Usual:", questionnaire.moreEnergyThanUsual)
            add_question_answer("More Active Than Usual:", questionnaire.moreActiveThanUsual)
            add_question_answer("More Social Than Usual:", questionnaire.moreSocialThanUsual)

        elif questionnaire_type.upper() == "BDI":
            add_question_answer("Feelings Of Sadness:", questionnaire.feelingsOfSadness)
            add_question_answer("Thoughts About Future:", questionnaire.thoughtsAboutFuture)
            add_question_answer("Definition Of Success:", questionnaire.definitionOfSuccess)
            add_question_answer("Ability To Experience Pleasure:", questionnaire.abilityToExperiencePleasure)
            add_question_answer("Negative Self Statements:", questionnaire.negativeSelfStatements)
            add_question_answer("Feelings Of Punishment:", questionnaire.feelingsOfPunishment)
            add_question_answer("Disappointments In Self:", questionnaire.disappointmentsInSelf)
            add_question_answer("Handling Self Criticism:", questionnaire.handlingSelfCriticism)
            add_question_answer("Thoughts Of Self Harm:", questionnaire.thoughtsOfSelfHarm)
            add_question_answer("Frequency Of Crying:", questionnaire.frequencyOfCrying)

        elif questionnaire_type.upper() == "NPQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decisions:", questionnaire.avoidIndependentDecisions)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Find It Difficult To Concentrate:", questionnaire.findItDifficultToConcentrate)
            add_question_answer("Frequently Dissatisfied With Self:", questionnaire.frequentlyDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)

        elif questionnaire_type.upper() == "BFT":
            add_question_answer("Talks A Lot:", questionnaire.talksALot)
            add_question_answer("Notices Weak Points:", questionnaire.noticesWeakPoints)
            add_question_answer("Does Things Carefully:", questionnaire.doesThingsCarefully)
            add_question_answer("Is Sad/Depressed:", questionnaire.isSadDepressed)
            add_question_answer("Is Original:", questionnaire.isOriginal)
            add_question_answer("Keeps Thoughts to Themselves:", questionnaire.keepsThoughtsToThemselves)
            add_question_answer("Is Helpful Not Selfish:", questionnaire.isHelpfulNotSelfish)
            add_question_answer("Is Careless:", questionnaire.isCareless)
            add_question_answer("Is Relaxed:", questionnaire.isRelaxed)
            add_question_answer("Is Curious:", questionnaire.isCurious)

        elif questionnaire_type.upper() == "OCIR":
            add_question_answer("Saved Too Many Things:", questionnaire.savedTooManyThings)
            add_question_answer("Check Things More Often:", questionnaire.checkThingsMoreOften)
            add_question_answer("Upset If Not Arranged Properly:", questionnaire.upsetIfNotArrangedProperly)
            add_question_answer("Compelled To Count:", questionnaire.compelledToCount)
            add_question_answer("Difficult To Touch Touched Objects:", questionnaire.difficultToTouchTouchedObjects)
            add_question_answer("Difficult To Control Thoughts:", questionnaire.difficultToControlThoughts)
            add_question_answer("Collect Unnecessary Things:", questionnaire.collectUnnecessaryThings)
            add_question_answer("Repeatedly Check Items:", questionnaire.repeatedlyCheckItems)
            add_question_answer("Upset If Others Change Arrangement:", questionnaire.upsetIfOthersChangeArrangement)
            add_question_answer("Feel Compelled To Repeat Numbers:", questionnaire.feelCompelledToRepeatNumbers)

        elif questionnaire_type.upper() == "MMPI2":
            add_question_answer("Rarely Worry About Health:", questionnaire.rarelyWorryAboutHealth)
            add_question_answer("Always Tell The Truth:", questionnaire.alwaysTellTruth)
            add_question_answer("Feel Tired Most Of The Time:", questionnaire.feelTiredMostOfTheTime)
            add_question_answer("Feel Punished Without Cause:", questionnaire.feelPunishedWithoutCause)
            add_question_answer("Bothered By Upset Stomach:", questionnaire.botheredByUpsetStomach)
            add_question_answer("Get A Lot Of Headaches:", questionnaire.getLotOfHeadaches)
            add_question_answer("Like To Arrange Flowers:", questionnaire.likeToArrangeFlowers)
            add_question_answer("Someone Has It In For Me:", questionnaire.someoneHasItInForMe)
            add_question_answer("Often Disturbing Thoughts:", questionnaire.oftenDisturbingThoughts)
            add_question_answer("Hear Things Others Can't Hear:", questionnaire.hearThingsOthersCantHear)
            add_question_answer("Am Happier Than Most People:", questionnaire.amHappierThanMostPeople)
            add_question_answer("Am Easily Embarrassed:", questionnaire.amEasilyEmbarrassed)

        elif questionnaire_type.upper() == "ENNEAGRAM":
            add_question_answer("Creative Artistic View:", questionnaire.creativeArtisticView)
            add_question_answer("Feel Different From Others:", questionnaire.feelDifferentFromOthers)
            add_question_answer("Experience Melancholy:", questionnaire.experienceMelancholy)
            add_question_answer("Overly Sensitive:", questionnaire.overlySensitive)
            add_question_answer("Feel Something Is Missing:", questionnaire.feelSomethingIsMissing)
            add_question_answer("Feel Envious Of Others:", questionnaire.feelEnviousOfOthers)
            add_question_answer("Thrive In Creative Environments:", questionnaire.thriveInCreativeEnvironments)
            add_question_answer("Become Withdrawn When Misunderstood:", questionnaire.canBecomeWithdrawnWhenMisunderstood)
            add_question_answer("Romantic Longing:", questionnaire.romanticLonging)
            add_question_answer("Caught In Fantasy World:", questionnaire.caughtInFantasyWorld)
            add_question_answer("Enjoy Unique Elegant Things:", questionnaire.enjoyUniqueElegantThings)
            add_question_answer("Moody When Stressed:", questionnaire.moodyWhenStressed)
            add_question_answer("Reflective And Search For Meaning:", questionnaire.reflectiveAndSearchForMeaning)
            add_question_answer("Strive To Be Unique:", questionnaire.striveToBeUnique)
            add_question_answer("Manners And Good Taste:", questionnaire.mannersAndGoodTaste)
            add_question_answer("Seen As Overly Dramatic:", questionnaire.seenAsOverlyDramatic)
            add_question_answer("Important To Understand Feelings:", questionnaire.importantToUnderstandFeelings)

        else:
            logger.error(f"Unsupported questionnaire type: {questionnaire_type}")
            return Response({"error": "Unsupported questionnaire type"}, status=status.HTTP_400_BAD_REQUEST)

        # Build the PDF
        try:
            doc.build(story)
        except Exception as e:
            logger.exception(f"Error building PDF: {str(e)}")
            return Response({"error": "Error generating PDF"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Move the buffer's position to the beginning
        buffer.seek(0)

        # Write the buffer to the response
        response.write(buffer.getvalue())
        buffer.close()

        logger.info(f"PDF report generated successfully for user: {user_profile.name}, questionnaire type: {questionnaire_type}")

        return response
    
    def get(self, request, user_id, questionnaire_type):
        date_today = datetime.now().strftime("%B %d, %Y")
        print(f"Received request for report generation. User ID: {user_id}, Questionnaire Type: {questionnaire_type}")

        # Fetch the user's profile by firebase_uid
        try:
            user_profile = UserProfile.objects.get(firebase_uid=user_id)
        except UserProfile.DoesNotExist:
            print(f"UserProfile not found for user_id: {user_id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Mapping of questionnaire types to their respective model classes and filter logic
        questionnaire_models = {
            "ADHD": {"model": ADHD, "filter_key": "user", "filter_value": user_profile},
            "GAD": {"model": GAD, "filter_key": "user", "filter_value": user_profile},
            "MDQ": {"model": MDQ, "filter_key": "user", "filter_value": user_profile},
            "BDI": {"model": BDI, "filter_key": "user", "filter_value": user_profile},
            "NPQ": {"model": NPQ, "filter_key": "user", "filter_value": user_profile.firebase_uid},
            "BFT": {"model": BFTQuestionnaire, "filter_key": "user", "filter_value": user_profile.firebase_uid},
            "OCIR": {"model": OCIR, "filter_key": "user", "filter_value": user_profile},
            "MMPI2": {"model": MMPI2Questionnaire, "filter_key": "user", "filter_value": user_profile},
            "ENNEAGRAM": {"model": ENNEAGRAM, "filter_key": "user", "filter_value": user_profile}
        }

        # Validate the questionnaire type
        model_info = questionnaire_models.get(questionnaire_type.upper())
        if not model_info:
            print(f"Unsupported questionnaire type: {questionnaire_type}")
            return Response({"error": "Unsupported questionnaire type"}, status=status.HTTP_400_BAD_REQUEST)

        model_class = model_info["model"]
        filter_kwargs = {model_info["filter_key"]: model_info["filter_value"]}

        # Fetch the most recent questionnaire entry by ordering descending by 'id'
        try:
            queryset = model_class.objects.filter(**filter_kwargs).order_by('-created_at').first()
            print(f"Queryset for {questionnaire_type.upper()}: {[q.id for q in queryset]}")
            questionnaire = queryset.first()
            # questionnaire = model_class.objects.filter(**filter_kwargs).order_by('-id').first()
            if not questionnaire:
                print(f"{questionnaire_type} Questionnaire not found for user: {user_profile.name}")
                return Response({"error": f"{questionnaire_type} Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            print(f"Fetched {questionnaire_type} Questionnaire with id: {questionnaire.id}")
        except Exception as e:
            print(f"Error fetching {questionnaire_type} Questionnaire: {str(e)}")
            return Response({"error": f"Error fetching {questionnaire_type} Questionnaire"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{questionnaire_type}_Report_{user_id}.pdf"'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=18, spaceAfter=10))
        styles.add(ParagraphStyle(name='SubtitleStyle', fontName='Helvetica-Oblique', fontSize=12, spaceAfter=20))
        styles.add(ParagraphStyle(name='DateStyle', fontName='Helvetica', fontSize=10, spaceAfter=5))
        styles.add(ParagraphStyle(name='SectionTitle', fontName='Helvetica-Bold', fontSize=14, spaceAfter=10))
        styles.add(ParagraphStyle(name='QuestionStyle', fontName='Helvetica-Bold', fontSize=12, spaceAfter=2))
        styles.add(ParagraphStyle(name='AnswerStyle', fontName='Helvetica', fontSize=12, leftIndent=20, spaceAfter=10))

        story = []

        # Header
        story.append(Paragraph("Mental Health Report", styles['TitleStyle']))
        story.append(Paragraph("Therapy is Healing", styles['SubtitleStyle']))

        # Date (Removed 'Created At')
        story.append(Paragraph(f"Date: {date_today}", styles['DateStyle']))
        story.append(Spacer(1, 12))

        # Line Separator
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color='black'))
        story.append(Spacer(1, 12))

        # Section Title
        story.append(Paragraph(f"{questionnaire_type.upper()} Questionnaire", styles['SectionTitle']))

        # Helper function to add question and answer
        def add_question_answer(question, answer):
            story.append(Paragraph(question, styles['QuestionStyle']))
            story.append(Paragraph(str(answer), styles['AnswerStyle']))
            story.append(Spacer(1, 6))

        # Add content based on questionnaire type
        if questionnaire_type.upper() == "ADHD":
            add_question_answer("Trouble Wrapping Up Final Details:", questionnaire.troubleWrappingUpFinalDetails)
            add_question_answer("Difficulty Getting Organized:", questionnaire.difficultyGettingOrganized)
            add_question_answer("Problems Remembering Appointments:", questionnaire.problemsRememberingAppointments)
            add_question_answer("Avoid Delaying Thought-Intensive Tasks:", questionnaire.avoidDelayingThoughtIntensiveTasks)
            add_question_answer("Fidget or Squirm When Sitting:", questionnaire.fidgetOrSquirmWhenSitting)
            add_question_answer("Feel Overly Active or Compelled:", questionnaire.feelOverlyActiveCompelled)
            add_question_answer("Make Careless Mistakes:", questionnaire.makeCarelessMistakes)
            add_question_answer("Difficulty Keeping Attention:", questionnaire.difficultyKeepingAttention)
            add_question_answer("Difficulty Concentrating on Direct Speech:", questionnaire.difficultyConcentratingOnDirectSpeech)
            add_question_answer("Misplace or Difficulty Finding Things:", questionnaire.misplaceOrDifficultyFindingThings)

        elif questionnaire_type.upper() == "GAD":
            add_question_answer("Feeling Nervous:", questionnaire.feelingNervous)
            add_question_answer("Inability to Control Worrying:", questionnaire.inabilityToControlWorrying)
            add_question_answer("Excessive Worrying:", questionnaire.excessiveWorrying)
            add_question_answer("Trouble Relaxing:", questionnaire.troubleRelaxing)
            add_question_answer("Restlessness:", questionnaire.restlessness)
            add_question_answer("Irritability:", questionnaire.irritability)
            add_question_answer("Fear of Something Awful:", questionnaire.fearOfSomethingAwful)

        elif questionnaire_type.upper() == "MDQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decision Making:", questionnaire.avoidIndependentDecisionMaking)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Difficulty Concentrating:", questionnaire.difficultyConcentrating)
            add_question_answer("Feel Dissatisfied With Self:", questionnaire.feelDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)
            add_question_answer("Feel Hyper To The Point Of Concern:", questionnaire.feelHyperToThePointOfConcern)
            add_question_answer("Irritability Leading To Conflict:", questionnaire.irritabilityLeadingToConflict)
            add_question_answer("Increased Self Confidence:", questionnaire.increasedSelfConfidence)
            add_question_answer("Less Sleep Than Usual:", questionnaire.lessSleepThanUsual)
            add_question_answer("More Talkative Than Usual:", questionnaire.moreTalkativeThanUsual)
            add_question_answer("Racing Thoughts:", questionnaire.racingThoughts)
            add_question_answer("Easily Distracted:", questionnaire.easilyDistracted)
            add_question_answer("More Energy Than Usual:", questionnaire.moreEnergyThanUsual)
            add_question_answer("More Active Than Usual:", questionnaire.moreActiveThanUsual)
            add_question_answer("More Social Than Usual:", questionnaire.moreSocialThanUsual)

        elif questionnaire_type.upper() == "BDI":
            add_question_answer("Feelings Of Sadness:", questionnaire.feelingsOfSadness)
            add_question_answer("Thoughts About Future:", questionnaire.thoughtsAboutFuture)
            add_question_answer("Definition Of Success:", questionnaire.definitionOfSuccess)
            add_question_answer("Ability To Experience Pleasure:", questionnaire.abilityToExperiencePleasure)
            add_question_answer("Negative Self Statements:", questionnaire.negativeSelfStatements)
            add_question_answer("Feelings Of Punishment:", questionnaire.feelingsOfPunishment)
            add_question_answer("Disappointments In Self:", questionnaire.disappointmentsInSelf)
            add_question_answer("Handling Self Criticism:", questionnaire.handlingSelfCriticism)
            add_question_answer("Thoughts Of Self Harm:", questionnaire.thoughtsOfSelfHarm)
            add_question_answer("Frequency Of Crying:", questionnaire.frequencyOfCrying)

        elif questionnaire_type.upper() == "NPQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decisions:", questionnaire.avoidIndependentDecisions)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Find It Difficult To Concentrate:", questionnaire.findItDifficultToConcentrate)
            add_question_answer("Frequently Dissatisfied With Self:", questionnaire.frequentlyDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)

        elif questionnaire_type.upper() == "BFT":
            add_question_answer("Talks A Lot:", questionnaire.talksALot)
            add_question_answer("Notices Weak Points:", questionnaire.noticesWeakPoints)
            add_question_answer("Does Things Carefully:", questionnaire.doesThingsCarefully)
            add_question_answer("Is Sad/Depressed:", questionnaire.isSadDepressed)
            add_question_answer("Is Original:", questionnaire.isOriginal)
            add_question_answer("Keeps Thoughts to Themselves:", questionnaire.keepsThoughtsToThemselves)
            add_question_answer("Is Helpful Not Selfish:", questionnaire.isHelpfulNotSelfish)
            add_question_answer("Is Careless:", questionnaire.isCareless)
            add_question_answer("Is Relaxed:", questionnaire.isRelaxed)
            add_question_answer("Is Curious:", questionnaire.isCurious)

        elif questionnaire_type.upper() == "OCIR":
            add_question_answer("Saved Too Many Things:", questionnaire.savedTooManyThings)
            add_question_answer("Check Things More Often:", questionnaire.checkThingsMoreOften)
            add_question_answer("Upset If Not Arranged Properly:", questionnaire.upsetIfNotArrangedProperly)
            add_question_answer("Compelled To Count:", questionnaire.compelledToCount)
            add_question_answer("Difficult To Touch Touched Objects:", questionnaire.difficultToTouchTouchedObjects)
            add_question_answer("Difficult To Control Thoughts:", questionnaire.difficultToControlThoughts)
            add_question_answer("Collect Unnecessary Things:", questionnaire.collectUnnecessaryThings)
            add_question_answer("Repeatedly Check Items:", questionnaire.repeatedlyCheckItems)
            add_question_answer("Upset If Others Change Arrangement:", questionnaire.upsetIfOthersChangeArrangement)
            add_question_answer("Feel Compelled To Repeat Numbers:", questionnaire.feelCompelledToRepeatNumbers)

        elif questionnaire_type.upper() == "MMPI2":
            add_question_answer("Rarely Worry About Health:", questionnaire.rarelyWorryAboutHealth)
            add_question_answer("Always Tell The Truth:", questionnaire.alwaysTellTruth)
            add_question_answer("Feel Tired Most Of The Time:", questionnaire.feelTiredMostOfTheTime)
            add_question_answer("Feel Punished Without Cause:", questionnaire.feelPunishedWithoutCause)
            add_question_answer("Bothered By Upset Stomach:", questionnaire.botheredByUpsetStomach)
            add_question_answer("Get A Lot Of Headaches:", questionnaire.getLotOfHeadaches)
            add_question_answer("Like To Arrange Flowers:", questionnaire.likeToArrangeFlowers)
            add_question_answer("Someone Has It In For Me:", questionnaire.someoneHasItInForMe)
            add_question_answer("Often Disturbing Thoughts:", questionnaire.oftenDisturbingThoughts)
            add_question_answer("Hear Things Others Can't Hear:", questionnaire.hearThingsOthersCantHear)
            add_question_answer("Am Happier Than Most People:", questionnaire.amHappierThanMostPeople)
            add_question_answer("Am Easily Embarrassed:", questionnaire.amEasilyEmbarrassed)

        elif questionnaire_type.upper() == "ENNEAGRAM":
            add_question_answer("Creative Artistic View:", questionnaire.creativeArtisticView)
            add_question_answer("Feel Different From Others:", questionnaire.feelDifferentFromOthers)
            add_question_answer("Experience Melancholy:", questionnaire.experienceMelancholy)
            add_question_answer("Overly Sensitive:", questionnaire.overlySensitive)
            add_question_answer("Feel Something Is Missing:", questionnaire.feelSomethingIsMissing)
            add_question_answer("Feel Envious Of Others:", questionnaire.feelEnviousOfOthers)
            add_question_answer("Thrive In Creative Environments:", questionnaire.thriveInCreativeEnvironments)
            add_question_answer("Become Withdrawn When Misunderstood:", questionnaire.canBecomeWithdrawnWhenMisunderstood)
            add_question_answer("Romantic Longing:", questionnaire.romanticLonging)
            add_question_answer("Caught In Fantasy World:", questionnaire.caughtInFantasyWorld)
            add_question_answer("Enjoy Unique Elegant Things:", questionnaire.enjoyUniqueElegantThings)
            add_question_answer("Moody When Stressed:", questionnaire.moodyWhenStressed)
            add_question_answer("Reflective And Search For Meaning:", questionnaire.reflectiveAndSearchForMeaning)
            add_question_answer("Strive To Be Unique:", questionnaire.striveToBeUnique)
            add_question_answer("Manners And Good Taste:", questionnaire.mannersAndGoodTaste)
            add_question_answer("Seen As Overly Dramatic:", questionnaire.seenAsOverlyDramatic)
            add_question_answer("Important To Understand Feelings:", questionnaire.importantToUnderstandFeelings)

        # Build the PDF
        doc.build(story)

        # Move the buffer's position to the beginning
        buffer.seek(0)

        # Write the buffer to the response
        response.write(buffer.getvalue())
        buffer.close()

        print(f"PDF report generated successfully for user: {user_profile.name}, questionnaire type: {questionnaire_type}")

        return response
    
    def get(self, request, user_id, questionnaire_type):
        date_today = datetime.now().strftime("%B %d, %Y")
        print(f"Received request for report generation. User ID: {user_id}, Questionnaire Type: {questionnaire_type}")

        # Fetch the user's profile by firebase_uid
        try:
            user_profile = UserProfile.objects.get(firebase_uid=user_id)
        except UserProfile.DoesNotExist:
            print(f"UserProfile not found for user_id: {user_id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Mapping of questionnaire types to their respective model classes
        questionnaire_models = {
            "ADHD": ADHD,
            "GAD": GAD,
            "MDQ": MDQ,
            "BDI": BDI,
            "NPQ": NPQ,
            "BFT": BFTQuestionnaire,
            "OCIR": OCIR,
            "MMPI2": MMPI2Questionnaire,
            "ENNEAGRAM": ENNEAGRAM
        }

        # Validate the questionnaire type
        model_class = questionnaire_models.get(questionnaire_type.upper())
        if not model_class:
            print(f"Unsupported questionnaire type: {questionnaire_type}")
            return Response({"error": "Unsupported questionnaire type"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the most recent questionnaire entry by ordering descending by 'id'
        try:
            questionnaire = model_class.objects.filter(user=user_profile).order_by('-id').first()
            if not questionnaire:
                print(f"{questionnaire_type} Questionnaire not found for user: {user_profile.name}")
                return Response({"error": f"{questionnaire_type} Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error fetching {questionnaire_type} Questionnaire: {str(e)}")
            return Response({"error": f"Error fetching {questionnaire_type} Questionnaire"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{questionnaire_type}_Report_{user_id}.pdf"'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=18, spaceAfter=10))
        styles.add(ParagraphStyle(name='SubtitleStyle', fontName='Helvetica-Oblique', fontSize=12, spaceAfter=20))
        styles.add(ParagraphStyle(name='DateStyle', fontName='Helvetica', fontSize=10, spaceAfter=5))
        styles.add(ParagraphStyle(name='SectionTitle', fontName='Helvetica-Bold', fontSize=14, spaceAfter=10))
        styles.add(ParagraphStyle(name='QuestionStyle', fontName='Helvetica-Bold', fontSize=12, spaceAfter=2))
        styles.add(ParagraphStyle(name='AnswerStyle', fontName='Helvetica', fontSize=12, leftIndent=20, spaceAfter=10))

        story = []

        # Header
        story.append(Paragraph("Mental Health Report", styles['TitleStyle']))
        story.append(Paragraph("Therapy is Healing", styles['SubtitleStyle']))

        # Date (Removed 'Created At')
        story.append(Paragraph(f"Date: {date_today}", styles['DateStyle']))
        story.append(Spacer(1, 12))

        # Line Separator
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color='black'))
        story.append(Spacer(1, 12))

        # Section Title
        story.append(Paragraph(f"{questionnaire_type} Questionnaire", styles['SectionTitle']))

        # Helper function to add question and answer
        def add_question_answer(question, answer):
            story.append(Paragraph(question, styles['QuestionStyle']))
            story.append(Paragraph(str(answer), styles['AnswerStyle']))
            story.append(Spacer(1, 6))

        # Add content based on questionnaire type
        if questionnaire_type.upper() == "ADHD":
            add_question_answer("Trouble Wrapping Up Final Details:", questionnaire.troubleWrappingUpFinalDetails)
            add_question_answer("Difficulty Getting Organized:", questionnaire.difficultyGettingOrganized)
            add_question_answer("Problems Remembering Appointments:", questionnaire.problemsRememberingAppointments)
            add_question_answer("Avoid Delaying Thought-Intensive Tasks:", questionnaire.avoidDelayingThoughtIntensiveTasks)
            add_question_answer("Fidget or Squirm When Sitting:", questionnaire.fidgetOrSquirmWhenSitting)
            add_question_answer("Feel Overly Active or Compelled:", questionnaire.feelOverlyActiveCompelled)
            add_question_answer("Make Careless Mistakes:", questionnaire.makeCarelessMistakes)
            add_question_answer("Difficulty Keeping Attention:", questionnaire.difficultyKeepingAttention)
            add_question_answer("Difficulty Concentrating on Direct Speech:", questionnaire.difficultyConcentratingOnDirectSpeech)
            add_question_answer("Misplace or Difficulty Finding Things:", questionnaire.misplaceOrDifficultyFindingThings)

        elif questionnaire_type.upper() == "GAD":
            add_question_answer("Feeling Nervous:", questionnaire.feelingNervous)
            add_question_answer("Inability to Control Worrying:", questionnaire.inabilityToControlWorrying)
            add_question_answer("Excessive Worrying:", questionnaire.excessiveWorrying)
            add_question_answer("Trouble Relaxing:", questionnaire.troubleRelaxing)
            add_question_answer("Restlessness:", questionnaire.restlessness)
            add_question_answer("Irritability:", questionnaire.irritability)
            add_question_answer("Fear of Something Awful:", questionnaire.fearOfSomethingAwful)

        elif questionnaire_type.upper() == "MDQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decision Making:", questionnaire.avoidIndependentDecisionMaking)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Difficulty Concentrating:", questionnaire.difficultyConcentrating)
            add_question_answer("Feel Dissatisfied With Self:", questionnaire.feelDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)
            add_question_answer("Feel Hyper To The Point Of Concern:", questionnaire.feelHyperToThePointOfConcern)
            add_question_answer("Irritability Leading To Conflict:", questionnaire.irritabilityLeadingToConflict)
            add_question_answer("Increased Self Confidence:", questionnaire.increasedSelfConfidence)
            add_question_answer("Less Sleep Than Usual:", questionnaire.lessSleepThanUsual)
            add_question_answer("More Talkative Than Usual:", questionnaire.moreTalkativeThanUsual)
            add_question_answer("Racing Thoughts:", questionnaire.racingThoughts)
            add_question_answer("Easily Distracted:", questionnaire.easilyDistracted)
            add_question_answer("More Energy Than Usual:", questionnaire.moreEnergyThanUsual)
            add_question_answer("More Active Than Usual:", questionnaire.moreActiveThanUsual)
            add_question_answer("More Social Than Usual:", questionnaire.moreSocialThanUsual)

        elif questionnaire_type.upper() == "BDI":
            add_question_answer("Feelings Of Sadness:", questionnaire.feelingsOfSadness)
            add_question_answer("Thoughts About Future:", questionnaire.thoughtsAboutFuture)
            add_question_answer("Definition Of Success:", questionnaire.definitionOfSuccess)
            add_question_answer("Ability To Experience Pleasure:", questionnaire.abilityToExperiencePleasure)
            add_question_answer("Negative Self Statements:", questionnaire.negativeSelfStatements)
            add_question_answer("Feelings Of Punishment:", questionnaire.feelingsOfPunishment)
            add_question_answer("Disappointments In Self:", questionnaire.disappointmentsInSelf)
            add_question_answer("Handling Self Criticism:", questionnaire.handlingSelfCriticism)
            add_question_answer("Thoughts Of Self Harm:", questionnaire.thoughtsOfSelfHarm)
            add_question_answer("Frequency Of Crying:", questionnaire.frequencyOfCrying)

        elif questionnaire_type.upper() == "NPQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decisions:", questionnaire.avoidIndependentDecisions)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Find It Difficult To Concentrate:", questionnaire.findItDifficultToConcentrate)
            add_question_answer("Frequently Dissatisfied With Self:", questionnaire.frequentlyDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)

        elif questionnaire_type.upper() == "BFT":
            add_question_answer("Talks A Lot:", questionnaire.talksALot)
            add_question_answer("Notices Weak Points:", questionnaire.noticesWeakPoints)
            add_question_answer("Does Things Carefully:", questionnaire.doesThingsCarefully)
            add_question_answer("Is Sad/Depressed:", questionnaire.isSadDepressed)
            add_question_answer("Is Original:", questionnaire.isOriginal)
            add_question_answer("Keeps Thoughts to Themselves:", questionnaire.keepsThoughtsToThemselves)
            add_question_answer("Is Helpful Not Selfish:", questionnaire.isHelpfulNotSelfish)
            add_question_answer("Is Careless:", questionnaire.isCareless)
            add_question_answer("Is Relaxed:", questionnaire.isRelaxed)
            add_question_answer("Is Curious:", questionnaire.isCurious)

        elif questionnaire_type.upper() == "OCIR":
            add_question_answer("Saved Too Many Things:", questionnaire.savedTooManyThings)
            add_question_answer("Check Things More Often:", questionnaire.checkThingsMoreOften)
            add_question_answer("Upset If Not Arranged Properly:", questionnaire.upsetIfNotArrangedProperly)
            add_question_answer("Compelled To Count:", questionnaire.compelledToCount)
            add_question_answer("Difficult To Touch Touched Objects:", questionnaire.difficultToTouchTouchedObjects)
            add_question_answer("Difficult To Control Thoughts:", questionnaire.difficultToControlThoughts)
            add_question_answer("Collect Unnecessary Things:", questionnaire.collectUnnecessaryThings)
            add_question_answer("Repeatedly Check Items:", questionnaire.repeatedlyCheckItems)
            add_question_answer("Upset If Others Change Arrangement:", questionnaire.upsetIfOthersChangeArrangement)
            add_question_answer("Feel Compelled To Repeat Numbers:", questionnaire.feelCompelledToRepeatNumbers)

        elif questionnaire_type.upper() == "MMPI2":
            add_question_answer("Rarely Worry About Health:", questionnaire.rarelyWorryAboutHealth)
            add_question_answer("Always Tell The Truth:", questionnaire.alwaysTellTruth)
            add_question_answer("Feel Tired Most Of The Time:", questionnaire.feelTiredMostOfTheTime)
            add_question_answer("Feel Punished Without Cause:", questionnaire.feelPunishedWithoutCause)
            add_question_answer("Bothered By Upset Stomach:", questionnaire.botheredByUpsetStomach)
            add_question_answer("Get A Lot Of Headaches:", questionnaire.getLotOfHeadaches)
            add_question_answer("Like To Arrange Flowers:", questionnaire.likeToArrangeFlowers)
            add_question_answer("Someone Has It In For Me:", questionnaire.someoneHasItInForMe)
            add_question_answer("Often Disturbing Thoughts:", questionnaire.oftenDisturbingThoughts)
            add_question_answer("Hear Things Others Can't Hear:", questionnaire.hearThingsOthersCantHear)
            add_question_answer("Am Happier Than Most People:", questionnaire.amHappierThanMostPeople)
            add_question_answer("Am Easily Embarrassed:", questionnaire.amEasilyEmbarrassed)

        elif questionnaire_type.upper() == "ENNEAGRAM":
            add_question_answer("Creative Artistic View:", questionnaire.creativeArtisticView)
            add_question_answer("Feel Different From Others:", questionnaire.feelDifferentFromOthers)
            add_question_answer("Experience Melancholy:", questionnaire.experienceMelancholy)
            add_question_answer("Overly Sensitive:", questionnaire.overlySensitive)
            add_question_answer("Feel Something Is Missing:", questionnaire.feelSomethingIsMissing)
            add_question_answer("Feel Envious Of Others:", questionnaire.feelEnviousOfOthers)
            add_question_answer("Thrive In Creative Environments:", questionnaire.thriveInCreativeEnvironments)
            add_question_answer("Become Withdrawn When Misunderstood:", questionnaire.canBecomeWithdrawnWhenMisunderstood)
            add_question_answer("Romantic Longing:", questionnaire.romanticLonging)
            add_question_answer("Caught In Fantasy World:", questionnaire.caughtInFantasyWorld)
            add_question_answer("Enjoy Unique Elegant Things:", questionnaire.enjoyUniqueElegantThings)
            add_question_answer("Moody When Stressed:", questionnaire.moodyWhenStressed)
            add_question_answer("Reflective And Search For Meaning:", questionnaire.reflectiveAndSearchForMeaning)
            add_question_answer("Strive To Be Unique:", questionnaire.striveToBeUnique)
            add_question_answer("Manners And Good Taste:", questionnaire.mannersAndGoodTaste)
            add_question_answer("Seen As Overly Dramatic:", questionnaire.seenAsOverlyDramatic)
            add_question_answer("Important To Understand Feelings:", questionnaire.importantToUnderstandFeelings)

        # Build the PDF
        doc.build(story)

        # Move the buffer's position to the beginning
        buffer.seek(0)

        # Write the buffer to the response
        response.write(buffer.getvalue())
        buffer.close()

        print(f"PDF report generated successfully for user: {user_profile.name}, questionnaire type: {questionnaire_type}")

        return response
    
    def get(self, request, user_id, questionnaire_type):
        date_today = datetime.now().strftime("%B %d, %Y")
        print(f"Received request for report generation. User ID: {user_id}, Questionnaire Type: {questionnaire_type}")

        # Fetch the user's profile by firebase_uid
        try:
            user_profile = UserProfile.objects.get(firebase_uid=user_id)
        except UserProfile.DoesNotExist:
            print(f"UserProfile not found for user_id: {user_id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the corresponding questionnaire data based on the questionnaire_type
        questionnaire = None
        try:
            if questionnaire_type == "ADHD":
                questionnaire = ADHD.objects.filter(user=user_profile).first()
            elif questionnaire_type == "GAD":
                questionnaire = GAD.objects.filter(user=user_profile).first()
            elif questionnaire_type == "MDQ":
                questionnaire = MDQ.objects.filter(user=user_profile).first()
            elif questionnaire_type == "BDI":
                questionnaire = BDI.objects.filter(user=user_profile).first()
            elif questionnaire_type == "NPQ":
                questionnaire = NPQ.objects.filter(user=user_profile).first()
            elif questionnaire_type == "BFT":
                questionnaire = BFTQuestionnaire.objects.filter(user=user_profile).first()
            elif questionnaire_type == "OCIR":
                questionnaire = OCIR.objects.filter(user=user_profile).first()
            elif questionnaire_type == "MMPI2":
                questionnaire = MMPI2Questionnaire.objects.filter(user=user_profile).first()
            elif questionnaire_type == "ENNEAGRAM":
                questionnaire = ENNEAGRAM.objects.filter(user=user_profile).first()
            else:
                print(f"Unsupported questionnaire type: {questionnaire_type}")
                return Response({"error": "Unsupported questionnaire type"}, status=status.HTTP_400_BAD_REQUEST)

            if not questionnaire:
                print(f"{questionnaire_type} Questionnaire not found for user: {user_profile.name}")
                return Response({"error": f"{questionnaire_type} Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"Error fetching {questionnaire_type} Questionnaire: {str(e)}")
            return Response({"error": f"Error fetching {questionnaire_type} Questionnaire"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{questionnaire_type}_Report_{user_id}.pdf"'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=18, spaceAfter=10))
        styles.add(ParagraphStyle(name='SubtitleStyle', fontName='Helvetica-Oblique', fontSize=12, spaceAfter=20))
        styles.add(ParagraphStyle(name='DateStyle', fontName='Helvetica', fontSize=10, spaceAfter=5))
        styles.add(ParagraphStyle(name='SectionTitle', fontName='Helvetica-Bold', fontSize=14, spaceAfter=10))
        styles.add(ParagraphStyle(name='QuestionStyle', fontName='Helvetica-Bold', fontSize=12, spaceAfter=2))
        styles.add(ParagraphStyle(name='AnswerStyle', fontName='Helvetica', fontSize=12, leftIndent=20, spaceAfter=10))

        story = []

        # Header
        story.append(Paragraph("Mental Health Report", styles['TitleStyle']))
        story.append(Paragraph("Therapy is Healing", styles['SubtitleStyle']))

        # Date (Removed 'Created At')
        story.append(Paragraph(f"Date: {date_today}", styles['DateStyle']))
        story.append(Spacer(1, 12))

        # Line Separator
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color='black'))
        story.append(Spacer(1, 12))

        # Section Title
        story.append(Paragraph(f"{questionnaire_type} Questionnaire", styles['SectionTitle']))

        # Helper function to add question and answer
        def add_question_answer(question, answer):
            story.append(Paragraph(question, styles['QuestionStyle']))
            story.append(Paragraph(str(answer), styles['AnswerStyle']))
            story.append(Spacer(1, 6))

        # Add content based on questionnaire type
        if questionnaire_type == "ADHD":
            add_question_answer("Trouble Wrapping Up Final Details:", questionnaire.troubleWrappingUpFinalDetails)
            add_question_answer("Difficulty Getting Organized:", questionnaire.difficultyGettingOrganized)
            add_question_answer("Problems Remembering Appointments:", questionnaire.problemsRememberingAppointments)
            add_question_answer("Avoid Delaying Thought-Intensive Tasks:", questionnaire.avoidDelayingThoughtIntensiveTasks)
            add_question_answer("Fidget or Squirm When Sitting:", questionnaire.fidgetOrSquirmWhenSitting)
            add_question_answer("Feel Overly Active or Compelled:", questionnaire.feelOverlyActiveCompelled)
            add_question_answer("Make Careless Mistakes:", questionnaire.makeCarelessMistakes)
            add_question_answer("Difficulty Keeping Attention:", questionnaire.difficultyKeepingAttention)
            add_question_answer("Difficulty Concentrating on Direct Speech:", questionnaire.difficultyConcentratingOnDirectSpeech)
            add_question_answer("Misplace or Difficulty Finding Things:", questionnaire.misplaceOrDifficultyFindingThings)

        elif questionnaire_type == "GAD":
            add_question_answer("Feeling Nervous:", questionnaire.feelingNervous)
            add_question_answer("Inability to Control Worrying:", questionnaire.inabilityToControlWorrying)
            add_question_answer("Excessive Worrying:", questionnaire.excessiveWorrying)
            add_question_answer("Trouble Relaxing:", questionnaire.troubleRelaxing)
            add_question_answer("Restlessness:", questionnaire.restlessness)
            add_question_answer("Irritability:", questionnaire.irritability)
            add_question_answer("Fear of Something Awful:", questionnaire.fearOfSomethingAwful)

        elif questionnaire_type == "MDQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decision Making:", questionnaire.avoidIndependentDecisionMaking)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Difficulty Concentrating:", questionnaire.difficultyConcentrating)
            add_question_answer("Feel Dissatisfied With Self:", questionnaire.feelDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)
            add_question_answer("Feel Hyper To The Point Of Concern:", questionnaire.feelHyperToThePointOfConcern)
            add_question_answer("Irritability Leading To Conflict:", questionnaire.irritabilityLeadingToConflict)
            add_question_answer("Increased Self Confidence:", questionnaire.increasedSelfConfidence)
            add_question_answer("Less Sleep Than Usual:", questionnaire.lessSleepThanUsual)
            add_question_answer("More Talkative Than Usual:", questionnaire.moreTalkativeThanUsual)
            add_question_answer("Racing Thoughts:", questionnaire.racingThoughts)
            add_question_answer("Easily Distracted:", questionnaire.easilyDistracted)
            add_question_answer("More Energy Than Usual:", questionnaire.moreEnergyThanUsual)
            add_question_answer("More Active Than Usual:", questionnaire.moreActiveThanUsual)
            add_question_answer("More Social Than Usual:", questionnaire.moreSocialThanUsual)

        elif questionnaire_type == "BDI":
            add_question_answer("Feelings Of Sadness:", questionnaire.feelingsOfSadness)
            add_question_answer("Thoughts About Future:", questionnaire.thoughtsAboutFuture)
            add_question_answer("Definition Of Success:", questionnaire.definitionOfSuccess)
            add_question_answer("Ability To Experience Pleasure:", questionnaire.abilityToExperiencePleasure)
            add_question_answer("Negative Self Statements:", questionnaire.negativeSelfStatements)
            add_question_answer("Feelings Of Punishment:", questionnaire.feelingsOfPunishment)
            add_question_answer("Disappointments In Self:", questionnaire.disappointmentsInSelf)
            add_question_answer("Handling Self Criticism:", questionnaire.handlingSelfCriticism)
            add_question_answer("Thoughts Of Self Harm:", questionnaire.thoughtsOfSelfHarm)
            add_question_answer("Frequency Of Crying:", questionnaire.frequencyOfCrying)

        elif questionnaire_type == "NPQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decisions:", questionnaire.avoidIndependentDecisions)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Find It Difficult To Concentrate:", questionnaire.findItDifficultToConcentrate)
            add_question_answer("Frequently Dissatisfied With Self:", questionnaire.frequentlyDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)

        elif questionnaire_type == "BFT":
            add_question_answer("Talks A Lot:", questionnaire.talksALot)
            add_question_answer("Notices Weak Points:", questionnaire.noticesWeakPoints)
            add_question_answer("Does Things Carefully:", questionnaire.doesThingsCarefully)
            add_question_answer("Is Sad/Depressed:", questionnaire.isSadDepressed)
            add_question_answer("Is Original:", questionnaire.isOriginal)
            add_question_answer("Keeps Thoughts to Themselves:", questionnaire.keepsThoughtsToThemselves)
            add_question_answer("Is Helpful Not Selfish:", questionnaire.isHelpfulNotSelfish)
            add_question_answer("Is Careless:", questionnaire.isCareless)
            add_question_answer("Is Relaxed:", questionnaire.isRelaxed)
            add_question_answer("Is Curious:", questionnaire.isCurious)

        elif questionnaire_type == "OCIR":
            add_question_answer("Saved Too Many Things:", questionnaire.savedTooManyThings)
            add_question_answer("Check Things More Often:", questionnaire.checkThingsMoreOften)
            add_question_answer("Upset If Not Arranged Properly:", questionnaire.upsetIfNotArrangedProperly)
            add_question_answer("Compelled To Count:", questionnaire.compelledToCount)
            add_question_answer("Difficult To Touch Touched Objects:", questionnaire.difficultToTouchTouchedObjects)
            add_question_answer("Difficult To Control Thoughts:", questionnaire.difficultToControlThoughts)
            add_question_answer("Collect Unnecessary Things:", questionnaire.collectUnnecessaryThings)
            add_question_answer("Repeatedly Check Items:", questionnaire.repeatedlyCheckItems)
            add_question_answer("Upset If Others Change Arrangement:", questionnaire.upsetIfOthersChangeArrangement)
            add_question_answer("Feel Compelled To Repeat Numbers:", questionnaire.feelCompelledToRepeatNumbers)

        elif questionnaire_type == "MMPI2":
            add_question_answer("Rarely Worry About Health:", questionnaire.rarelyWorryAboutHealth)
            add_question_answer("Always Tell The Truth:", questionnaire.alwaysTellTruth)
            add_question_answer("Feel Tired Most Of The Time:", questionnaire.feelTiredMostOfTheTime)
            add_question_answer("Feel Punished Without Cause:", questionnaire.feelPunishedWithoutCause)
            add_question_answer("Bothered By Upset Stomach:", questionnaire.botheredByUpsetStomach)
            add_question_answer("Get A Lot Of Headaches:", questionnaire.getLotOfHeadaches)
            add_question_answer("Like To Arrange Flowers:", questionnaire.likeToArrangeFlowers)
            add_question_answer("Someone Has It In For Me:", questionnaire.someoneHasItInForMe)
            add_question_answer("Often Disturbing Thoughts:", questionnaire.oftenDisturbingThoughts)
            add_question_answer("Hear Things Others Can't Hear:", questionnaire.hearThingsOthersCantHear)
            add_question_answer("Am Happier Than Most People:", questionnaire.amHappierThanMostPeople)
            add_question_answer("Am Easily Embarrassed:", questionnaire.amEasilyEmbarrassed)

        elif questionnaire_type == "ENNEAGRAM":
            add_question_answer("Creative Artistic View:", questionnaire.creativeArtisticView)
            add_question_answer("Feel Different From Others:", questionnaire.feelDifferentFromOthers)
            add_question_answer("Experience Melancholy:", questionnaire.experienceMelancholy)
            add_question_answer("Overly Sensitive:", questionnaire.overlySensitive)
            add_question_answer("Feel Something Is Missing:", questionnaire.feelSomethingIsMissing)
            add_question_answer("Feel Envious Of Others:", questionnaire.feelEnviousOfOthers)
            add_question_answer("Thrive In Creative Environments:", questionnaire.thriveInCreativeEnvironments)
            add_question_answer("Become Withdrawn When Misunderstood:", questionnaire.canBecomeWithdrawnWhenMisunderstood)
            add_question_answer("Romantic Longing:", questionnaire.romanticLonging)
            add_question_answer("Caught In Fantasy World:", questionnaire.caughtInFantasyWorld)
            add_question_answer("Enjoy Unique Elegant Things:", questionnaire.enjoyUniqueElegantThings)
            add_question_answer("Moody When Stressed:", questionnaire.moodyWhenStressed)
            add_question_answer("Reflective And Search For Meaning:", questionnaire.reflectiveAndSearchForMeaning)
            add_question_answer("Strive To Be Unique:", questionnaire.striveToBeUnique)
            add_question_answer("Manners And Good Taste:", questionnaire.mannersAndGoodTaste)
            add_question_answer("Seen As Overly Dramatic:", questionnaire.seenAsOverlyDramatic)
            add_question_answer("Important To Understand Feelings:", questionnaire.importantToUnderstandFeelings)

        # Build the PDF
        doc.build(story)

        # Move the buffer's position to the beginning
        buffer.seek(0)

        # Write the buffer to the response
        response.write(buffer.getvalue())
        buffer.close()

        print(f"PDF report generated successfully for user: {user_profile.name}, questionnaire type: {questionnaire_type}")

        return response
    
    def get(self, request, user_id, questionnaire_type):
        date_today = datetime.now().strftime("%B %d, %Y")
        print(f"Received request for report generation. User ID: {user_id}, Questionnaire Type: {questionnaire_type}")

        # Fetch the user's profile by firebase_uid
        try:
            user_profile = UserProfile.objects.get(firebase_uid=user_id)
        except UserProfile.DoesNotExist:
            print(f"UserProfile not found for user_id: {user_id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the corresponding questionnaire data based on the questionnaire_type
        questionnaire = None
        try:
            if questionnaire_type == "ADHD":
                questionnaire = ADHD.objects.filter(user=user_profile).first()
            elif questionnaire_type == "GAD":
                questionnaire = GAD.objects.filter(user=user_profile).first()
            elif questionnaire_type == "MDQ":
                questionnaire = MDQ.objects.filter(user=user_profile).first()
            elif questionnaire_type == "BDI":
                questionnaire = BDI.objects.filter(user=user_profile).first()
            elif questionnaire_type == "NPQ":
                questionnaire = NPQ.objects.filter(user=user_profile).first()
            elif questionnaire_type == "BFT":
                questionnaire = BFTQuestionnaire.objects.filter(user=user_profile).first()
            elif questionnaire_type == "OCIR":
                questionnaire = OCIR.objects.filter(user=user_profile).first()
            elif questionnaire_type == "MMPI2":
                questionnaire = MMPI2Questionnaire.objects.filter(user=user_profile).first()
            elif questionnaire_type == "ENNEAGRAM":
                questionnaire = ENNEAGRAM.objects.filter(user=user_profile).first()
            else:
                print(f"Unsupported questionnaire type: {questionnaire_type}")
                return Response({"error": "Unsupported questionnaire type"}, status=status.HTTP_400_BAD_REQUEST)

            if not questionnaire:
                print(f"{questionnaire_type} Questionnaire not found for user: {user_profile.name}")
                return Response({"error": f"{questionnaire_type} Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"Error fetching {questionnaire_type} Questionnaire: {str(e)}")
            return Response({"error": f"Error fetching {questionnaire_type} Questionnaire"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{questionnaire_type}_Report_{user_id}.pdf"'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=18, spaceAfter=10))
        styles.add(ParagraphStyle(name='SubtitleStyle', fontName='Helvetica-Oblique', fontSize=12, spaceAfter=20))
        styles.add(ParagraphStyle(name='DateStyle', fontName='Helvetica', fontSize=10, spaceAfter=5))
        styles.add(ParagraphStyle(name='SectionTitle', fontName='Helvetica-Bold', fontSize=14, spaceAfter=10))
        styles.add(ParagraphStyle(name='QuestionStyle', fontName='Helvetica-Bold', fontSize=12, spaceAfter=2))
        styles.add(ParagraphStyle(name='AnswerStyle', fontName='Helvetica', fontSize=12, leftIndent=20, spaceAfter=10))

        story = []

        # Header
        story.append(Paragraph("Mental Health Report", styles['TitleStyle']))
        story.append(Paragraph("Therapy is Healing", styles['SubtitleStyle']))

        # Date and Created At (if available)
        story.append(Paragraph(f"Date: {date_today}", styles['DateStyle']))
        # if hasattr(questionnaire, 'created_at') and questionnaire.created_at:
        #     story.append(Paragraph(f"Created At: {questionnaire.created_at.strftime('%B %d, %Y')}", styles['DateStyle']))
        # else:
        #     story.append(Paragraph("Created At: N/A", styles['DateStyle']))
        story.append(Spacer(1, 12))

        # Line Separator
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color='black'))
        story.append(Spacer(1, 12))

        # Section Title
        story.append(Paragraph(f"{questionnaire_type} Questionnaire", styles['SectionTitle']))

        # Helper function to add question and answer
        def add_question_answer(question, answer):
            story.append(Paragraph(question, styles['QuestionStyle']))
            story.append(Paragraph(str(answer), styles['AnswerStyle']))
            story.append(Spacer(1, 6))

        # Add content based on questionnaire type
        if questionnaire_type == "ADHD":
            add_question_answer("Trouble Wrapping Up Final Details:", questionnaire.troubleWrappingUpFinalDetails)
            add_question_answer("Difficulty Getting Organized:", questionnaire.difficultyGettingOrganized)
            add_question_answer("Problems Remembering Appointments:", questionnaire.problemsRememberingAppointments)
            add_question_answer("Avoid Delaying Thought-Intensive Tasks:", questionnaire.avoidDelayingThoughtIntensiveTasks)
            add_question_answer("Fidget or Squirm When Sitting:", questionnaire.fidgetOrSquirmWhenSitting)
            add_question_answer("Feel Overly Active or Compelled:", questionnaire.feelOverlyActiveCompelled)
            add_question_answer("Make Careless Mistakes:", questionnaire.makeCarelessMistakes)
            add_question_answer("Difficulty Keeping Attention:", questionnaire.difficultyKeepingAttention)
            add_question_answer("Difficulty Concentrating on Direct Speech:", questionnaire.difficultyConcentratingOnDirectSpeech)
            add_question_answer("Misplace or Difficulty Finding Things:", questionnaire.misplaceOrDifficultyFindingThings)

        elif questionnaire_type == "GAD":
            add_question_answer("Feeling Nervous:", questionnaire.feelingNervous)
            add_question_answer("Inability to Control Worrying:", questionnaire.inabilityToControlWorrying)
            add_question_answer("Excessive Worrying:", questionnaire.excessiveWorrying)
            add_question_answer("Trouble Relaxing:", questionnaire.troubleRelaxing)
            add_question_answer("Restlessness:", questionnaire.restlessness)
            add_question_answer("Irritability:", questionnaire.irritability)
            add_question_answer("Fear of Something Awful:", questionnaire.fearOfSomethingAwful)

        elif questionnaire_type == "MDQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decision Making:", questionnaire.avoidIndependentDecisionMaking)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Difficulty Concentrating:", questionnaire.difficultyConcentrating)
            add_question_answer("Feel Dissatisfied With Self:", questionnaire.feelDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)
            add_question_answer("Feel Hyper To The Point Of Concern:", questionnaire.feelHyperToThePointOfConcern)
            add_question_answer("Irritability Leading To Conflict:", questionnaire.irritabilityLeadingToConflict)
            add_question_answer("Increased Self Confidence:", questionnaire.increasedSelfConfidence)
            add_question_answer("Less Sleep Than Usual:", questionnaire.lessSleepThanUsual)
            add_question_answer("More Talkative Than Usual:", questionnaire.moreTalkativeThanUsual)
            add_question_answer("Racing Thoughts:", questionnaire.racingThoughts)
            add_question_answer("Easily Distracted:", questionnaire.easilyDistracted)
            add_question_answer("More Energy Than Usual:", questionnaire.moreEnergyThanUsual)
            add_question_answer("More Active Than Usual:", questionnaire.moreActiveThanUsual)
            add_question_answer("More Social Than Usual:", questionnaire.moreSocialThanUsual)

        elif questionnaire_type == "BDI":
            add_question_answer("Feelings Of Sadness:", questionnaire.feelingsOfSadness)
            add_question_answer("Thoughts About Future:", questionnaire.thoughtsAboutFuture)
            add_question_answer("Definition Of Success:", questionnaire.definitionOfSuccess)
            add_question_answer("Ability To Experience Pleasure:", questionnaire.abilityToExperiencePleasure)
            add_question_answer("Negative Self Statements:", questionnaire.negativeSelfStatements)
            add_question_answer("Feelings Of Punishment:", questionnaire.feelingsOfPunishment)
            add_question_answer("Disappointments In Self:", questionnaire.disappointmentsInSelf)
            add_question_answer("Handling Self Criticism:", questionnaire.handlingSelfCriticism)
            add_question_answer("Thoughts Of Self Harm:", questionnaire.thoughtsOfSelfHarm)
            add_question_answer("Frequency Of Crying:", questionnaire.frequencyOfCrying)

        elif questionnaire_type == "NPQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decisions:", questionnaire.avoidIndependentDecisions)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Find It Difficult To Concentrate:", questionnaire.findItDifficultToConcentrate)
            add_question_answer("Frequently Dissatisfied With Self:", questionnaire.frequentlyDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)

        elif questionnaire_type == "BFT":
            add_question_answer("Talks A Lot:", questionnaire.talksALot)
            add_question_answer("Notices Weak Points:", questionnaire.noticesWeakPoints)
            add_question_answer("Does Things Carefully:", questionnaire.doesThingsCarefully)
            add_question_answer("Is Sad/Depressed:", questionnaire.isSadDepressed)
            add_question_answer("Is Original:", questionnaire.isOriginal)
            add_question_answer("Keeps Thoughts to Themselves:", questionnaire.keepsThoughtsToThemselves)
            add_question_answer("Is Helpful Not Selfish:", questionnaire.isHelpfulNotSelfish)
            add_question_answer("Is Careless:", questionnaire.isCareless)
            add_question_answer("Is Relaxed:", questionnaire.isRelaxed)
            add_question_answer("Is Curious:", questionnaire.isCurious)

        elif questionnaire_type == "OCIR":
            add_question_answer("Saved Too Many Things:", questionnaire.savedTooManyThings)
            add_question_answer("Check Things More Often:", questionnaire.checkThingsMoreOften)
            add_question_answer("Upset If Not Arranged Properly:", questionnaire.upsetIfNotArrangedProperly)
            add_question_answer("Compelled To Count:", questionnaire.compelledToCount)
            add_question_answer("Difficult To Touch Touched Objects:", questionnaire.difficultToTouchTouchedObjects)
            add_question_answer("Difficult To Control Thoughts:", questionnaire.difficultToControlThoughts)
            add_question_answer("Collect Unnecessary Things:", questionnaire.collectUnnecessaryThings)
            add_question_answer("Repeatedly Check Items:", questionnaire.repeatedlyCheckItems)
            add_question_answer("Upset If Others Change Arrangement:", questionnaire.upsetIfOthersChangeArrangement)
            add_question_answer("Feel Compelled To Repeat Numbers:", questionnaire.feelCompelledToRepeatNumbers)

        elif questionnaire_type == "MMPI2":
            add_question_answer("Rarely Worry About Health:", questionnaire.rarelyWorryAboutHealth)
            add_question_answer("Always Tell The Truth:", questionnaire.alwaysTellTruth)
            add_question_answer("Feel Tired Most Of The Time:", questionnaire.feelTiredMostOfTheTime)
            add_question_answer("Feel Punished Without Cause:", questionnaire.feelPunishedWithoutCause)
            add_question_answer("Bothered By Upset Stomach:", questionnaire.botheredByUpsetStomach)
            add_question_answer("Get A Lot Of Headaches:", questionnaire.getLotOfHeadaches)
            add_question_answer("Like To Arrange Flowers:", questionnaire.likeToArrangeFlowers)
            add_question_answer("Someone Has It In For Me:", questionnaire.someoneHasItInForMe)
            add_question_answer("Often Disturbing Thoughts:", questionnaire.oftenDisturbingThoughts)
            add_question_answer("Hear Things Others Can't Hear:", questionnaire.hearThingsOthersCantHear)
            add_question_answer("Am Happier Than Most People:", questionnaire.amHappierThanMostPeople)
            add_question_answer("Am Easily Embarrassed:", questionnaire.amEasilyEmbarrassed)

        elif questionnaire_type == "ENNEAGRAM":
            add_question_answer("Creative Artistic View:", questionnaire.creativeArtisticView)
            add_question_answer("Feel Different From Others:", questionnaire.feelDifferentFromOthers)
            add_question_answer("Experience Melancholy:", questionnaire.experienceMelancholy)
            add_question_answer("Overly Sensitive:", questionnaire.overlySensitive)
            add_question_answer("Feel Something Is Missing:", questionnaire.feelSomethingIsMissing)
            add_question_answer("Feel Envious Of Others:", questionnaire.feelEnviousOfOthers)
            add_question_answer("Thrive In Creative Environments:", questionnaire.thriveInCreativeEnvironments)
            add_question_answer("Become Withdrawn When Misunderstood:", questionnaire.canBecomeWithdrawnWhenMisunderstood)
            add_question_answer("Romantic Longing:", questionnaire.romanticLonging)
            add_question_answer("Caught In Fantasy World:", questionnaire.caughtInFantasyWorld)
            add_question_answer("Enjoy Unique Elegant Things:", questionnaire.enjoyUniqueElegantThings)
            add_question_answer("Moody When Stressed:", questionnaire.moodyWhenStressed)
            add_question_answer("Reflective And Search For Meaning:", questionnaire.reflectiveAndSearchForMeaning)
            add_question_answer("Strive To Be Unique:", questionnaire.striveToBeUnique)
            add_question_answer("Manners And Good Taste:", questionnaire.mannersAndGoodTaste)
            add_question_answer("Seen As Overly Dramatic:", questionnaire.seenAsOverlyDramatic)
            add_question_answer("Important To Understand Feelings:", questionnaire.importantToUnderstandFeelings)

        # Build the PDF
        doc.build(story)

        # Move the buffer's position to the beginning
        buffer.seek(0)

        # Write the buffer to the response
        response.write(buffer.getvalue())
        buffer.close()

        print(f"PDF report generated successfully for user: {user_profile.name}, questionnaire type: {questionnaire_type}")

        return response
    def get(self, request, user_id, questionnaire_type):
        date_today = datetime.now().strftime("%B %d, %Y")
        print(f"Received request for report generation. User ID: {user_id}, Questionnaire Type: {questionnaire_type}")

        try:
            user_profile = UserProfile.objects.get(firebase_uid=user_id)
        except UserProfile.DoesNotExist:
            print(f"UserProfile not found for user_id: {user_id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

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

        elif questionnaire_type == "NPQ":
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
                else:
                    print(f"BFT Questionnaire data >>: {questionnaire}")
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

        elif questionnaire_type == "MMPI2":
            try:
                questionnaire = MMPI2Questionnaire.objects.filter(user=user_profile).first()
                if not questionnaire:
                    print(f"MMPI2 Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "MMPI2 Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    print(f"MMPI2 Questionnaire data: {questionnaire}")
            except MMPI2Questionnaire.DoesNotExist:
                print(f"MMPI2 Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "MMPI2 Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)

        elif questionnaire_type == "ENNEAGRAM":
            try:
                questionnaire = ENNEAGRAM.objects.filter(user=user_profile).first()
                if not questionnaire:
                    print(f"ENNEAGRAM Questionnaire not found for user: {user_profile.name}")
                    return Response({"error": "ENNEAGRAM Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)
            except ENNEAGRAM.DoesNotExist:
                print(f"ENNEAGRAM Questionnaire not found for user: {user_profile.name}")
                return Response({"error": "ENNEAGRAM Questionnaire not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            print(f"Unsupported questionnaire type: {questionnaire_type}")
            return Response({"error": "Unsupported questionnaire type"}, status=status.HTTP_400_BAD_REQUEST)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{questionnaire_type}_Report_{user_id}.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Question', fontName='Helvetica-Bold', fontSize=12, spaceAfter=4))
        styles.add(ParagraphStyle(name='Answer', fontName='Helvetica', fontSize=12, leftIndent=20, spaceAfter=10))

        # Create a PDF document using Platypus for better text handling
        from reportlab.platypus import SimpleDocTemplate, Spacer, Frame

        # Re-initialize the PDF with Platypus
        from io import BytesIO
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=72)

        story = []

        # Header
        header_title = Paragraph("Mental Health Report", styles['Title'])
        header_subtitle = Paragraph("Therapy is Healing", styles['Italic'])

        story.append(header_title)
        story.append(header_subtitle)
        story.append(Spacer(1, 12))

        # Date and Created At
        date_paragraph = Paragraph(f"Date: {date_today}", styles['Normal'])
        # created_at_paragraph = Paragraph(f"Created At: {questionnaire.created_at.strftime('%B %d, %Y')}", styles['Normal'])
        story.append(date_paragraph)
        # story.append(created_at_paragraph)
        story.append(Spacer(1, 12))

        # Line Separator
        from reportlab.platypus import HRFlowable
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color='black'))
        story.append(Spacer(1, 12))

        # Section Title
        section_title = Paragraph(f"{questionnaire_type} Questionnaire", styles['Heading2'])
        story.append(section_title)
        story.append(Spacer(1, 12))

        # Helper function to add question and answer
        def add_question_answer(question, answer):
            story.append(Paragraph(question, styles['Question']))
            story.append(Paragraph(str(answer), styles['Answer']))
            story.append(Spacer(1, 6))

        # Add content based on questionnaire type
        if questionnaire_type == "ADHD":
            add_question_answer("Trouble Wrapping Up Final Details:", questionnaire.troubleWrappingUpFinalDetails)
            add_question_answer("Difficulty Getting Organized:", questionnaire.difficultyGettingOrganized)
            add_question_answer("Problems Remembering Appointments:", questionnaire.problemsRememberingAppointments)
            add_question_answer("Avoid Delaying Thought-Intensive Tasks:", questionnaire.avoidDelayingThoughtIntensiveTasks)
            add_question_answer("Fidget or Squirm When Sitting:", questionnaire.fidgetOrSquirmWhenSitting)
            add_question_answer("Feel Overly Active or Compelled:", questionnaire.feelOverlyActiveCompelled)
            add_question_answer("Make Careless Mistakes:", questionnaire.makeCarelessMistakes)
            add_question_answer("Difficulty Keeping Attention:", questionnaire.difficultyKeepingAttention)
            add_question_answer("Difficulty Concentrating on Direct Speech:", questionnaire.difficultyConcentratingOnDirectSpeech)
            add_question_answer("Misplace or Difficulty Finding Things:", questionnaire.misplaceOrDifficultyFindingThings)

        elif questionnaire_type == "GAD":
            add_question_answer("Feeling Nervous:", questionnaire.feelingNervous)
            add_question_answer("Inability to Control Worrying:", questionnaire.inabilityToControlWorrying)
            add_question_answer("Excessive Worrying:", questionnaire.excessiveWorrying)
            add_question_answer("Trouble Relaxing:", questionnaire.troubleRelaxing)
            add_question_answer("Restlessness:", questionnaire.restlessness)
            add_question_answer("Irritability:", questionnaire.irritability)
            add_question_answer("Fear of Something Awful:", questionnaire.fearOfSomethingAwful)

        elif questionnaire_type == "MDQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decision Making:", questionnaire.avoidIndependentDecisionMaking)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Difficulty Concentrating:", questionnaire.difficultyConcentrating)
            add_question_answer("Feel Dissatisfied With Self:", questionnaire.feelDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)
            add_question_answer("Feel Hyper To The Point Of Concern:", questionnaire.feelHyperToThePointOfConcern)
            add_question_answer("Irritability Leading To Conflict:", questionnaire.irritabilityLeadingToConflict)
            add_question_answer("Increased Self Confidence:", questionnaire.increasedSelfConfidence)
            add_question_answer("Less Sleep Than Usual:", questionnaire.lessSleepThanUsual)
            add_question_answer("More Talkative Than Usual:", questionnaire.moreTalkativeThanUsual)
            add_question_answer("Racing Thoughts:", questionnaire.racingThoughts)
            add_question_answer("Easily Distracted:", questionnaire.easilyDistracted)
            add_question_answer("More Energy Than Usual:", questionnaire.moreEnergyThanUsual)
            add_question_answer("More Active Than Usual:", questionnaire.moreActiveThanUsual)
            add_question_answer("More Social Than Usual:", questionnaire.moreSocialThanUsual)

        elif questionnaire_type == "BDI":
            add_question_answer("Feelings Of Sadness:", questionnaire.feelingsOfSadness)
            add_question_answer("Thoughts About Future:", questionnaire.thoughtsAboutFuture)
            add_question_answer("Definition Of Success:", questionnaire.definitionOfSuccess)
            add_question_answer("Ability To Experience Pleasure:", questionnaire.abilityToExperiencePleasure)
            add_question_answer("Negative Self Statements:", questionnaire.negativeSelfStatements)
            add_question_answer("Feelings Of Punishment:", questionnaire.feelingsOfPunishment)
            add_question_answer("Disappointments In Self:", questionnaire.disappointmentsInSelf)
            add_question_answer("Handling Self Criticism:", questionnaire.handlingSelfCriticism)
            add_question_answer("Thoughts Of Self Harm:", questionnaire.thoughtsOfSelfHarm)
            add_question_answer("Frequency Of Crying:", questionnaire.frequencyOfCrying)

        elif questionnaire_type == "NPQ":
            add_question_answer("Feel Dependent On Others:", questionnaire.feelDependentOnOthers)
            add_question_answer("Avoid Independent Decisions:", questionnaire.avoidIndependentDecisions)
            add_question_answer("Feel Weak Or Tired:", questionnaire.feelWeakOrTired)
            add_question_answer("Find It Difficult To Concentrate:", questionnaire.findItDifficultToConcentrate)
            add_question_answer("Frequently Dissatisfied With Self:", questionnaire.frequentlyDissatisfiedWithSelf)
            add_question_answer("Consider Self A Failure:", questionnaire.considerSelfAFailure)
            add_question_answer("Trouble Controlling Temper:", questionnaire.troubleControllingTemper)
            add_question_answer("Hesitate When Making Decisions:", questionnaire.hesitateWhenMakingDecisions)
            add_question_answer("Rely On Others For Decisions:", questionnaire.relyOnOthersForDecisions)

        elif questionnaire_type == "BFT":
            add_question_answer("Talks A Lot:", questionnaire.talksALot)
            add_question_answer("Notices Weak Points:", questionnaire.noticesWeakPoints)
            add_question_answer("Does Things Carefully:", questionnaire.doesThingsCarefully)
            add_question_answer("Is Sad/Depressed:", questionnaire.isSadDepressed)
            add_question_answer("Is Original:", questionnaire.isOriginal)
            add_question_answer("Keeps Thoughts to Themselves:", questionnaire.keepsThoughtsToThemselves)
            add_question_answer("Is Helpful Not Selfish:", questionnaire.isHelpfulNotSelfish)
            add_question_answer("Is Careless:", questionnaire.isCareless)
            add_question_answer("Is Relaxed:", questionnaire.isRelaxed)
            add_question_answer("Is Curious:", questionnaire.isCurious)

        elif questionnaire_type == "OCIR":
            add_question_answer("Saved Too Many Things:", questionnaire.savedTooManyThings)
            add_question_answer("Check Things More Often:", questionnaire.checkThingsMoreOften)
            add_question_answer("Upset If Not Arranged Properly:", questionnaire.upsetIfNotArrangedProperly)
            add_question_answer("Compelled To Count:", questionnaire.compelledToCount)
            add_question_answer("Difficult To Touch Touched Objects:", questionnaire.difficultToTouchTouchedObjects)
            add_question_answer("Difficult To Control Thoughts:", questionnaire.difficultToControlThoughts)
            add_question_answer("Collect Unnecessary Things:", questionnaire.collectUnnecessaryThings)
            add_question_answer("Repeatedly Check Items:", questionnaire.repeatedlyCheckItems)
            add_question_answer("Upset If Others Change Arrangement:", questionnaire.upsetIfOthersChangeArrangement)
            add_question_answer("Feel Compelled To Repeat Numbers:", questionnaire.feelCompelledToRepeatNumbers)

        elif questionnaire_type == "MMPI2":
            add_question_answer("Rarely Worry About Health:", questionnaire.rarelyWorryAboutHealth)
            add_question_answer("Always Tell The Truth:", questionnaire.alwaysTellTruth)
            add_question_answer("Feel Tired Most Of The Time:", questionnaire.feelTiredMostOfTheTime)
            add_question_answer("Feel Punished Without Cause:", questionnaire.feelPunishedWithoutCause)
            add_question_answer("Bothered By Upset Stomach:", questionnaire.botheredByUpsetStomach)
            add_question_answer("Get A Lot Of Headaches:", questionnaire.getLotOfHeadaches)
            add_question_answer("Like To Arrange Flowers:", questionnaire.likeToArrangeFlowers)
            add_question_answer("Someone Has It In For Me:", questionnaire.someoneHasItInForMe)
            add_question_answer("Often Disturbing Thoughts:", questionnaire.oftenDisturbingThoughts)
            add_question_answer("Hear Things Others Can't Hear:", questionnaire.hearThingsOthersCantHear)
            add_question_answer("Am Happier Than Most People:", questionnaire.amHappierThanMostPeople)
            add_question_answer("Am Easily Embarrassed:", questionnaire.amEasilyEmbarrassed)

        elif questionnaire_type == "ENNEAGRAM":
            add_question_answer("Creative Artistic View:", questionnaire.creativeArtisticView)
            add_question_answer("Feel Different From Others:", questionnaire.feelDifferentFromOthers)
            add_question_answer("Experience Melancholy:", questionnaire.experienceMelancholy)
            add_question_answer("Overly Sensitive:", questionnaire.overlySensitive)
            add_question_answer("Feel Something Is Missing:", questionnaire.feelSomethingIsMissing)
            add_question_answer("Feel Envious Of Others:", questionnaire.feelEnviousOfOthers)
            add_question_answer("Thrive In Creative Environments:", questionnaire.thriveInCreativeEnvironments)
            add_question_answer("Become Withdrawn When Misunderstood:", questionnaire.canBecomeWithdrawnWhenMisunderstood)
            add_question_answer("Romantic Longing:", questionnaire.romanticLonging)
            add_question_answer("Caught In Fantasy World:", questionnaire.caughtInFantasyWorld)
            add_question_answer("Enjoy Unique Elegant Things:", questionnaire.enjoyUniqueElegantThings)
            add_question_answer("Moody When Stressed:", questionnaire.moodyWhenStressed)
            add_question_answer("Reflective And Search For Meaning:", questionnaire.reflectiveAndSearchForMeaning)
            add_question_answer("Strive To Be Unique:", questionnaire.striveToBeUnique)
            add_question_answer("Manners And Good Taste:", questionnaire.mannersAndGoodTaste)
            add_question_answer("Seen As Overly Dramatic:", questionnaire.seenAsOverlyDramatic)
            add_question_answer("Important To Understand Feelings:", questionnaire.importantToUnderstandFeelings)

        # Build the PDF
        doc.build(story)

        # Move the buffer's position to the beginning
        buffer.seek(0)

        # Write the buffer to the response
        response.write(buffer.getvalue())
        buffer.close()

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