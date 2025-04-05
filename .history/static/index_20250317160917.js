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
    user_name: document.getElementById("user_name").value,
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
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
function signin(event) {
  event.preventDefault(); // Sayfanın yeniden yüklenmesini engeller.

  const formData = {
    useremail: document.getElementById("useremail").value,
    userpass: document.getElementById("userpassword").value,
  };

  fetch("/signin", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert("Login failed: " + data.error);
      }
      else { 
         window.location.href = '/main'
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
