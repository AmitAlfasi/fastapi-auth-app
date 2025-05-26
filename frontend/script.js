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

// frontend/script.js
document.getElementById("login-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Login failed");
        }

        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        window.location.href = "dashboard.html";
    } catch (err) {
        document.getElementById("error-message").textContent = err.message;
    }
});



// script.js

async function refreshAccessToken() {
    try {
        // Only include credentials for the refresh token request
        const response = await fetch("http://localhost:8000/auth/refresh", {
            method: "POST",
            credentials: "include",  // Only here we send the refresh token cookie
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

    // First try without credentials
    const response = await fetch(url, {
        ...options,
        headers: defaultHeaders
    });

    if (response.status === 401 || response.status === 403) {
        // Only include credentials when refreshing token
        const refreshed = await refreshAccessToken();
        if (!refreshed) {
            window.location.href = "index.html";
            return null;
        }

        const newToken = localStorage.getItem("access_token");
        // Second request with new token, still without credentials
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