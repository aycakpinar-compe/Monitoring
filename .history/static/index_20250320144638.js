function resmidegistir() {
  const select = document.getElementById("selectid");
  const videoElement = document.getElementById("resimid");
  const videoSource = document.getElementById("videosource");
  const selectedVideo = select.value;

  if (selectedVideo) {
    videoSource.setAttribute("src", selectedVideo);
    videoElement.load();
  } else {
    videoElement.pause();
    videoSource.setAttribute("src", "");
  }
}
function signup(e) {
  e.preventDefault();
  const formData = {
    username: document.getElementById("username").value,
    useremail: document.getElementById("useremail").value,
    userpass: document.getElementById("userpass").value,
  };
  fetch("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Server responded with an error");
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        alert("Registration successful! Please sign in.");
        window.location.href = "/"; // Redirect to sign-in page
      } else if (data.error) {
        alert("Registration failed: " + data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred during registration.");
    });
}

function signin(event) {
  event.preventDefault();

  const formData = {
    useremail: document.getElementById("useremail").value,
    userpass: document.getElementById("userpass").value,
  };

  fetch("/signin", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      if (!response.ok) {
        if (response.status === 401) {
          return response.json().then((data) => {
            throw new Error(data.error || "Invalid email or password");
          });
        }
        throw new Error("Server error");
      }
      return response.json();
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
