import { useState, useEffect } from "react";
import io from "socket.io-client";

export default function useWebSocket(url, handleData) {
    const [socket, setSocket] = useState(null);

    useEffect(() => {
        const socketClient = io(url);

        socketClient.on('connect', () => {
            console.log('Connected to server')
        });

        socketClient.on('disconnect', () => {
            console.log('Disconnected from server')
        });

        socketClient.on('data', (data) => {
            handleData(data);
        });

        setSocket(socketClient);

        return () => {
            socketClient.close();
        };
    }, []);

    return socket;
};