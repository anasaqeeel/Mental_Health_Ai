import React from 'react'
import Questionnaire from './Components/Questions'
export default function index({ questions, options, userId }) {
  return (
    <div>
      <Questionnaire questions={questions} options={options}/>
    </div>
  )
}
