import React from 'react';
import Questionnaire from './Components/Questions';
import { useAuth } from '../Login/Components/AuthContext';

export default function Index({ questionnaireName }) {
  const { currentUser } = useAuth();

  // Check if the user is logged in and has a valid userId
  if (!currentUser || !currentUser.uid) {
    return <div>Loading or User is not authenticated.</div>; // You could show a loading state or redirect to login
  }

  const userId = currentUser.uid;  // Extract userId from Firebase's currentUser

  return (
    <div>
      {/* Pass userId as a prop to the Questionnaire */}
      <Questionnaire questionnaireName={questionnaireName} userId={userId} />
    </div>
  );
}
