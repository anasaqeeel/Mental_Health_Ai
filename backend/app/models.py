from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/')
    transcript = models.TextField(blank=True, null=True)
    emotions_summary = models.JSONField(blank=True, null=True)  # Store as JSON
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video {self.id} by {self.user.name}"
    

class UserVideo(models.Model):
    user = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/')
    transcript = models.TextField(blank=True, null=True)
    emotions = models.JSONField(blank=True, null=True)


    def __str__(self):
        return self.user
    
class UserQuestionnaire(models.Model):
    # user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user=models.CharField(max_length=100)
    typeOfTherapy=models.CharField(max_length=100)
    sleepingHabits=models.CharField(max_length=100)
    physicalHealth=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    providerGender=models.CharField(max_length=100)
    dateOfBirth=models.CharField(max_length=100)
    preferredLang=models.CharField(max_length=100)
    issue=models.CharField(max_length=5000,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags=models.CharField(max_length=1000,null=True,blank=True)
class ENNEAGRAM(models.Model):
    user = models.CharField(max_length=100)
    creativeArtisticView = models.CharField(max_length=100)  # Creative and have an artistic view of life.
    feelDifferentFromOthers = models.CharField(max_length=100)  # Feel different from others, as if “on the outside looking in.”
    experienceMelancholy = models.CharField(max_length=100)  # Tend to experience more melancholy than most people I know.
    overlySensitive = models.CharField(max_length=100)  # Tend to be overly sensitive.
    feelSomethingIsMissing = models.CharField(max_length=100)  # Feel that something is missing in my life.
    feelEnviousOfOthers = models.CharField(max_length=100)  # Feel envious of other people’s relationships, lifestyles, and accomplishments.
    thriveInCreativeEnvironments = models.CharField(max_length=100)  # Thrive in environments where I can express my creativity.
    canBecomeWithdrawnWhenMisunderstood = models.CharField(max_length=100)  # When misunderstood, can become withdrawn, self-conscious, and/or rebellious.
    romanticLonging = models.CharField(max_length=100)  # Tend to be romantic and long for the great love of my life to come along.
    caughtInFantasyWorld = models.CharField(max_length=100)  # Can be caught in a fantasy world of romance and imagination.
    enjoyUniqueElegantThings = models.CharField(max_length=100)  # Enjoy having elegant, refined, unique things that no one else has. Attracted to what is intense and out of the ordinary.
    moodyWhenStressed = models.CharField(max_length=100)  # Tend to be moody, withdrawn, and self-absorbed when stressed. Tend to be compassionate, expressive, and supportive when not stressed. Can be deeply hurt by the slightest criticism.
    reflectiveAndSearchForMeaning = models.CharField(max_length=100)  # Tend to be reflective and to search for the meaning of my life.
    striveToBeUnique = models.CharField(max_length=100)  # Strive to be unique and have done things to avoid being ordinary.
    mannersAndGoodTaste = models.CharField(max_length=100)  # Manners and good taste are extremely important to me.
    seenAsOverlyDramatic = models.CharField(max_length=100)  # People have seen me as overly dramatic.
    importantToUnderstandFeelings = models.CharField(max_length=100)  # Believe it is important to understand my own and other people’s feelings.

    def __str__(self):
        return f"Enneagram Responses for User: {self.user}"
class BFTQuestionnaire(models.Model):
    user = models.CharField(max_length=100)
    talksALot = models.IntegerField()  
    noticesWeakPoints = models.IntegerField()  # Scale from 1 to 5
    doesThingsCarefully = models.IntegerField()  # Scale from 1 to 5
    isSadDepressed = models.IntegerField()  # Scale from 1 to 5
    isOriginal = models.IntegerField()  # Scale from 1 to 5
    keepsThoughtsToThemselves = models.IntegerField()  # Scale from 1 to 5
    isHelpfulNotSelfish = models.IntegerField()  # Scale from 1 to 5
    isCareless = models.IntegerField()  # Scale from 1 to 5
    isRelaxed = models.IntegerField()  # Scale from 1 to 5
    isCurious = models.IntegerField()  # Scale from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BFT Questionnaire by User {self.user}"


class MHProfessional(models.Model):
    photo=models.ImageField(null=True,blank=True)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=200)
    phone=models.CharField(max_length=100)
    therapy_specification=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dateOfBirth=models.CharField(max_length=100)
    language1=models.CharField(max_length=100)
    language2=models.CharField(max_length=100,null=True,blank=True)
    language3=models.CharField(max_length=100,null=True,blank=True)
    specialization=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)




class MMPI2Questionnaire(models.Model):
    user = models.CharField(max_length=100)
    rarelyWorryAboutHealth = models.BooleanField(default=False)
    alwaysTellTruth = models.BooleanField(default=False)
    feelTiredMostOfTheTime = models.BooleanField(default=False)
    feelPunishedWithoutCause = models.BooleanField(default=False)
    botheredByUpsetStomach = models.BooleanField(default=False)
    getLotOfHeadaches = models.BooleanField(default=False)
    likeToArrangeFlowers = models.BooleanField(default=False)
    someoneHasItInForMe = models.BooleanField(default=False)
    oftenDisturbingThoughts = models.BooleanField(default=False)
    hearThingsOthersCantHear = models.BooleanField(default=False)
    amHappierThanMostPeople = models.BooleanField(default=False)
    amEasilyEmbarrassed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
class NPQ(models.Model):
    user = models.CharField(max_length=100)
    feelDependentOnOthers = models.BooleanField(default=False)
    avoidIndependentDecisions = models.BooleanField(default=False)
    feelWeakOrTired = models.BooleanField(default=False)
    findItDifficultToConcentrate = models.BooleanField(default=False)
    frequentlyDissatisfiedWithSelf = models.BooleanField(default=False)
    considerSelfAFailure = models.BooleanField(default=False)
    troubleControllingTemper = models.BooleanField(default=False)
    hesitateWhenMakingDecisions = models.BooleanField(default=False)
    relyOnOthersForDecisions = models.BooleanField(default=False)

    def __str__(self):
        return f"NPQ Responses for User: {self.user}"
class ADHD(models.Model):
    user = models.CharField(max_length=100)
    troubleWrappingUpFinalDetails = models.CharField(max_length=100)
    difficultyGettingOrganized = models.CharField(max_length=100)
    problemsRememberingAppointments = models.CharField(max_length=100)
    avoidDelayingThoughtIntensiveTasks = models.CharField(max_length=100)
    fidgetOrSquirmWhenSitting = models.CharField(max_length=100)
    feelOverlyActiveCompelled = models.CharField(max_length=100)
    makeCarelessMistakes = models.CharField(max_length=100)
    difficultyKeepingAttention = models.CharField(max_length=100)
    difficultyConcentratingOnDirectSpeech = models.CharField(max_length=100)
    misplaceOrDifficultyFindingThings = models.CharField(max_length=100)

    def __str__(self):
        return f"ADHD Responses for User: {self.user}"
class BDI(models.Model):
    user = models.CharField(max_length=100)

    feelingsOfSadness = models.CharField(max_length=100)
    thoughtsAboutFuture = models.CharField(max_length=100)
    definitionOfSuccess = models.CharField(max_length=100)
    abilityToExperiencePleasure = models.CharField(max_length=100)
    negativeSelfStatements = models.CharField(max_length=100)
    feelingsOfPunishment = models.CharField(max_length=100)
    disappointmentsInSelf = models.CharField(max_length=100)
    handlingSelfCriticism = models.CharField(max_length=100)
    thoughtsOfSelfHarm = models.CharField(max_length=100)
    frequencyOfCrying = models.CharField(max_length=100)

    def __str__(self):
        return f"BDI Responses for User: {self.user}"
class GAD(models.Model):
    user = models.CharField(max_length=100)

    feelingNervous = models.CharField(max_length=100)
    inabilityToControlWorrying = models.CharField(max_length=100)
    excessiveWorrying = models.CharField(max_length=100)
    troubleRelaxing = models.CharField(max_length=100)
    restlessness = models.CharField(max_length=100)
    irritability = models.CharField(max_length=100)
    fearOfSomethingAwful = models.CharField(max_length=100)

    def __str__(self):
        return f"GAD Responses for User: {self.user}"
class MDQ(models.Model):
    user = models.CharField(max_length=100)

    feelDependentOnOthers = models.BooleanField(default=False)
    avoidIndependentDecisionMaking = models.BooleanField(default=False)
    feelWeakOrTired = models.BooleanField(default=False)
    difficultyConcentrating = models.BooleanField(default=False)
    feelDissatisfiedWithSelf = models.BooleanField(default=False)
    considerSelfAFailure = models.BooleanField(default=False)
    troubleControllingTemper = models.BooleanField(default=False)
    hesitateWhenMakingDecisions = models.BooleanField(default=False)
    relyOnOthersForDecisions = models.BooleanField(default=False)
    feelHyperToThePointOfConcern = models.BooleanField(default=False)
    irritabilityLeadingToConflict = models.BooleanField(default=False)
    increasedSelfConfidence = models.BooleanField(default=False)
    lessSleepThanUsual = models.BooleanField(default=False)
    moreTalkativeThanUsual = models.BooleanField(default=False)
    racingThoughts = models.BooleanField(default=False)
    easilyDistracted = models.BooleanField(default=False)
    moreEnergyThanUsual = models.BooleanField(default=False)
    moreActiveThanUsual = models.BooleanField(default=False)
    moreSocialThanUsual = models.BooleanField(default=False)

    def __str__(self):
        return f"MDQ Responses for User: {self.user}"
class OCIR(models.Model):
    user = models.CharField(max_length=100)
    savedTooManyThings = models.CharField(max_length=100)  # I have saved up so many things that they get in the way.
    checkThingsMoreOften = models.CharField(max_length=100)  # I check things more often than necessary.
    upsetIfNotArrangedProperly = models.CharField(max_length=100)  # I get upset if objects are not arranged properly.
    compelledToCount = models.CharField(max_length=100)  # I feel compelled to count while I am doing things.
    difficultToTouchTouchedObjects = models.CharField(max_length=100)  # I find it difficult to touch an object when I know it has been touched by strangers or certain people.
    difficultToControlThoughts = models.CharField(max_length=100)  # I find it difficult to control my own thoughts.
    collectUnnecessaryThings = models.CharField(max_length=100)  # I collect things I don’t need.
    repeatedlyCheckItems = models.CharField(max_length=100)  # I repeatedly check doors, windows, drawers, etc.
    upsetIfOthersChangeArrangement = models.CharField(max_length=100)  # I get upset if others change the way I have arranged things.
    feelCompelledToRepeatNumbers = models.CharField(max_length=100)  # I feel I have to repeat certain numbers.

    def __str__(self):
        return f"OCIR Responses for User: {self.user}"
class IBT(models.Model):
    user = models.CharField(max_length=100)
    image1 = models.CharField(max_length=100)  # Question related to image 1
    image2 = models.CharField(max_length=100)  # Question related to image 2
    image3 = models.CharField(max_length=100)  # Question related to image 3
    image4 = models.CharField(max_length=100)  # Question related to image 4
    image5 = models.CharField(max_length=100)  # Question related to image 5
    image6 = models.CharField(max_length=100)  # Question related to image 6
    image7 = models.CharField(max_length=100)  # Question related to image 7
    image8 = models.CharField(max_length=100)  # Question related to image 8
    image9 = models.CharField(max_length=100)  # Question related to image 9
    image10 = models.CharField(max_length=100)  # Question related to image 10

    def __str__(self):
        return f"IBT Responses for User: {self.user}"