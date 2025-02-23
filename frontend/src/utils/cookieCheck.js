export default function cookieCheck(cookie) {
    if (document.cookie.split("; ").find((row) => row.startsWith(cookie))) {
        return true;
    };
    return false;
};