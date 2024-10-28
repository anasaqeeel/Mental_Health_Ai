// frontend/src/App.js

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'fontawesome-free/css/all.min.css';
import 'mdbreact/dist/css/mdb.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Landing from './Pages/Landing';
import Login from './Pages/Login';
import Interview from './Pages/VidInterview';
import Visualization from './Pages/Visualize/Visualization';
import Questionnaire from './Pages/Questionnaire';
import GeneralChat from './Pages/GeneralChat';
import TopNav from './Pages/Landing/Components/TopNav';
import Footer from './Pages/Landing/Components/Footer';
import MHProfessional from './Pages/MH_Professional';
import { AuthProvider } from './Pages/Login/Components/AuthContext';
import PrivateRoute from './Components/PrivateRoute';
import Multipage from './Pages/multiquestion/component/multipage';
import VideoChat from './Pages/VideoChat/VideoChat';
import Carousel from './Pages/Landing/Components/Carousal';

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <Router>
          {/* TopNav is outside Routes to appear on all pages */}
          <TopNav />
          <Routes>
            {/* Default route to Login */}
            <Route path="/" element={<Login />} />
            {/* Explicitly define /login route */}
            <Route path="/login" element={<Login />} />

            {/* Protected routes */}
            <Route
              path="/landing"
              element={
                <PrivateRoute>
                  <Carousel />
                  <Landing />
                  <GeneralChat />
                  <Footer />
                </PrivateRoute>
              }
            />

            {/* Add the Questionnaire route under /landing */}
            <Route
              path="/landing/questionnaire"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="personal" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT"
              element={
                <PrivateRoute>
                  <Multipage test="self-report" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT/ADHD"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="ADHD" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT/BDI"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="BDI" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT/OCIR"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="OCIR" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT/MDQ"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="MDQ" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT/GAD"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="GAD" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT"
              element={
                <PrivateRoute>
                  <Multipage test="PT" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT/BFT"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="BFT" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT/MMPI"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="MMPI2" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT/NPQ"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="NPQ" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT/ENNEAGRAM"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="ENNEAGRAM" />
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT/IBT"
              element={
                <PrivateRoute>
                  <Questionnaire questionnaireName="IBT" />
                  {/* <Questionnaire questions={questions} options={options} /> */}
                  <Footer />
                </PrivateRoute>
              }
            />

            {/* Video Chat Route */}
            <Route
              path="/landing/video-chat"
              element={
                <PrivateRoute>
                  <VideoChat />
                  <Footer />
                </PrivateRoute>
              }
            />

            {/* Visualization Route */}
            <Route
              path="/visualize"
              element={
                <PrivateRoute>
                  <Visualization />
                  <Footer />
                </PrivateRoute>
              }
            />
          </Routes>
        </Router>
      </AuthProvider>
    </div>
  );
}

export default App;
