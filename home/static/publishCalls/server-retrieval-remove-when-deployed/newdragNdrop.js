window.onload = setup();

var dz;
var uploader;
var counter = 0;

function setup(){
    Dropzone.autoDiscover = false;
    var uploadButton = document.querySelector("button");
    uploadButton.addEventListener("click",uploadFiles,false);
    uploader = document.getElementById("upload");
    if (document.getElementById("dropbox")){
        dz = new Dropzone("div#dropbox", {
        //uploadMultiple: true,
        paramName: "file",
        maxFilesize: 5,
        maxFiles: 3,
        parallelUploads: 3,
        autoProcessQueue: false,
        acceptedFiles: "application/pdf" ,
        url: "../python/fileReceiver.py",
        init: function() {
            this.on("totaluploadprogress",uploadInformation);
            this.on("addedfile", fileAdded);
            this.on("success",success);
            this.on("sending",sndMul);
        }
    });
  }
}

function sndMul(file,xhr,formData){
    //this makes it compatible with django, as all we need to do is add this
    //script whatever the name is in the html, this also means we can grab elements from
    //the django page and upload them as formData to the server!
    console.log("sending multiple files and adding additional dom uploadInformation");
}


function success(ev){
    uploader.innerHTML = "Upload complete!";
}

function uploadInformation(progress,totalBytes,bytesSent){//, progress, bytesSent){
    uploader.innerHTML = "Upload beginning for all files: progress = " + progress + "%";
}

function fileAdded(ev){
    counter +=1;
    uploader.innerHTML = "Upload.. files added = " + counter;
}

function uploadFiles(ev){
    console.log("beginning upload....");
    dz.processQueue();
}
