import React, { useState } from "react";

export default function ChatInput(props) {
    const [message, setMessage] = useState('');

    const sendMessage = () => {
        const messagePayload = {
            chatId: props.chatId,
            senderId: props.userId,
            senderUsername: props.username,
            content: message,
            timestamp: new Date().toISOString()
        };

        if (!messagePayload.chatId || !messagePayload.senderId || !messagePayload.senderUsername || !messagePayload.content) {
            return;
        };

        props.socket.emit('data', messagePayload);
        setMessage('');
    };

    return (
        <div className="h-20 w-full absolute bottom-0 flex flex-row gap-3 items-center px-8 py-12 bg-grey--000">
            <input
                value={message}
                className={`h-14 w-full px-2 rounded-2xl bg-grey--300 ${!props.chatId ? 'opacity-70 cursor-not-allowed' : ''}`}
                type="text"
                placeholder="Enter a message..."
                onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                onChange={(e) => {setMessage(e.target.value)}}
                disabled={!props.chatId}
            />
            <button
                className={`h-14 w-16 relative flex items-center justify-center !rounded-2xl ${!props.chatId ? 'hover:bg-blue--100 opacity-70 cursor-not-allowed' : ''} btn--primary`}
                onClick={sendMessage}
                disabled={!props.chatId}>
                <svg
                    className="h-7 absolute fill-white"
                    viewBox="0 0 50 42"
                    xmlns="http://www.w3.org/2000/svg">
                    <path d="M0 42V0L50 21L0 42ZM5.26316 34.125L36.4474 21L5.26316 7.875V17.0625L21.0526 21L5.26316 24.9375V34.125Z"/>
                </svg>
            </button>
        </div>
    );
};