import {React, useEffect} from "react";
import { Link, useNavigate } from "react-router-dom";

import cookieCheck from "../../utils/cookieCheck";

export default function Home() {
    const navigate = useNavigate()

    useEffect(() => {
        if (cookieCheck('loggedIn=true')) {
            navigate('/chat')
        }
    }, [navigate]);

    return (
        <main className="flex flex-col items-center">
            <h1 className="flex flex-col items-center m-auto mt-8 text-5xl">Welcome To <span className="text-7xl">Chatify</span></h1>

            <div className="w-64 sm:w-96 flex flex-col gap-14 items-center mt-44 sm:mt-28 text-2xl">
                <Link className="w-full btn--primary" to="/login">Login</Link>
                <Link className="w-full btn--secondary" to="/signup">Sign Up</Link>
            </div>
        </main>
    );
};