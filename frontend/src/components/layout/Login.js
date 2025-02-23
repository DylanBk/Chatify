import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import show from "../../assets/icons/show.svg";
import hide from "../../assets/icons/hide.svg";

export default function Login() {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [error, setError] = useState('');
    const navigate = useNavigate()

    const handleChange = (e) => {
        const {name, value} = e.target;

        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        for (const key in formData) {
            if (formData[key] === '') {
                setError('All fields are required');
                return false;
            };
        };

        setError('');

        try {
            const res = await fetch('/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(formData)
            })
            .then(res => res.json())
            console.log(res)

            if (res.message) {
                document.cookie = 'loggedIn=true;'; //TODO: replace with server cookie
                navigate('/chat')
            } else {
                setError(res.error)
            }
        } catch(err) {
            console.error(err);
        };
    };

    const togglePw = (e) => {
        const btn = e.target;
        const input = e.target.previousSibling;

        if (input.type === 'password') {
            input.type = 'text';
            btn.src = hide;
        } else {
            input.type = 'password';
            btn.src = show;
        };
    };

    const handleKey = (e) => {
        if (e.keyCode === '13') {
            togglePw(e);
        };
    };

    return (
        <form className="w-fit flex flex-col gap-4 mt-12 card" onSubmit={handleSubmit}>
            <div className="form__input--txt">
                <label className="text-lg" htmlFor="email">Email</label>
                <input
                    id="email"
                    name="email"
                    className="w-96"
                    type="email"
                    placeholder="Enter your email address..."
                    onChange={handleChange}
                    required
                />
            </div>

            <div className="form__input--txt">
                <label className="text-lg" htmlFor="password">Password</label>
                <div className="relative flex flex-row items-center">
                    <input
                        id="password"
                        name="password"
                        className="w-96"
                        type="password"
                        minLength="8"
                        placeholder="Create a password..."
                        onChange={handleChange}
                        required
                    />
                    <img
                        className="min-w-5 absolute right-2 p-1 cursor-pointer"
                        src={show}
                        alt="Show password icon"
                        tabIndex={0}
                        onClick={togglePw}
                        onKeyDown={handleKey}
                    />
                </div>
            </div>

            <p className="mx-auto -my-2 text-red--100">{error}</p>

            <button
                className="w-64 mx-auto mt-2 text-xl btn--primary"
                type="submit">
                Login
            </button>

            <Link className="mx-auto mt-2 text-blue--100" to="/signup">I don't have an account</Link>
        </form>
    );
};