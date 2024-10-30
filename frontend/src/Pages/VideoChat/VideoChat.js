import React, { useState, useRef, useEffect } from 'react';
import Peer from 'peerjs';
import './VideoChat.css'; 

const VideoChat = () => {
    const [peerId, setPeerId] = useState(''); 
    const [remotePeerId, setRemotePeerId] = useState(''); 
    const [callStarted, setCallStarted] = useState(false);
    const [messages, setMessages] = useState([]); 
    const [message, setMessage] = useState(''); 

    const localVideoRef = useRef(null); 
    const remoteVideoRef = useRef(null); 
    const peerInstance = useRef(null);
    const dataConnection = useRef(null); 

    useEffect(() => {
        
        peerInstance.current = new Peer();

        
        peerInstance.current.on('open', (id) => {
            setPeerId(id);
        });

        
        peerInstance.current.on('call', (call) => {
            navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                .then((stream) => {
                    localVideoRef.current.srcObject = stream;
                    call.answer(stream);

                    call.on('stream', (remoteStream) => {
                        remoteVideoRef.current.srcObject = remoteStream;
                    });
                })
                .catch((error) => console.error('Failed to get local stream', error));
        });

        
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

    
    const startCall = () => {
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then((stream) => {
                localVideoRef.current.srcObject = stream;

                const call = peerInstance.current.call(remotePeerId, stream);
                setCallStarted(true);


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

    
    const sendMessage = () => {
        if (dataConnection.current && message.trim() !== '') {
            dataConnection.current.send(message);
            setMessages((prevMessages) => [...prevMessages, { sender: 'You', text: message }]);
            setMessage('');
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