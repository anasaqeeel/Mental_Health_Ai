import React from 'react'
import Questionnaire from './Components/Questions'
export default function index({ questionnaireName, userId }) {
  return (
    <div>
      <Questionnaire questionnaireName={questionnaireName} userId={userId}/>
    </div>
  )
}
