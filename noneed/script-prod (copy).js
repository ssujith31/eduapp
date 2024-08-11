let isRecording = false;
//let socket;
let microphone;

//const socket_port = 5001;
//socket = io(
//  "http://" + window.location.hostname + ":" + socket_port.toString()
//);

socket.on("transcription_update", (data) => {
  alert(data);
  //document.getElementById("captions").innerHTML = data.transcription;
});

socket.on("questionasked", (data) => {
  //alert(data);
  //document.getElementById("captions").innerHTML = data.transcription;
  document.getElementById("result").innerHTML=data['question'];
  document.getElementById("q1").style.display="block";
  document.getElementById("status1").innerHTML="Generating Voice";
  document.getElementById("s1").style.display="block";
  document.getElementById("loadingimgvoice").style.display="block";

});

socket.on("voicestart1", (data) => {
  //alert(data);
  //document.getElementById("captions").innerHTML = data.transcription;
  //document.getElementById("result").innerHTML=data['question'];
  //document.getElementById("q1").style.display="block";
  //document.getElementById("status1").innerHTML="Generating Voice";
  document.getElementById("s1").style.display="none";
  document.getElementById("loadingimgvoice").style.display="none";
  document.getElementById("a1").style.display="block";
  document.getElementById("answer").innerHTML=data['answer'];
  document.getElementById("speak").style.display="block";
  //document.getElementById("loadingimgvoice").style.display="block";
});

async function getMicrophone() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    return new MediaRecorder(stream, { mimeType: "audio/webm" });
  } catch (error) {
    console.error("Error accessing microphone:", error);
    throw error;
  }
}

async function openMicrophone(microphone, socket) {
  return new Promise((resolve) => {
    microphone.onstart = () => {
      console.log("Client: Microphone opened");
      //document.body.classList.add("recording");
      resolve();
    };
    microphone.ondataavailable = async (event) => {
      console.log("client: microphone data received");
      if (event.data.size > 0) {
        socket.emit("audio_stream", event.data);
      }
    };
    microphone.start(1000);
  });
}

async function startRecording() {
  isRecording = true;
  microphone = await getMicrophone();
  console.log("Client: Waiting to open microphone");
  await openMicrophone(microphone, socket);
}

async function stopRecording() {
  if (isRecording === true) {
    microphone.stop();
    microphone.stream.getTracks().forEach((track) => track.stop()); // Stop all tracks
    socket.emit("toggle_transcription", { action: "stop" });
    microphone = null;
    isRecording = false;
    console.log("Client: Microphone closed");
    //document.body.classList.remove("recording");
  }
}
/*
document.addEventListener("DOMContentLoaded", () => {
  const recordButton = document.getElementById("record");

  recordButton.addEventListener("click", () => {
    if (!isRecording) {
      socket.emit("toggle_transcription", { action: "start" });
      startRecording().catch((error) =>
        console.error("Error starting recording:", error)
      );
    } else {
      stopRecording().catch((error) =>
        console.error("Error stopping recording:", error)
      );
    }
  });
});
*/