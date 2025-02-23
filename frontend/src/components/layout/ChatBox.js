import React, { useEffect, useState } from "react";

import FriendBanner from "./FriendBanner";
import ChatBubble from "./ChatBubble";
import ChatInput from "./ChatInput";

import useWebSocket from "../../hooks/useWebSocket";

export default function ChatBox(props) {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        setMessages(props.chatData.messages)
    }, [props.chatData.messages])

    const socket = useWebSocket(
        process.env.FLASK_URL,
        (data) => {
            setMessages(prevMessages => [
                ...prevMessages,
                data
            ]);
            if (document.getElementById('chats')) {
                setTimeout(() => { // delay so that DOM has time to create new element for message before scrolling
                    document.getElementById('chats').scrollTo(0, document.getElementById('chats').scrollHeight)
                }, 500)
            }
        }
    );

    return (
        <div className="h-screen w-2/3 relative flex-col overflow-hidden">
            <FriendBanner username={props.chatData.username} status={props.chatData.status} pfp={props.chatData.pfp} />
            {messages ? (
                <>
                    <div id="chats" className="h-2/3 flex flex-col gap-3 overflow-y-scroll">
                    { Array.isArray(messages) ? (
                        messages.map((message, i) => (
                            <ChatBubble key={i} userId={props.userData.id} message={message} />
                        ))
                    ) : (
                        <p className="m-auto text-lg text-blue--100">Send your first message</p>
                    )}
                    </div>
                </>
            ) : (
                <h2 className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 md:text-nowrap text-xl font-bold">You need to open a chat before sending a message</h2>
            )}
            <ChatInput socket={socket} userId={props.userData.id} username={props.userData.username} chatId={props.chatData.id} />
        </div>
    );
};