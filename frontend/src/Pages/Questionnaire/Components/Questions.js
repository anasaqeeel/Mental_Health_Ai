import React, { useState } from 'react';
import { ProgressBar, Button, Form, Alert, Card, Container, Row, Col } from 'react-bootstrap';
import DatePicker from 'react-datepicker';
import { format } from 'date-fns';
import { useNavigate } from 'react-router-dom';
import 'react-datepicker/dist/react-datepicker.css';
import '../Styles/questions.styles.css';

import questionsData from './quest.json';

const Questionnaire = ({ questionnaireName, userId }) => {
  const selectedData = questionsData[questionnaireName];
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState(Array(selectedData.questions.length).fill(''));
  const [dateOfBirth, setDateOfBirth] = useState(null);
  const [showAlert, setShowAlert] = useState(false);

  const handleNext = () => {
    if (dateOfBirth === null && selectedData.questions[currentStep] === "What is your date of birth?") {
      setShowAlert(true);
      return;
    } else if (!answers[currentStep] && selectedData.questions[currentStep] !== "What is your date of birth?" && currentStep !== selectedData.questions.length - 1) {
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
    // console.log("bft mn ", questionnaireName)
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
          navigate(`/landing`);
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
          navigate(`/landing`);
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
          navigate(`/landing`);
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
          navigate(`/landing`);
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
          navigate(`/landing`);
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
          navigate(`/landing`);
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
          navigate(`/landing`);
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
          navigate(`/landing`);
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
        talksALot: answers[0],
        noticesWeakPoints: answers[1],
        doesThingsCarefully: answers[2],
        isSadDepressed: answers[3],
        isOriginal: answers[4],
        keepsThoughtsToThemselves: answers[5],
        isHelpfulNotSelfish: answers[6],
        isCareless: answers[7],
        isRelaxed: answers[8],
        isCurious: answers[9]
      };

      console.log(data)
      try {


        const response = await fetch('http://127.0.0.1:8000/api/bft-questionnaire/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (response.ok) {
          console.log("BFT Questionnaire submitted successfully");
          navigate(`/landing`);
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
        rarelyWorryAboutHealth: answers[0],
        alwaysTellTruth: answers[1],
        feelTiredMostOfTheTime: answers[2],
        feelPunishedWithoutCause: answers[3],
        botheredByUpsetStomach: answers[4],
        getLotOfHeadaches: answers[5],
        likeToArrangeFlowers: answers[6],
        someoneHasItInForMe: answers[7],
        oftenDisturbingThoughts: answers[8],
        hearThingsOthersCantHear: answers[9],
        amHappierThanMostPeople: answers[10],
        amEasilyEmbarrassed: answers[11],
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
          navigate(`/landing`);
        } else {
          console.error("Failed to submit the MMPI2 questionnaire", await response.json()); // Log error details
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }


    if (questionnaireName === 'personal') {
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
        <Form.Group className="mb-4">
          <Form.Label className="fw-bold">{selectedData.questions[currentStep]}</Form.Label>
          <DatePicker
            selected={dateOfBirth}
            onChange={(date) => setDateOfBirth(date)}
            dateFormat="dd/MM/yyyy"
            placeholderText="dd/mm/yyyy"
            className="form-control"
          />
        </Form.Group>
      );
    } else if (selectedData.questions[currentStep] === "Do you have any additional comments or concerns?" || questionnaireName === "IBT") {
      return (
        <Form.Group className="mb-4">
          {questionnaireName === "IBT" && (
            <div className="mb-3">
              <img src={`/Assets/${selectedData.questions[currentStep]}`} alt={`Question ${currentStep}`} className="img-fluid rounded shadow" />
            </div>
          )}
          <Form.Label className="fw-bold">{questionnaireName === "IBT" ? "What is the first thing that you see?" : selectedData.questions[currentStep]}</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            value={answers[currentStep]}
            onChange={handleInputChange}
            className="shadow-sm"
          />
        </Form.Group>
      );
    } else {
      return (
        <Form.Group className="mb-4">
          {questionnaireName === "IBT" && (
            <div className="mb-3">
              <img src={`/Assets/${selectedData.questions[currentStep]}`} alt={`Question ${currentStep}`} className="img-fluid rounded shadow" />
            </div>
          )}
          <Form.Label className="fw-bold">{selectedData.questions[currentStep]}</Form.Label>
          <Form.Select
            value={answers[currentStep]}
            onChange={handleInputChange}
            className="shadow-sm"
          >
            <option value="">Select an option</option>
            {selectedData.options[currentStep].map((option, index) => (
              <option key={index} value={option}>{option}</option>
            ))}
          </Form.Select>
        </Form.Group>
      );
    }
  };

  return (
    <Container className="py-5">
      <Row className="justify-content-center">
        <Col md={8} lg={6}>
          <Card className="shadow-lg">
            <Card.Body className="p-4">
              <h1 className="text-center mb-4 text-primary">Questionnaire</h1>
              <p className="text-center mb-4 text-muted">Just answer some simple questions for us to get to know you better :)</p>

              <ProgressBar
                now={(currentStep + 1) / selectedData.questions.length * 100}
                className="mb-4 shadow-sm"
                variant="info"
              />

              {showAlert && (
                <Alert variant="danger" onClose={() => setShowAlert(false)} dismissible className="mb-4">
                  Please answer the question before proceeding.
                </Alert>
              )}

              <Form className="mb-4">
                {renderQuestion()}
              </Form>

              <div className="d-flex justify-content-between">
                <Button
                  variant="outline-secondary"
                  onClick={handleBack}
                  disabled={currentStep === 0}
                  className="shadow-sm"
                >
                  Back
                </Button>
                {currentStep === selectedData.questions.length - 1 ? (
                  <Button
                    variant="primary"
                    onClick={handleSubmit}
                    className="shadow-sm"
                  >
                    Submit
                  </Button>
                ) : (
                  <Button
                    variant="primary"
                    onClick={handleNext}
                    className="shadow-sm"
                  >
                    Next
                  </Button>
                )}
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Questionnaire;