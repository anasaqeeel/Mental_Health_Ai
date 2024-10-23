# Generated by Django 5.1.1 on 2024-10-20 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ADHD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('troubleWrappingUpFinalDetails', models.CharField(max_length=100)),
                ('difficultyGettingOrganized', models.CharField(max_length=100)),
                ('problemsRememberingAppointments', models.CharField(max_length=100)),
                ('avoidDelayingThoughtIntensiveTasks', models.CharField(max_length=100)),
                ('fidgetOrSquirmWhenSitting', models.CharField(max_length=100)),
                ('feelOverlyActiveCompelled', models.CharField(max_length=100)),
                ('makeCarelessMistakes', models.CharField(max_length=100)),
                ('difficultyKeepingAttention', models.CharField(max_length=100)),
                ('difficultyConcentratingOnDirectSpeech', models.CharField(max_length=100)),
                ('misplaceOrDifficultyFindingThings', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BDI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('feelingsOfSadness', models.CharField(max_length=100)),
                ('thoughtsAboutFuture', models.CharField(max_length=100)),
                ('definitionOfSuccess', models.CharField(max_length=100)),
                ('abilityToExperiencePleasure', models.CharField(max_length=100)),
                ('negativeSelfStatements', models.CharField(max_length=100)),
                ('feelingsOfPunishment', models.CharField(max_length=100)),
                ('disappointmentsInSelf', models.CharField(max_length=100)),
                ('handlingSelfCriticism', models.CharField(max_length=100)),
                ('thoughtsOfSelfHarm', models.CharField(max_length=100)),
                ('frequencyOfCrying', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BFTQuestionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('talksALot', models.CharField(max_length=100)),
                ('noticesWeakPoints', models.CharField(max_length=100)),
                ('doesThingsCarefully', models.CharField(max_length=100)),
                ('isSadDepressed', models.CharField(max_length=100)),
                ('isOriginal', models.CharField(max_length=100)),
                ('keepsThoughtsToThemselves', models.CharField(max_length=100)),
                ('isHelpfulNotSelfish', models.CharField(max_length=100)),
                ('isCareless', models.CharField(max_length=100)),
                ('isRelaxed', models.CharField(max_length=100)),
                ('isCurious', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ENNEAGRAM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('creativeArtisticView', models.CharField(max_length=100)),
                ('feelDifferentFromOthers', models.CharField(max_length=100)),
                ('experienceMelancholy', models.CharField(max_length=100)),
                ('overlySensitive', models.CharField(max_length=100)),
                ('feelSomethingIsMissing', models.CharField(max_length=100)),
                ('feelEnviousOfOthers', models.CharField(max_length=100)),
                ('thriveInCreativeEnvironments', models.CharField(max_length=100)),
                ('canBecomeWithdrawnWhenMisunderstood', models.CharField(max_length=100)),
                ('romanticLonging', models.CharField(max_length=100)),
                ('caughtInFantasyWorld', models.CharField(max_length=100)),
                ('enjoyUniqueElegantThings', models.CharField(max_length=100)),
                ('moodyWhenStressed', models.CharField(max_length=100)),
                ('reflectiveAndSearchForMeaning', models.CharField(max_length=100)),
                ('striveToBeUnique', models.CharField(max_length=100)),
                ('mannersAndGoodTaste', models.CharField(max_length=100)),
                ('seenAsOverlyDramatic', models.CharField(max_length=100)),
                ('importantToUnderstandFeelings', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GAD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('feelingNervous', models.CharField(max_length=100)),
                ('inabilityToControlWorrying', models.CharField(max_length=100)),
                ('excessiveWorrying', models.CharField(max_length=100)),
                ('troubleRelaxing', models.CharField(max_length=100)),
                ('restlessness', models.CharField(max_length=100)),
                ('irritability', models.CharField(max_length=100)),
                ('fearOfSomethingAwful', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IBT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('image1', models.CharField(max_length=100)),
                ('image2', models.CharField(max_length=100)),
                ('image3', models.CharField(max_length=100)),
                ('image4', models.CharField(max_length=100)),
                ('image5', models.CharField(max_length=100)),
                ('image6', models.CharField(max_length=100)),
                ('image7', models.CharField(max_length=100)),
                ('image8', models.CharField(max_length=100)),
                ('image9', models.CharField(max_length=100)),
                ('image10', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MDQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('feelDependentOnOthers', models.BooleanField(default=False)),
                ('avoidIndependentDecisionMaking', models.BooleanField(default=False)),
                ('feelWeakOrTired', models.BooleanField(default=False)),
                ('difficultyConcentrating', models.BooleanField(default=False)),
                ('feelDissatisfiedWithSelf', models.BooleanField(default=False)),
                ('considerSelfAFailure', models.BooleanField(default=False)),
                ('troubleControllingTemper', models.BooleanField(default=False)),
                ('hesitateWhenMakingDecisions', models.BooleanField(default=False)),
                ('relyOnOthersForDecisions', models.BooleanField(default=False)),
                ('feelHyperToThePointOfConcern', models.BooleanField(default=False)),
                ('irritabilityLeadingToConflict', models.BooleanField(default=False)),
                ('increasedSelfConfidence', models.BooleanField(default=False)),
                ('lessSleepThanUsual', models.BooleanField(default=False)),
                ('moreTalkativeThanUsual', models.BooleanField(default=False)),
                ('racingThoughts', models.BooleanField(default=False)),
                ('easilyDistracted', models.BooleanField(default=False)),
                ('moreEnergyThanUsual', models.BooleanField(default=False)),
                ('moreActiveThanUsual', models.BooleanField(default=False)),
                ('moreSocialThanUsual', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MHProfessional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100)),
                ('therapy_specification', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('dateOfBirth', models.CharField(max_length=100)),
                ('language1', models.CharField(max_length=100)),
                ('language2', models.CharField(blank=True, max_length=100, null=True)),
                ('language3', models.CharField(blank=True, max_length=100, null=True)),
                ('specialization', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MMPI2Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('rarelyWorryAboutHealth', models.BooleanField(default=False)),
                ('alwaysTellTruth', models.BooleanField(default=False)),
                ('feelTiredMostOfTheTime', models.BooleanField(default=False)),
                ('feelPunishedWithoutCause', models.BooleanField(default=False)),
                ('botheredByUpsetStomach', models.BooleanField(default=False)),
                ('getLotOfHeadaches', models.BooleanField(default=False)),
                ('likeToArrangeFlowers', models.BooleanField(default=False)),
                ('someoneHasItInForMe', models.BooleanField(default=False)),
                ('oftenDisturbingThoughts', models.BooleanField(default=False)),
                ('hearThingsOthersCantHear', models.BooleanField(default=False)),
                ('amHappierThanMostPeople', models.BooleanField(default=False)),
                ('amEasilyEmbarrassed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='NPQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('feelDependentOnOthers', models.BooleanField(default=False)),
                ('avoidIndependentDecisions', models.BooleanField(default=False)),
                ('feelWeakOrTired', models.BooleanField(default=False)),
                ('findItDifficultToConcentrate', models.BooleanField(default=False)),
                ('frequentlyDissatisfiedWithSelf', models.BooleanField(default=False)),
                ('considerSelfAFailure', models.BooleanField(default=False)),
                ('troubleControllingTemper', models.BooleanField(default=False)),
                ('hesitateWhenMakingDecisions', models.BooleanField(default=False)),
                ('relyOnOthersForDecisions', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OCIR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('savedTooManyThings', models.CharField(max_length=100)),
                ('checkThingsMoreOften', models.CharField(max_length=100)),
                ('upsetIfNotArrangedProperly', models.CharField(max_length=100)),
                ('compelledToCount', models.CharField(max_length=100)),
                ('difficultToTouchTouchedObjects', models.CharField(max_length=100)),
                ('difficultToControlThoughts', models.CharField(max_length=100)),
                ('collectUnnecessaryThings', models.CharField(max_length=100)),
                ('repeatedlyCheckItems', models.CharField(max_length=100)),
                ('upsetIfOthersChangeArrangement', models.CharField(max_length=100)),
                ('feelCompelledToRepeatNumbers', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserQuestionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('typeOfTherapy', models.CharField(max_length=100)),
                ('sleepingHabits', models.CharField(max_length=100)),
                ('physicalHealth', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('providerGender', models.CharField(max_length=100)),
                ('dateOfBirth', models.CharField(max_length=100)),
                ('preferredLang', models.CharField(max_length=100)),
                ('issue', models.CharField(blank=True, max_length=5000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tags', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('video', models.FileField(upload_to='videos/')),
                ('transcript', models.TextField(blank=True, null=True)),
                ('emotions', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_file', models.FileField(upload_to='videos/')),
                ('transcript', models.TextField(blank=True, null=True)),
                ('emotions_summary', models.JSONField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userprofile')),
            ],
        ),
    ]
