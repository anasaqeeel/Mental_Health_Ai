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
