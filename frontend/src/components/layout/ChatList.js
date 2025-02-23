import React, { useEffect, useState } from "react";

import ProfileBanner from "./ProfileBanner";

export default function ChatList({userData, handleChatData}) {
    const [chats, setChats] = useState([]);

    useEffect(() => {
        const getChatList = async () => {
            const res = await fetch('/chatlist', {
                method: 'GET',
            })
            .then(res => res.json());

            if (res.message) {
                setChats([res.data]);
            } else {
                console.error(res.error)
            };
        };

        getChatList();
    }, []);

    const loadChataData = (id) => {
        handleChatData(id);
    };

    return (
        <div className="h-screen w-1/3 relative flex flex-col overflow-y-scroll bg-grey--200">
            {chats.map((chat, i) => (
                <div
                    key={chat[i].id}
                    className="h-20 flex flex-row gap-4 items-center border-b border-grey--300 bg-grey--100 hover:bg-blue--300 focus:bg-blue-300 cursor-default"
                    onClick={() => loadChataData(chat[i].id)}>
                    <img
                        className="h-12 w-12 object-cover rounded-full ml-2 bg-grey--100"
                        src={chat[i].pfp ? `data:image/webp;base64,${chat[i].pfp}` : ''}
                        alt="User avatar"
                    />
                    <div className="flex flex-col justify-between my-1 text-offBlack hover:!text-black focus:text-black">
                        <h3 className="text-lg overflow-ellipsis">{chat[i].username}</h3>

                        {chat[i].lastMessage ? (
                            <p className="text-base overflow-ellipsis">{chat[i].lastMessage.senderId === userData.id ? "You: " : `${chat[i].username}: `}{chat[i].lastMessage.content}</p>
                        ) : (
                            <p className="text-base overflow-ellipsis">You haven't messaged this user yet</p>
                        )}

                    </div>
                </div>
            ))}
            <ProfileBanner userData={userData} />
        </div>
    );
};