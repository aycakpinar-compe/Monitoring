function resmidegistir() {
  const select = document.getElementById("selectid");
  const videoElement = document.getElementById("resimid");
  const videoSource = document.getElementById("videosource");
  const selectedVideo = select.id;
  const sessionDate = new Date().toISOString();

  if (selectedVideo) {
    videoSource.setAttribute("src", selectedVideo);
    videoElement.load(); // This line is missing in your code

    // Video yükleme islemi tamamlandıgında fetchi calistirmak
    videoElement.onloadeddata = function () {
      // Video yüklendikten sonra fetch isteği yap
      fetch("/history", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          pickedsong: selectedVideo,
          session_date: sessionDate,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Response:", data);
        })
        .catch((error) => console.error("Error:", error));
    };
  } else {
    videoElement.pause();
    videoSource.setAttribute("src", "");
  }
} // This closing brace was missing

function signup(e) {
  e.preventDefault();

  // Get form data
  const formData = {
    username: document.getElementById("username").value,
    useremail: document.getElementById("useremail").value,
    userpass: document.getElementById("userpass").value,
  };

  // Basic validation
  if (!formData.username || !formData.useremail || !formData.userpass) {
    alert("Please fill in all fields");
    return;
  }

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(formData.useremail)) {
    alert("Please enter a valid email address");
    return;
  }

  // Password strength check
  if (formData.userpass.length < 6) {
    alert("Password should be at least 6 characters long");
    return;
  }

  fetch("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      return response.json().then((data) => {
        if (!response.ok) {
          throw new Error(data.error || "Server responded with an error");
        }
        return data;
      });
    })
    .then((data) => {
      if (data.success) {
        // Since we now log in the user automatically after signup in the backend,
        // we can redirect directly to the main page
        window.location.href = "/main";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert(error.message || "An error occurred during registration.");
    });
}

// Function to handle signin
function signin(event) {
  event.preventDefault();

  const formData = {
    useremail: document.getElementById("useremail").value,
    userpass: document.getElementById("userpass").value,
  };

  // Basic validation
  if (!formData.useremail || !formData.userpass) {
    alert("Please enter both email and password");
    return;
  }

  fetch("/signin", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      return response.json().then((data) => {
        if (!response.ok) {
          throw new Error(data.error || "Authentication failed");
        }
        return data;
      });
    })
    .then((data) => {
      if (data.success) {
        window.location.href = "/main";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert(error.message || "An error occurred during sign in.");
    });
}

// Function to logout
function logout() {
  fetch("/logout")
    .then(() => {
      window.location.href = "/";
    })
    .catch((error) => {
      console.error("Logout error:", error);
    });
}

// Function to check if user is authenticated
function checkAuthentication() {
  fetch("/check-auth")
    .then((response) => response.json())
    .then((data) => {
      if (!data.authenticated) {
        window.location.href = "/";
      }
    })
    .catch((error) => {
      console.error("Authentication check failed:", error);
      window.location.href = "/";
    });
}

// Handle back button and page refresh issues
function setupAuthChecks() {
  // Check if we're on a protected page (not login or signup)
  const currentPath = window.location.pathname;
  if (currentPath !== "/" && currentPath !== "/signup") {
    checkAuthentication();
  }

  // For login and signup pages - prevent going back to them if logged in
  if (currentPath === "/" || currentPath === "/signup") {
    fetch("/check-auth")
      .then((response) => response.json())
      .then((data) => {
        if (data.authenticated) {
          window.location.href = "/main";
        }
      })
      .catch((error) => {
        console.error("Auth check error:", error);
      });
  }
}

// Handle page visibility changes (for back/forward browser navigation)
document.addEventListener("visibilitychange", function () {
  if (document.visibilityState === "visible") {
    setupAuthChecks();
  }
});

// Add event listener for page loads including back button navigation
window.addEventListener("pageshow", function (event) {
  // Check if page is loaded from cache (back/forward navigation)
  if (event.persisted) {
    setupAuthChecks();
  }
});

// Initialize authentication checks when DOM is loaded
document.addEventListener("DOMContentLoaded", setupAuthChecks);

// Add event listener for history changes
window.addEventListener("popstate", setupAuthChecks);
