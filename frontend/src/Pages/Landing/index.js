import React from "react";
import { useNavigate } from 'react-router-dom'; // Import useNavigate hook
import SelectionPallete from "./Components/SelectionPallete";
import Faq from "./Components/Faq";

export default function Landing() {
  const navigate = useNavigate();

  // Handler function to navigate to the video chat page
  const handleVideoChatClick = () => {
    navigate('/landing/video-chat');
  };

  return (
    <div>
      {/* Video Chat Button */}
      {/* <div style={{ margin: '20px', textAlign: 'center' }}>
        <button
          onClick={handleVideoChatClick}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Start Video Chat
        </button>
      </div> */}

      {/* Other Components */}
      <SelectionPallete />
      <Faq />
    </div>
  );
}
