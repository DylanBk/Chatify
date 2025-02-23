import React from "react";

export default function FriendBanner(props) {
    return (
        <>
            {props.username ? (
            <div className="w-full flex flex-row gap-4 justify-between !rounded-none card">
                <img
                    className="h-12 w-12 object-cover rounded-full bg-grey--100"
                    src={props.pfp ? `data:image/webp;base64,${props.pfp}` : ''}
                    alt="User avatar"
                />
                <div className="w-5/6 flex flex-col justify-between">
                    <h3>{props.username}</h3>
                    <p>{props.status}</p>
                </div>
                <button
                    className=""
                    onClick={() => {return}}>
                    <svg
                        className="h-8 fill-offBlack hover:fill-black focus:fill-black"
                        viewBox="0 0 12 46"
                        xmlns="http://www.w3.org/2000/svg">
                        <path d="M6 46C4.35 46 2.9375 45.437 1.7625 44.3109C0.5875 43.1849 0 41.8312 0 40.25C0 38.6688 0.5875 37.3151 1.7625 36.1891C2.9375 35.063 4.35 34.5 6 34.5C7.65 34.5 9.0625 35.063 10.2375 36.1891C11.4125 37.3151 12 38.6688 12 40.25C12 41.8312 11.4125 43.1849 10.2375 44.3109C9.0625 45.437 7.65 46 6 46ZM6 28.75C4.35 28.75 2.9375 28.187 1.7625 27.0609C0.5875 25.9349 0 24.5812 0 23C0 21.4187 0.5875 20.0651 1.7625 18.9391C2.9375 17.813 4.35 17.25 6 17.25C7.65 17.25 9.0625 17.813 10.2375 18.9391C11.4125 20.0651 12 21.4187 12 23C12 24.5812 11.4125 25.9349 10.2375 27.0609C9.0625 28.187 7.65 28.75 6 28.75ZM6 11.5C4.35 11.5 2.9375 10.937 1.7625 9.81094C0.5875 8.6849 0 7.33125 0 5.75C0 4.16875 0.5875 2.8151 1.7625 1.68906C2.9375 0.563021 4.35 0 6 0C7.65 0 9.0625 0.563021 10.2375 1.68906C11.4125 2.8151 12 4.16875 12 5.75C12 7.33125 11.4125 8.6849 10.2375 9.81094C9.0625 10.937 7.65 11.5 6 11.5Z"/>
                    </svg>
                </button>
            </div>
            ) : (
                <></>
            )}
        </>
    )
}