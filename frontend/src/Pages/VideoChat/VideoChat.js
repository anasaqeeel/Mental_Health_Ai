import React, { useState, useRef, useEffect } from 'react';
import Peer from 'peerjs';

const VideoChat = () => {
    const [peerId, setPeerId] = useState('');
    const [remotePeerId, setRemotePeerId] = useState('');
    const [callStarted, setCallStarted] = useState(false);

    const localVideoRef = useRef(null);
    const remoteVideoRef = useRef(null);
    const peerInstance = useRef(null);

    useEffect(() => {
        // Initialize peer instance
        peerInstance.current = new Peer();

        // Handle peer open event
        peerInstance.current.on('open', id => {
            setPeerId(id);
        });

        // Handle incoming calls
        peerInstance.current.on('call', call => {
            navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                .then(stream => {
                    localVideoRef.current.srcObject = stream;
                    call.answer(stream); // Answer the call with the stream

                    call.on('stream', remoteStream => {
                        remoteVideoRef.current.srcObject = remoteStream;
                    });
                });
        });

        return () => {
            peerInstance.current.destroy();
        };
    }, []);

    // Initiate a call to the remote peer
    const startCall = () => {
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then(stream => {
                localVideoRef.current.srcObject = stream;

                const call = peerInstance.current.call(remotePeerId, stream);
                setCallStarted(true);

                call.on('stream', remoteStream => {
                    remoteVideoRef.current.srcObject = remoteStream;
                });
            })
            .catch(error => console.error('Failed to get local stream', error));
    };

    return (
        <div style={{ padding: '20px' }}>
            <h2>Video Chat</h2>
            <div>
                <p>Your Peer ID: {peerId}</p>
                <input
                    type="text"
                    placeholder="Enter Remote Peer ID"
                    value={remotePeerId}
                    onChange={(e) => setRemotePeerId(e.target.value)}
                />
                <button onClick={startCall} disabled={callStarted || !remotePeerId}>
                    Start Call
                </button>
            </div>
            <div style={{ display: 'flex', marginTop: '20px' }}>
                <div style={{ marginRight: '20px' }}>
                    <h3>Local Video</h3>
                    <video ref={localVideoRef} autoPlay playsInline style={{ width: '300px', border: '1px solid black' }} />
                </div>
                <div>
                    <h3>Remote Video</h3>
                    <video ref={remoteVideoRef} autoPlay playsInline style={{ width: '300px', border: '1px solid black' }} />
                </div>
            </div>
        </div>
    );
};

export default VideoChat;
