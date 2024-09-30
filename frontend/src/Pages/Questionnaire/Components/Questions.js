import React, { useState, useEffect } from 'react';
import { ProgressBar, Button, Form, Alert } from 'react-bootstrap';
import '../Styles/questions.styles.css';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { format } from 'date-fns';
import { useNavigate } from 'react-router-dom';

const Questionnaire = ({ questions, options, userId }) => {
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState(Array(questions.length).fill(''));
  const [dateOfBirth, setDateOfBirth] = useState(null);
  const [showAlert, setShowAlert] = useState(false);

  useEffect(() => {
    console.log("Updated dateOfBirth:", dateOfBirth);
  }, [dateOfBirth]);
  const handleNext = () => {
    console.log({ dateOfBirth });
    console.log(questions[currentStep]);
    if (dateOfBirth === null && questions[currentStep] === "What is your date of birth?") {
      console.log({ dateOfBirth });
      setShowAlert(true);
      return;
    } else if (!answers[currentStep] && questions[currentStep] !== "What is your date of birth?" && currentStep !== questions.length - 1) {
      console.log("hello")
      setShowAlert(true);
      return;
    }

    setShowAlert(false);
    if (currentStep < questions.length - 1) {
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
    if (!answers[currentStep] && questions[currentStep] !== "What is your date of birth?" && currentStep !== questions.length - 1) {
      setShowAlert(true);
      return;
    }

    if (questions[currentStep] === "What is your date of birth?" && !dateOfBirth) {
      setShowAlert(true);
      return;
    }

    setShowAlert(false);

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
        navigate(`/matched-professionals`);
      } else {
        console.error("Failed to submit the questionnaire");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const renderQuestion = () => {
    if (questions[currentStep] === "What is your date of birth?") {
      return (
        <div>
          <Form.Label>{questions[currentStep]}</Form.Label>
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
    } else if (questions[currentStep] === "Do you have any additional comments or concerns?") {
      return (
        <Form.Group controlId={`question-${currentStep}`}>
          <Form.Label>{questions[currentStep]}</Form.Label>
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
          <Form.Label>{questions[currentStep]}</Form.Label>
          <Form.Control
            as="select"
            value={answers[currentStep]}
            onChange={handleInputChange}
          >
            <option value="">Select an option</option>
            {options[currentStep].map((option, index) => (
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
        <ProgressBar now={(currentStep + 1) / questions.length * 100} />

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
          {currentStep === questions.length - 1 ? (
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
