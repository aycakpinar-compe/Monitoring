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
