import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'fontawesome-free/css/all.min.css';
import 'mdbreact/dist/css/mdb.css';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
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

const pageVariants = {
  initial: { opacity: 0, x: "-100vw" },
  in: { opacity: 1, x: 0 },
  out: { opacity: 0, x: "100vw" },
};

const pageTransition = {
  type: "tween",
  ease: "anticipate",
  duration: 0.8,
};

function App() {
  // const location = useLocation();

  return (
    <div className="App">
      <AuthProvider>
        <Router>
          <TopNav />
          <AnimatePresence mode="wait">
            <Routes >
              <Route path="/" element={<PageWrapper><Login /></PageWrapper>} />
              <Route path="/login" element={<PageWrapper><Login /></PageWrapper>} />

              <Route
                path="/landing"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Carousel />
                      <Landing />
                      <GeneralChat />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              {/* Define other routes similarly using <PageWrapper> */}
              {/* Add more routes as per your setup */}
              <Route
                path="/landing/questionnaire"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="personal" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/SRT"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Multipage test="self-report" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/SRT/ADHD"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="ADHD" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/SRT/BDI"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="BDI" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/SRT/OCIR"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="OCIR" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/SRT/MDQ"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="MDQ" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/SRT/GAD"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="GAD" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/PT"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Multipage test="PT" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/PT/BFT"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="BFT" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/PT/MMPI"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="MMPI2" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/PT/NPQ"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="NPQ" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/PT/ENNEAGRAM"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="ENNEAGRAM" />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              <Route
                path="/landing/PT/IBT"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Questionnaire questionnaireName="IBT" />
                      {/* <Questionnaire questions={questions} options={options} /> */}
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />

              {/* Video Chat Route */}
              <Route
                path="/landing/video-chat"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <VideoChat />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />

              {/* Visualization Route */}
              <Route
                path="/visualize"
                element={
                  <PrivateRoute>
                    <PageWrapper>
                      <Visualization />
                      <Footer />
                    </PageWrapper>
                  </PrivateRoute>
                }
              />
              {/* Add additional routes */}
            </Routes>
          </AnimatePresence>
        </Router>
      </AuthProvider>
    </div>
  );
}

function PageWrapper({ children }) {
  return (
    <motion.div
      initial="initial"
      animate="in"
      exit="out"
      variants={pageVariants}
      transition={pageTransition}
    >
      {children}
    </motion.div>
  );
}

export default App;
