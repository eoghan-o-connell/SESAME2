window.onload = setup();

var dz;
var progressbar;

var csrftoken;
var uploadButton;
var call_id;
var editing_mode;

function setup(){
    Dropzone.autoDiscover = false;
    call_id = document.getElementById('call_id');
    progressbar = document.getElementById('progress');
    uploadButton = document.getElementById("btn");
    csrftoken = Cookies.get('csrftoken');
    uploadButton.addEventListener("click",uploadFiles,false);

    form = document.getElementById('checkForm');

    if (document.getElementById("dropbox")){
        dz = new Dropzone("div#dropbox", {
        uploadMultiple: true,
        paramName: "file",
        maxFilesize: 5,
        maxFiles: 3,
        parallelUploads: 3,
        addRemoveLinks: true,
        autoProcessQueue: false,
        acceptedFiles: "application/pdf" ,
        headers: { "X-CSRFToken": csrftoken
          },
        url: "/home/call_view",
        init: function() {
            this.on("totaluploadprogress",uploadInformation);
            this.on("successmultiple",success);
            this.on("sendingmultiple",sndMul);
            this.on("maxfilesexceeded", function(file) { this.removeFile(file); });
        }
    });
  }
}

function checkSummary(){
  console.log("click");
    if (summary.style.visibility=="visible"){
        summary.style.visibility="hidden";
    }
}

function checkValidName(e){

    let element = elements[dict[e.srcElement.id]];
    let val = e.srcElement.value;
    if (val == ""){
        element.classList.remove('is-valid');
        element.classList.add('is-invalid');
    }else{
        element.classList.remove('is-invalid');
        element.classList.add('is-valid');
    }
}

 function sndMul(file,xhr,formData){
       var urlParams = new URLSearchParams(window.location.search);
       var myParam = urlParams.get('call_id');
       console.log("GRABBED PARAM = " + myParam);
       formData.append("call_id",call_id.value);
}

function success(ev){
    console.log("success!");
    dz.removeAllFiles();
    console.log("removed all files");
    progressbar.style.width = 0 + "%";
    progressbar.innerHTML = 0 + "%";
}

function uploadInformation(progress,totalBytes,bytesSent){//, progress, bytesSent){
    if (bytesSent > 0){
        progressbar.style.width= progress + "%";
        progressbar.innerHTML = progress + "%";
    }
}


function uploadFiles(ev){
      if (dz.getQueuedFiles().length > 0){
        captureFiles = dz.getQueuedFiles();
        dz.processQueue();
      }
}
