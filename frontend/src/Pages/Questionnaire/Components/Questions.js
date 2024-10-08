import React, { useState, useEffect } from 'react';
import { ProgressBar, Button, Form, Alert } from 'react-bootstrap';
import '../Styles/questions.styles.css';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { format } from 'date-fns';
import { useNavigate } from 'react-router-dom';

import questionsData from './quest.json';

const Questionnaire = ({ questionnaireName, userId }) => {
  const selectedData = questionsData[questionnaireName];
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState(Array(selectedData.questions.length).fill(''));
  const [dateOfBirth, setDateOfBirth] = useState(null);
  const [showAlert, setShowAlert] = useState(false);

  useEffect(() => {
    console.log("Updated dateOfBirth:", dateOfBirth);
  }, [dateOfBirth]);
  const handleNext = () => {
    console.log({ dateOfBirth });
    console.log(selectedData.questions[currentStep]);
    if (dateOfBirth === null && selectedData.questions[currentStep] === "What is your date of birth?") {
      console.log({ dateOfBirth });
      setShowAlert(true);
      return;
    } else if (!answers[currentStep] && selectedData.questions[currentStep] !== "What is your date of birth?" && currentStep !== selectedData.questions.length - 1) {
      console.log("hello")
      setShowAlert(true);
      return;
    }

    setShowAlert(false);
    if (currentStep < selectedData.questions.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleInputChange = (e) => {
    const newAnswers = [...answers];
    newAnswers[currentStep] = e.target.value;
    setAnswers(newAnswers);
  };

  const handleSubmit = async () => {
    if (!answers[currentStep] && selectedData.questions[currentStep] !== "What is your date of birth?" && currentStep !== selectedData.questions.length - 1) {
      setShowAlert(true);
      return;
    }

    if (selectedData.questions[currentStep] === "What is your date of birth?" && !dateOfBirth) {
      setShowAlert(true);
      return;
    }

    setShowAlert(false);
    console.log("bft mn ", questionnaireName)
    if (questionnaireName === 'ENNEAGRAM') {
      const data = {
        user: userId || "1",  // Assigns userId if available, otherwise defaults to "1"
        creativeArtisticView: answers[0],
        feelDifferentFromOthers: answers[1],
        experienceMelancholy: answers[2],
        overlySensitive: answers[3],
        feelSomethingIsMissing: answers[4],
        feelEnviousOfOthers: answers[5],
        thriveInCreativeEnvironments: answers[6],
        canBecomeWithdrawnWhenMisunderstood: answers[7],
        romanticLonging: answers[8],
        caughtInFantasyWorld: answers[9],
        enjoyUniqueElegantThings: answers[10],
        moodyWhenStressed: answers[11],
        reflectiveAndSearchForMeaning: answers[12],
        striveToBeUnique: answers[13],
        mannersAndGoodTaste: answers[14],
        seenAsOverlyDramatic: answers[15],
        importantToUnderstandFeelings: answers[16],
      };
      console.log(data);
      try {
        const response = await fetch('http://127.0.0.1:8000/api/enneagram/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          console.log("Enneagram Questionnaire submitted successfully");
          navigate(`/landing/video-chat`); // Navigate or handle success
        } else {
          console.error("Failed to submit the Enneagram questionnaire", await response.json());
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }



    if (questionnaireName === 'NPQ') {
      const data = {
        user: userId || "1",
        feelDependentOnOthers: answers[0],
        avoidIndependentDecisions: answers[1],
        feelWeakOrTired: answers[2],
        findItDifficultToConcentrate: answers[3],
        frequentlyDissatisfiedWithSelf: answers[4],
        considerSelfAFailure: answers[5],
        troubleControllingTemper: answers[6],
        hesitateWhenMakingDecisions: answers[7],
        relyOnOthersForDecisions: answers[8],
      };
      console.log(data);
      try {
        const response = await fetch('http://127.0.0.1:8000/api/npq/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          console.log("NPQ Questionnaire submitted successfully");
          navigate(`/landing/video-chat`);
        } else {
          console.error("Failed to submit the NPQ questionnaire", await response.json());
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }

    if (questionnaireName === 'ADHD') {
      const data = {
        user: userId || "1",
        troubleWrappingUpFinalDetails: answers[0],
        difficultyGettingOrganized: answers[1],
        problemsRememberingAppointments: answers[2],
        avoidDelayingThoughtIntensiveTasks: answers[3],
        fidgetOrSquirmWhenSitting: answers[4],
        feelOverlyActiveCompelled: answers[5],
        makeCarelessMistakes: answers[6],
        difficultyKeepingAttention: answers[7],
        difficultyConcentratingOnDirectSpeech: answers[8],
        misplaceOrDifficultyFindingThings: answers[9],
      };
      console.log(data);
      try {
        const response = await fetch('http://127.0.0.1:8000/api/adhd/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          console.log("ADHD Questionnaire submitted successfully");
          navigate(`/landing/video-chat`);
        } else {
          console.error("Failed to submit the ADHD questionnaire", await response.json());
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
    if (questionnaireName === 'OCIR') {
      const data = {
        user: userId || "1",
        savedTooManyThings: answers[0],
        checkThingsMoreOften: answers[1],
        upsetIfNotArrangedProperly: answers[2],
        compelledToCount: answers[3],
        difficultToTouchTouchedObjects: answers[4],
        difficultToControlThoughts: answers[5],
        collectUnnecessaryThings: answers[6],
        repeatedlyCheckItems: answers[7],
        upsetIfOthersChangeArrangement: answers[8],
        feelCompelledToRepeatNumbers: answers[9],
      };
      console.log(data);
      try {
        const response = await fetch('http://127.0.0.1:8000/api/ocir/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          console.log("OCIR Questionnaire submitted successfully");
          navigate(`/landing/video-chat`);
        } else {
          console.error("Failed to submit the OCIR questionnaire", await response.json());
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }

    if (questionnaireName === 'MDQ') {
      const data = {
        user: userId || "1",
        feelDependentOnOthers: answers[0],
        avoidIndependentDecisionMaking: answers[1],
        feelWeakOrTired: answers[2],
        difficultyConcentrating: answers[3],
        feelDissatisfiedWithSelf: answers[4],
        considerSelfAFailure: answers[5],
        troubleControllingTemper: answers[6],
        hesitateWhenMakingDecisions: answers[7],
        relyOnOthersForDecisions: answers[8],
        feelHyperToThePointOfConcern: answers[9],
        irritabilityLeadingToConflict: answers[10],
        increasedSelfConfidence: answers[11],
        lessSleepThanUsual: answers[12],
        moreTalkativeThanUsual: answers[13],
        racingThoughts: answers[14],
        easilyDistracted: answers[15],
        moreEnergyThanUsual: answers[16],
        moreActiveThanUsual: answers[17],
        moreSocialThanUsual: answers[18],
      };
      console.log(data);
      try {
        const response = await fetch('http://127.0.0.1:8000/api/mdq/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          console.log("MDQ Questionnaire submitted successfully");
          navigate(`/landing/video-chat`);
        } else {
          console.error("Failed to submit the MDQ questionnaire", await response.json());
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
    if (questionnaireName === 'IBT') {
      const data = {
        user: userId || "1",
        image1: answers[0],
        image2: answers[1],
        image3: answers[2],
        image4: answers[3],
        image5: answers[4],
        image6: answers[5],
        image7: answers[6],
        image8: answers[7],
        image9: answers[8],
        image10: answers[9],
      };
      console.log(data);
      try {
        const response = await fetch('http://127.0.0.1:8000/api/ibt/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          console.log("IBT Questionnaire submitted successfully");
          navigate(`/landing/video-chat`);
        } else {
          console.error("Failed to submit the IBT questionnaire", await response.json());
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }

    if (questionnaireName === 'BDI') {
      const data = {
        user: userId || "1",
        feelingsOfSadness: answers[0],
        thoughtsAboutFuture: answers[1],
        definitionOfSuccess: answers[2],
        abilityToExperiencePleasure: answers[3],
        negativeSelfStatements: answers[4],
        feelingsOfPunishment: answers[5],
        disappointmentsInSelf: answers[6],
        handlingSelfCriticism: answers[7],
        thoughtsOfSelfHarm: answers[8],
        frequencyOfCrying: answers[9],
      };
      console.log(data);
      try {
        const response = await fetch('http://127.0.0.1:8000/api/bdi/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          console.log("BDI Questionnaire submitted successfully");
          navigate(`/landing/video-chat`);
        } else {
          console.error("Failed to submit the BDI questionnaire", await response.json());
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }

    if (questionnaireName === 'GAD') {
      const data = {
        user: userId || "1",
        feelingNervous: answers[0],
        inabilityToControlWorrying: answers[1],
        excessiveWorrying: answers[2],
        troubleRelaxing: answers[3],
        restlessness: answers[4],
        irritability: answers[5],
        fearOfSomethingAwful: answers[6],
      };
      console.log(data);
      try {
        const response = await fetch('http://127.0.0.1:8000/api/gad/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          console.log("GAD Questionnaire submitted successfully");
          navigate(`/landing/video-chat`);
        } else {
          console.error("Failed to submit the GAD questionnaire", await response.json());
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
    if (questionnaireName === 'BFT') {
      const data = {
        user: userId || "1",
        talksALot: parseInt(answers[0], 10),  // Correctly referencing answers array
        noticesWeakPoints: parseInt(answers[1], 10),
        doesThingsCarefully: parseInt(answers[2], 10),
        isSadDepressed: parseInt(answers[3], 10),
        isOriginal: parseInt(answers[4], 10),
        keepsThoughtsToThemselves: parseInt(answers[5], 10),
        isHelpfulNotSelfish: parseInt(answers[6], 10),
        isCareless: parseInt(answers[7], 10),
        isRelaxed: parseInt(answers[8], 10),
        isCurious: parseInt(answers[9], 10)  // Fixed isCurious reference
      };

      console.log(data)
      try {
        console.log("lun", questionnaireName)

        const response = await fetch('http://127.0.0.1:8000/api/bft-questionnaire/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (response.ok) {
          console.log("BFT Questionnaire submitted successfully");
          // Navigate or handle success
        } else {
          console.error("Failed to submit the BFT questionnaire");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }

    if (questionnaireName === 'MMPI2') {
      const data = {
        user: userId || "1",  // Assigns userId if available, otherwise defaults to "1"
        rarelyWorryAboutHealth: answers[0],  // Convert to boolean
        alwaysTellTruth: answers[1],          // Convert to boolean
        feelTiredMostOfTheTime: answers[2],   // Convert to boolean
        feelPunishedWithoutCause: answers[3], // Convert to boolean
        botheredByUpsetStomach: answers[4],   // Convert to boolean
        getLotOfHeadaches: answers[5],        // Convert to boolean
        likeToArrangeFlowers: answers[6],      // Convert to boolean
        someoneHasItInForMe: answers[7],       // Assuming you have a corresponding answer
        oftenDisturbingThoughts: answers[8],   // Assuming you have a corresponding answer
        hearThingsOthersCantHear: answers[9],  // Assuming you have a corresponding answer
        amHappierThanMostPeople: answers[10],  // Assuming you have a corresponding answer
        amEasilyEmbarrassed: answers[11],        // Assuming you have a corresponding answer
      };
      console.log(data)
      try {
        const response = await fetch('http://127.0.0.1:8000/api/mmpi2/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          console.log("MMPI2 Questionnaire submitted successfully");
          navigate(`/landing/video-chat`); // Navigate or handle success
        } else {
          console.error("Failed to submit the MMPI2 questionnaire", await response.json()); // Log error details
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }


    if (questionnaireName === 'questionnaier') {
      const data = {
        user: userId || "1",
        typeOfTherapy: answers[0],
        sleepingHabits: answers[1],
        physicalHealth: answers[2],
        gender: answers[3],
        providerGender: answers[4],
        dateOfBirth: dateOfBirth ? format(dateOfBirth, 'yyyy-MM-dd') : null,
        preferredLang: answers[6],
        issue: answers[7]
      };

      try {
        const response = await fetch('http://127.0.0.1:8000/api/questionnaire/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          navigate(`/landing/video-chat`);
        } else {
          console.error("Failed to submit the questionnaire");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  const renderQuestion = () => {
    if (selectedData.questions[currentStep] === "What is your date of birth?") {
      return (
        <div>
          <Form.Label>{selectedData.questions[currentStep]}</Form.Label>
          <DatePicker
            selected={dateOfBirth}
            onChange={(date) => {
              setDateOfBirth(date);
              console.log("Selected Date:", date);
            }}

            dateFormat="dd/MM/yyyy"
            placeholderText="dd/mm/yyyy"
            className="form-control"
          />
        </div>
      );
    } else if (selectedData.questions[currentStep] === "Do you have any additional comments or concerns?" || questionnaireName === "IBT") {
      return (
        <Form.Group controlId={`question-${currentStep}`}>
          {questionnaireName === "IBT" ? (<><img className='btnn' src={`/Assets/${selectedData.questions[currentStep]}`} alt={`Question ${currentStep}`} />
            <Form.Label>What is the First thing that U see</Form.Label></>)
            : (<Form.Label>{selectedData.questions[currentStep]}</Form.Label>)}
          <Form.Control
            as="textarea"
            rows={3}
            value={answers[currentStep]}
            onChange={handleInputChange}
          />
        </Form.Group>
      );
    } else {
      return (
        <Form.Group controlId={`question-${currentStep}`}>
          {questionnaireName === "IBT" ? (<img src={`/Assets/${selectedData.questions[currentStep]}`} alt={`Question ${currentStep}`} />)
            : (<Form.Label>{selectedData.questions[currentStep]}</Form.Label>)}
          <Form.Control
            as="select"
            value={answers[currentStep]}
            onChange={handleInputChange}
          >
            <option value="">Select an option</option>
            {selectedData.options[currentStep].map((option, index) => (
              <option key={index} value={option}>{option}</option>
            ))}
          </Form.Control>
        </Form.Group>
      );
    }
  };

  return (
    <div className='question-container'>
      <div className="form-body" style={{ maxWidth: '1000px' }}>
        <center><h1 style={{ padding: "2rem" }}>Questionnaire</h1></center>
        <p style={{ padding: "2rem" }}>Just answer some simple questions for us to get to know you better :)</p>
        <ProgressBar now={(currentStep + 1) / selectedData.questions.length * 100} />

        {showAlert && (
          <Alert variant="danger" onClose={() => setShowAlert(false)} dismissible>
            Please answer the question before proceeding.
          </Alert>
        )}

        <Form>
          <div style={{ padding: "2rem" }}>
            {renderQuestion()}
          </div>
        </Form>

        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px', padding: "2rem" }}>
          <Button variant="secondary" onClick={handleBack} disabled={currentStep === 0}>
            Back
          </Button>
          {currentStep === selectedData.questions.length - 1 ? (
            <Button variant="primary" onClick={handleSubmit}>
              Submit
            </Button>
          ) : (
            <Button variant="primary" onClick={handleNext}>
              Next
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Questionnaire;
