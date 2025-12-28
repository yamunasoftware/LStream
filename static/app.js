/* UI SETUP */

//On Startup:
window.onload = async function () {
  //Find the Videos:
  document.getElementById('videoContainer').style.display = "none";
  await findVideos();
}

//Key Event Listener:
window.addEventListener("keydown", function (e) {
  //Checks the Case:
  if (e.key == "Enter") {
    //Runs the Play:
    playVideo();
  }
}, true);

//Alert Function:
function showAlert(message) {
  //Error Alert:
  alert(message + "\nPlease Try Again Later");
  window.location.reload();
}

//Error Function:
function showError(message) {
  //Error Alert:
  document.getElementById('errorMessage').innerHTML = message;
}

/* VIDEO FUNCTIONS */

//Submit Button Function:
async function addVideo() {
  //Gets the URL and File:
  var url = document.getElementById('videoURL').value;
  var name = document.getElementById('videoName').value;

  //Checks the Case:
  if (url != "" && name != "") {
    //Sends the Video Request:
    const response = await fetch('/add_video', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'url': url,
        'name': name
      })
    });

    //Checks the Status:
    if (response.status == 200) {
      //Gets Videos:
      await findVideos();
    }

    else {
      //Alerts User:
      showError(await response.text());
    }
  }
}

//Get Videos Function:
async function getVideos() {
  //Fetches the Video Filenames:
  const response = await fetch('/get_videos');
  if (response.status == 200) {
    const files = await response.json();
    pruneCache(files);
    return files;
  }

  else {
    //Alerts User:
    showError(await response.text());
    return [];
  }
}

//Play Video Function:
function playVideo(file) {
  //Gets the Video Elements:
  var video = document.getElementById('videoPlayer');
  var source = document.createElement('source');
  document.getElementById('selectionContainer').style.display = "none";
  document.getElementById('videoContainer').style.display = "block";

  //Video Error Event Listener:
  video.addEventListener("error", function (e) {
    //Alerts User:
    showAlert("An Error Occurred or Server is Busy");
  }, true);

  //Sets the Video Attributes:
  source.setAttribute('src', '/' + file);
  source.setAttribute('type', 'video/mp4');

  //Plays the Video:
  video.appendChild(source);
  video.setAttribute("controls", "controls");
  video.requestFullscreen().then((event) => {
    //Video FullScreen Event Listener:
    video.addEventListener("fullscreenchange", function (e) {
      //Checks the Case:
      if (document.fullscreenElement == null) {
        //Reloads the Page:
        window.location.reload();
      }
    });
    
    //Plays the Video:
    video.play();
  });

  //Sets the Scrubbing:
  autoScrub(file);
  setAutoScrub(file);
}

//Find Videos Function:
async function findVideos() {
  //DOM Variables:
  var videoDOM = "";
  var videos = await getVideos();

  //Loops through Array:
  for (var turns = 0; turns < videos.length; turns++) {
    //Adds an Element:
    videoDOM += 
      "<div> <p class='card' onclick='playVideo(" + JSON.stringify(videos[turns]) + ");'>" + videos[turns];

    //Checks the Case:
    if (localStorage.getItem(videos[turns]) != null) {
      //Time Array Variables:
      var array = JSON.parse(localStorage.getItem(videos[turns]));
      var remaining = array[1] - array[0];

      //Time Calculations:
      var hours = Math.floor(remaining / 3600.0);
      var minutes = Math.floor((remaining / 60.0) - (hours * 60.0));
      var seconds = Math.floor(remaining - (hours * 3600.0) - (minutes * 60.0));

      //Checks the Case:
      if (remaining != 0) {
        //Adds and Element:
        videoDOM += "<br /> <br />" + 
          hours + "h " +  minutes + "m " + seconds + "s";
      }

      else {
        //Deletes the Cached Item:
        localStorage.removeItem(videos[turns]);
      }
    }

    //Adds and Element:
    videoDOM += "</p> </div>";
  }

  //Sets the Inner HTML:
  document.getElementById('selectionContainer').innerHTML = videoDOM;
}

//Prune Cache Function:
function pruneCache(videoList) {
  //Loops through Cache:
  for (var i = 0; i < localStorage.length; i++) {
    //Gets the Key:
    var key = localStorage.key(i);

    //Checks the Case:
    if (!videoList.includes(key)) {
      //Removes the Item:
      localStorage.removeItem(key);
    }
  }
}

/* SCRUB FUNCTIONS */

//Automatic Scrub Function:
function autoScrub(file) {
  //Gets the Scrub Value:
  var video = document.getElementById('videoPlayer');
  
  //Checks the Case:
  if (localStorage.getItem(file) != null) {
    //Scrubs to the Value:
    var array = JSON.parse(localStorage.getItem(file));
    video.currentTime = array[0];
  }
}

//Set Automatic Scrub Function:
function setAutoScrub(file) {
  //Video Elements:
  var video = document.getElementById('videoPlayer');
  
  //Scrub Interval:
  setInterval(function () {
    //Sets the Automatic Scrub Value:
    var array = [video.currentTime, video.duration];
    localStorage.setItem(file, JSON.stringify(array));
  }, 1000);
}