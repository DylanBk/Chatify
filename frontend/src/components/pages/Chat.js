import React, { useEffect, useState } from "react";

import ChatBox from "../layout/ChatBox";
import ChatList from "../layout/ChatList";

export default function Chat() {
    const [userData, setUserData] = useState({});
    const [chatData, setChatData] = useState({});

    useEffect(() => {
        const getUserData = async () => {
            const res = await fetch('/userdata', {
                method: 'GET'
            })
            .then(res => res.json())

            if (res.message) {
                setUserData(res.data);
            } else {
                console.error(res.error);
            };
        };
        getUserData();
    }, []);

    const handleChatData = async (id) => {
        const res = await fetch('/chats', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(id)
        })
        .then(res => res.json())

        if (res.message) {
            setChatData(res.data);
        }
        else {
            console.error(res.error);
        };
    };

    return (
        <div className="flex flex-row">
            <ChatList userData={userData} handleChatData={handleChatData} />
            <ChatBox userData={userData} chatData={chatData} />
        </div>
    );
};