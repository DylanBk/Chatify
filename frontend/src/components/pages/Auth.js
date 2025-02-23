import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import Login from "../layout/Login";
import Signup from "../layout/Signup";

import cookieCheck from "../../utils/cookieCheck";

export default function Auth({form}) {
    const navigate = useNavigate()

    useEffect(() => {
        if (cookieCheck('loggedIn=true')) {
            navigate('/chat')
        }
    }, [navigate]);

    return (
        <main>
            <h1 className="flex flex-col items-center m-auto mt-4 text-5xl">Welcome To <span className="text-7xl">Chatify</span></h1>

            {form === "login" ? (
                <Login />
            ) : (
                <Signup />
            )}

        </main>
    );
};