import React, { useState, useRef, useEffect } from 'react';
import Peer from 'peerjs';
import './VideoChat.css'; // Create a CSS file for styling

const VideoChat = () => {
    const [peerId, setPeerId] = useState(''); // Local Peer ID
    const [remotePeerId, setRemotePeerId] = useState(''); // Remote Peer ID
    const [callStarted, setCallStarted] = useState(false); // Track if call has started
    const [messages, setMessages] = useState([]); // Chat messages
    const [message, setMessage] = useState(''); // Input message

    const localVideoRef = useRef(null); // Reference for local video element
    const remoteVideoRef = useRef(null); // Reference for remote video element
    const peerInstance = useRef(null); // Reference to hold the PeerJS instance
    const dataConnection = useRef(null); // Reference for data connection for chat

    useEffect(() => {
        // Initialize peer instance
        peerInstance.current = new Peer();

        // Handle peer open event
        peerInstance.current.on('open', (id) => {
            setPeerId(id);
        });

        // Handle incoming calls
        peerInstance.current.on('call', (call) => {
            navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                .then((stream) => {
                    localVideoRef.current.srcObject = stream;
                    call.answer(stream); // Answer the call with the stream

                    call.on('stream', (remoteStream) => {
                        remoteVideoRef.current.srcObject = remoteStream;
                    });
                })
                .catch((error) => console.error('Failed to get local stream', error));
        });

        // Handle incoming data connection
        peerInstance.current.on('connection', (conn) => {
            dataConnection.current = conn;
            conn.on('data', (data) => {
                setMessages((prevMessages) => [...prevMessages, { sender: 'Remote', text: data }]);
            });
        });

        return () => {
            if (peerInstance.current) {
                peerInstance.current.destroy();
            }
        };
    }, []);

    // Initiate a call to the remote peer
    const startCall = () => {
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then((stream) => {
                localVideoRef.current.srcObject = stream;

                const call = peerInstance.current.call(remotePeerId, stream);
                setCallStarted(true);

                // Establish a data connection for chat
                const conn = peerInstance.current.connect(remotePeerId);
                dataConnection.current = conn;

                conn.on('open', () => {
                    console.log('Data connection established.');
                });

                conn.on('data', (data) => {
                    setMessages((prevMessages) => [...prevMessages, { sender: 'Remote', text: data }]);
                });

                call.on('stream', (remoteStream) => {
                    remoteVideoRef.current.srcObject = remoteStream;
                });

                call.on('close', () => {
                    setCallStarted(false);
                    remoteVideoRef.current.srcObject = null;
                });
            })
            .catch((error) => console.error('Failed to get local stream', error));
    };

    // Send a chat message to the remote peer
    const sendMessage = () => {
        if (dataConnection.current && message.trim() !== '') {
            dataConnection.current.send(message);
            setMessages((prevMessages) => [...prevMessages, { sender: 'You', text: message }]);
            setMessage(''); // Clear the input field
        }
    };

    return (
        <div className="video-chat-container">
            <h2 className="title">Video Chat with Integrated Messaging</h2>
            <div className="peer-info">
                <p><strong>Your Peer ID:</strong> {peerId}</p>
                <input
                    type="text"
                    placeholder="Enter Remote Peer ID"
                    value={remotePeerId}
                    onChange={(e) => setRemotePeerId(e.target.value)}
                    className="peer-id-input"
                />
                <button onClick={startCall} disabled={callStarted || !remotePeerId} className="start-call-btn">
                    {callStarted ? 'Call In Progress' : 'Start Call'}
                </button>
            </div>
            <div className="video-section">
                <div className="video-container">
                    <h3>Local Video</h3>
                    <video ref={localVideoRef} autoPlay playsInline className="video-box" />
                </div>
                <div className="video-container">
                    <h3>Remote Video</h3>
                    <video ref={remoteVideoRef} autoPlay playsInline className="video-box" />
                </div>
            </div>
            <div className="chat-section">
                <h3>Chat</h3>
                <div className="chat-box">
                    {messages.map((msg, index) => (
                        <div key={index} className={`chat-message ${msg.sender === 'You' ? 'your-message' : 'remote-message'}`}>
                            <strong>{msg.sender}: </strong> {msg.text}
                        </div>
                    ))}
                </div>
                <div className="chat-input-container">
                    <input
                        type="text"
                        placeholder="Type your message..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        className="chat-input"
                    />
                    <button onClick={sendMessage} className="send-message-btn">
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};

export default VideoChat;