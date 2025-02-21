import React, { useState } from "react";
import { Link } from "react-router-dom";

import show from "../../assets/icons/show.svg";
import hide from "../../assets/icons/hide.svg";

export default function Signup() {
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        'confirm-password': ''
    });
    const [error, setError] = useState('');

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

        if (formData["password"] !== formData["confirm-password"]) {
            setError('Passwords must match')

            return;
        };

        const regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/;
        if ( !regex.test(formData["password"]) ) {
            setError('Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one number')
            return;
        };

        setError('');
        delete formData['confirm-password'];

        try {
            const res = await fetch('/signup', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(formData)
            })
            .then(res => res.json())

            if (res.message) {
                window.location.href = '/login';
            } else {
                setError(res.error)
            };
        } catch(err) {
            console.error(err)
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
        <form className="w-fit flex flex-col gap-2 mt-12 card" onSubmit={handleSubmit}>
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
                <label className="text-lg" htmlFor="username">Username</label>
                <input
                    id="username"
                    name="username"
                    className="w-96"
                    type="text"
                    placeholder="Create a username..."
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

            <div className="form__input--txt">
                <label className="text-lg" htmlFor="confirm-password">Confirm Password</label>
                <div className="relative flex flex-row items-center">
                    <input
                        id="confirm-password"
                        name="confirm-password"
                        className="w-96"
                        type="password"
                        minLength="8"
                        placeholder="Enter your password again..."
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

            <p className="w-96 mx-auto -my-2 text-sm text-wrap leading-tight text-red--100">{error}</p>

            <button
                className="w-64 mx-auto mt-2 text-xl btn--primary"
                type="submit">
                Sign Up
            </button>

            <Link className="mx-auto mt-2 text-blue--100" to="/login">I already have an account</Link>
        </form>
    );
};