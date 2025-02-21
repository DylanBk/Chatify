import React from "react";

import Login from "../layout/Login";
import Signup from "../layout/Signup";

export default function Auth({form}) {
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