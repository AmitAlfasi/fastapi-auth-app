const API_BASE_URL = window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "http://127.0.0.1:8000";

/* 
    Login Form Handler
    This script handles the login form submission and authentication process.
    Features:
    - Form submission handling
    - API communication with backend
    - Error handling and display
    - Token storage in localStorage
    - Redirect to dashboard on success
*/

const publicPages = ["index.html", "register.html", "verify.html"];
const currentPage = window.location.pathname.split("/").pop();

if (publicPages.includes(currentPage)) {
    (async function checkLoggedIn() {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Accept": "application/json"
                }
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem("access_token", data.access_token);
                window.location.href = "dashboard.html";  // ✅ Redirect to home
            }
        } catch (err) {
            console.warn("Not logged in, staying on page.");
        }
    })();
}

async function refreshAccessToken() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) return false;

        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        return true;
    } catch (err) {
        console.error("Failed to refresh token:", err);
        return false;
    }
}

async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem("access_token");

    const defaultHeaders = {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
        ...options.headers,
    };

    const response = await fetch(url, {
        ...options,
        headers: defaultHeaders
    });

    if (response.status === 401 || response.status === 403) {
        const refreshed = await refreshAccessToken();
        if (!refreshed) {
            window.location.href = "index.html";
            return null;
        }

        const newToken = localStorage.getItem("access_token");
        return await fetch(url, {
            ...options,
            headers: {
                ...defaultHeaders,
                Authorization: `Bearer ${newToken}`
            }
        });
    }

    return response;
}
