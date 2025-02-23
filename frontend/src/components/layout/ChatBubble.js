import React from "react";

export default function ChatBubble(props) {
    if (props.message) {
        const [senderUserId, _] = props.message.senderId.split('/');
        const ownMessage = props.userId === senderUserId;

        return (
            <div className={`h-fit w-96 p-2 rounded-md ${ownMessage ? 'place-self-end mr-4 bg-blue--300': 'ml-4 bg-grey--200'}`}>
                <p className="font-bold">{ownMessage ? 'You' : props.message.senderUsername} | {props.message.timestamp}</p>
                <p className="break-words">{props.message.content}</p>
            </div>
        );
    };
};