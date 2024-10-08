from django.contrib import admin
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
    NPQ,
    BFTQuestionnaire,
    ENNEAGRAM
)
from django.db.models import Count
from collections import Counter

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at')
    readonly_fields = ('transcript', 'emotions_summary')

    def bar_chart_emotions(self, obj):
        if obj.emotions_summary:
            emotions = obj.emotions_summary
            labels = emotions.keys()
            data = emotions.values()
            return {
                'type': 'bar',
                'data': {
                    'labels': labels,
                    'datasets': [{
                        'label': 'Emotions',
                        'data': data,
                    }]
                },
            }
        return "No emotions data"
    
@admin.register(MMPI2Questionnaire)
class MMPI2QuestionnaireAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'rarelyWorryAboutHealth', 
        'alwaysTellTruth', 
        'feelTiredMostOfTheTime', 
        'feelPunishedWithoutCause', 
        'botheredByUpsetStomach', 
        'getLotOfHeadaches', 
        'likeToArrangeFlowers', 
        'someoneHasItInForMe', 
        'oftenDisturbingThoughts', 
        'hearThingsOthersCantHear', 
        'amHappierThanMostPeople', 
        'amEasilyEmbarrassed', 
        'created_at'
    )

@admin.register(ENNEAGRAM)
class ENNEAGRAMAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'creativeArtisticView', 
        'feelDifferentFromOthers', 
        'experienceMelancholy', 
        'overlySensitive', 
        'feelSomethingIsMissing', 
        'feelEnviousOfOthers', 
        'thriveInCreativeEnvironments', 
        'canBecomeWithdrawnWhenMisunderstood', 
        'romanticLonging', 
        'caughtInFantasyWorld', 
        'enjoyUniqueElegantThings', 
        'moodyWhenStressed', 
        'reflectiveAndSearchForMeaning', 
        'striveToBeUnique', 
        'mannersAndGoodTaste', 
        'seenAsOverlyDramatic', 
        'importantToUnderstandFeelings'
    )
@admin.register(BFTQuestionnaire)
class BFTQuestionnaireAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'talksALot', 
        'noticesWeakPoints', 
        'doesThingsCarefully', 
        'isSadDepressed', 
        'isOriginal', 
        'keepsThoughtsToThemselves', 
        'isHelpfulNotSelfish', 
        'isCareless', 
        'isRelaxed', 
        'isCurious', 
        'created_at'  # Adding created_at to the display list
    )
@admin.register(NPQ)
class NPQAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'feelDependentOnOthers',
        'avoidIndependentDecisions',
        'feelWeakOrTired',
        'findItDifficultToConcentrate',
        'frequentlyDissatisfiedWithSelf',
        'considerSelfAFailure',
        'troubleControllingTemper',
        'hesitateWhenMakingDecisions',
        'relyOnOthersForDecisions',
    )

@admin.register(ADHD)
class ADHDAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'troubleWrappingUpFinalDetails',
        'difficultyGettingOrganized',
        'problemsRememberingAppointments',
        'avoidDelayingThoughtIntensiveTasks',
        'fidgetOrSquirmWhenSitting',
        'feelOverlyActiveCompelled',
        'makeCarelessMistakes',
        'difficultyKeepingAttention',
        'difficultyConcentratingOnDirectSpeech',
        'misplaceOrDifficultyFindingThings',
    )

@admin.register(BDI)
class BDIAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'feelingsOfSadness',
        'thoughtsAboutFuture',
        'definitionOfSuccess',
        'abilityToExperiencePleasure',
        'negativeSelfStatements',
        'feelingsOfPunishment',
        'disappointmentsInSelf',
        'handlingSelfCriticism',
        'thoughtsOfSelfHarm',
        'frequencyOfCrying',
    )

@admin.register(GAD)
class GADAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'feelingNervous',
        'inabilityToControlWorrying',
        'excessiveWorrying',
        'troubleRelaxing',
        'restlessness',
        'irritability',
        'fearOfSomethingAwful',
    )

@admin.register(MDQ)
class MDQAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'feelDependentOnOthers',
        'avoidIndependentDecisionMaking',
        'feelWeakOrTired',
        'difficultyConcentrating',
        'feelDissatisfiedWithSelf',
        'considerSelfAFailure',
        'troubleControllingTemper',
        'hesitateWhenMakingDecisions',
        'relyOnOthersForDecisions',
        'feelHyperToThePointOfConcern',
        'irritabilityLeadingToConflict',
        'increasedSelfConfidence',
        'lessSleepThanUsual',
        'moreTalkativeThanUsual',
        'racingThoughts',
        'easilyDistracted',
        'moreEnergyThanUsual',
        'moreActiveThanUsual',
        'moreSocialThanUsual',
    )

@admin.register(OCIR)
class OCIRAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'savedTooManyThings',
        'checkThingsMoreOften',
        'upsetIfNotArrangedProperly',
        'compelledToCount',
        'difficultToTouchTouchedObjects',
        'difficultToControlThoughts',
        'collectUnnecessaryThings',
        'repeatedlyCheckItems',
        'upsetIfOthersChangeArrangement',
        'feelCompelledToRepeatNumbers',
    )

@admin.register(IBT)
class IBTAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'image1',
        'image2',
        'image3',
        'image4',
        'image5',
        'image6',
        'image7',
        'image8',
        'image9',
        'image10',
    )
@admin.register(UserVideo)
class UserVideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'transcript', 'emotions')

    def changelist_view(self, request, extra_context=None):
        # Get the selected user from the query parameters
        selected_user = request.GET.get('user__exact', None)
        
        # Filter the queryset based on the selected user
        queryset = UserVideo.objects.all()
        if selected_user:
            queryset = queryset.filter(user=selected_user)
        
        # Aggregate emotions for the selected user
        all_emotions = []
        for video in queryset:
            if video.emotions:
                all_emotions.extend(video.emotions)
        
        # Count emotions occurrences
        emotions_count = dict(Counter(all_emotions))
        
        # Pass data to the template
        extra_context = extra_context or {}
        extra_context['emotions_data'] = emotions_count
        extra_context['selected_user'] = selected_user
        return super().changelist_view(request, extra_context=extra_context)
    
@admin.register(UserQuestionnaire)
class UserQuestionnaireAdmin(admin.ModelAdmin):
    list_display= ('user','typeOfTherapy','sleepingHabits','physicalHealth','gender','providerGender','dateOfBirth','preferredLang','issue','tags')

@admin.register(MHProfessional)
class MHProfessionalAdmin(admin.ModelAdmin):
    list_display=('photo','name','email','phone','therapy_specification','gender','dateOfBirth','language1','language2','language3','specialization')