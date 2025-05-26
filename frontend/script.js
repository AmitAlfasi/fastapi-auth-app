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
