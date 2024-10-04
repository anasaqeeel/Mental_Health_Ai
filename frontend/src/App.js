import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'fontawesome-free/css/all.min.css';
import 'mdbreact/dist/css/mdb.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Landing from './Pages/Landing';
import Login from './Pages/Login';
import Interview from './Pages/VidInterview';
import Questionnaire from './Pages/Questionnaire';
import GeneralChat from './Pages/GeneralChat';
import TopNav from './Pages/Landing/Components/TopNav';
import Footer from './Pages/Landing/Components/Footer';
import MHProfessional from './Pages/MH_Professional';
import { AuthProvider } from './Pages/Login/Components/AuthContext';
import PrivateRoute from './Components/PrivateRoute';
// import questions from './Pages/Questionnaire/Components/quest.json';
// import options from './Pages/Questionnaire/Components/opt.json';
import Multipage from './Pages/multiquestion/component/multipage';
import questions from './Pages/Questionnaire/Components/Questions';
import options from './Pages/Questionnaire/Components/Questions';
import VideoChat from './Pages/VideoChat/VideoChat'

function App() {
  return (
    <div className="App">
      <AuthProvider>
        <Router>
          {/* Remove TopNav and Footer from here if you don't want them on the login page */}
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
                  <TopNav />
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
                  <TopNav />
                  <Questionnaire questionnaireName="personal"/>
                  <Footer />
                </PrivateRoute>
              }
            />
             <Route
              path="/landing/SRT"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Multipage test="self-report"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT/ADHD"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="ADHD"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT/BDI"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="BDI"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT/OCIR"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="OCIR"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT/MDQ"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="MDQ"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/SRT/GAD"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="GAD"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Multipage test="PT"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT/BFT"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="BFT"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT/MMPI"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="MMPI2"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            {/* <Route
              path="/landing/PT/BFT"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="BFT"/>
                  <Footer />
                </PrivateRoute>
              }
            /> */}
            <Route
              path="/landing/PT/NPQ"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="NPQ"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT/ENNEAGRAM"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="ENNEAGRAM"/>
                  <Footer />
                </PrivateRoute>
              }
            />
            <Route
              path="/landing/PT/IBT"
              element={
                <PrivateRoute>
                  <TopNav />
                  <Questionnaire questionnaireName="IBT"/>
                  <Questionnaire questions={questions} options={options} />
                  <Footer />
                </PrivateRoute>
              }
            />

            {/* Video Chat Route */}
            <Route
              path="/landing/video-chat"
              element={
                <PrivateRoute>
                  <TopNav />
                  <VideoChat />
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
