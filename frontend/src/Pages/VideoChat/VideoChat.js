import React, { useState, useRef, useEffect } from 'react';
import Peer from 'peerjs';
import './VideoChat.css'; // CSS file for styling

const VideoChat = () => {
    const [peerId, setPeerId] = useState('');
    const [remotePeerId, setRemotePeerId] = useState('');
    const [callStarted, setCallStarted] = useState(false);
    const [dataConnection, setDataConnection] = useState(null); // To manage data connection for chat
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]); // Store chat messages
    const [isChatOpen, setIsChatOpen] = useState(false);

    const localVideoRef = useRef(null);
    const remoteVideoRef = useRef(null);
    const peerInstance = useRef(null);

    useEffect(() => {
        peerInstance.current = new Peer();

        peerInstance.current.on('open', id => {
            setPeerId(id);
        });

        peerInstance.current.on('call', call => {
            navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                .then(stream => {
                    localVideoRef.current.srcObject = stream;
                    call.answer(stream);

                    call.on('stream', remoteStream => {
                        remoteVideoRef.current.srcObject = remoteStream;
                    });
                });
        });

        // Handle incoming data connections
        peerInstance.current.on('connection', conn => {
            setDataConnection(conn);
            conn.on('data', (data) => {
                setMessages(prevMessages => [...prevMessages, { sender: 'Peer', text: data }]);
            });
        });

        return () => {
            peerInstance.current.destroy();
        };
    }, []);

    const startCall = () => {
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then(stream => {
                localVideoRef.current.srcObject = stream;

                const call = peerInstance.current.call(remotePeerId, stream);
                setCallStarted(true);

                call.on('stream', remoteStream => {
                    remoteVideoRef.current.srcObject = remoteStream;
                });

                // Establish data connection for chat
                const conn = peerInstance.current.connect(remotePeerId);
                setDataConnection(conn);

                conn.on('data', (data) => {
                    setMessages(prevMessages => [...prevMessages, { sender: 'Peer', text: data }]);
                });
            })
            .catch(error => console.error('Failed to get local stream', error));
    };

    // Send a chat message to the peer
    const sendMessage = () => {
        if (dataConnection && message.trim()) {
            dataConnection.send(message);
            setMessages(prevMessages => [...prevMessages, { sender: 'You', text: message }]);
            setMessage(''); // Clear input
        }
    };

    return (
        <div className="video-chat-container">
            <header className="header">
                <nav className="navbar">
                    <h1 className="site-title">Mental Health Counseling</h1>
                    <ul className="nav-links">
                        <li><a href="/">Home</a></li>
                        <li><a href="/interview">Take An Interview</a></li>
                        <li><a href="/help">Seek Help</a></li>
                        <li><button className="login-btn">Log In</button></li>
                    </ul>
                </nav>
            </header>
            <main>
                <div className="video-chat">
                    <div className="peer-id-section">
                        <p><strong>Your Peer ID:</strong> {peerId}</p>
                        <input
                            type="text"
                            placeholder="Enter Remote Peer ID"
                            value={remotePeerId}
                            onChange={(e) => setRemotePeerId(e.target.value)}
                            className="peer-id-input"
                        />
                        <button onClick={startCall} className="start-call-btn" disabled={callStarted || !remotePeerId}>
                            Start Call
                        </button>
                    </div>
                    <div className="video-section">
                        <div className="video-card">
                            <h3>Local Video</h3>
                            <video ref={localVideoRef} autoPlay playsInline className="video" />
                        </div>
                        <div className="video-card">
                            <h3>Remote Video</h3>
                            <video ref={remoteVideoRef} autoPlay playsInline className="video" />
                        </div>
                    </div>
                </div>
                {/* Chat Button and Chat Sidebar */}
                <button className="chat-button" onClick={() => setIsChatOpen(!isChatOpen)}>💬</button>
                {isChatOpen && (
                    <div className="chat-sidebar">
                        <div className="chat-header">
                            <h3>In-call Messages</h3>
                            <button className="close-chat-btn" onClick={() => setIsChatOpen(false)}>✖</button>
                        </div>
                        <div className="chat-messages">
                            {messages.map((msg, index) => (
                                <div key={index} className={`message ${msg.sender === 'You' ? 'sent' : 'received'}`}>
                                    <p><strong>{msg.sender}:</strong> {msg.text}</p>
                                </div>
                            ))}
                        </div>
                        <div className="chat-input-section">
                            <input
                                type="text"
                                placeholder="Send a message..."
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                className="chat-input"
                            />
                            <button onClick={sendMessage} className="send-btn">Send</button>
                        </div>
                    </div>
                )}
            </main>
            <footer className="footer">
                <p>Sign up for personalized emails and queries</p>
                <form className="newsletter-form">
                    <input type="email" placeholder="Email address" className="email-input" />
                    <button type="submit" className="subscribe-btn">Subscribe</button>
                </form>
            </footer>
        </div>
    );
};

export default VideoChat;

