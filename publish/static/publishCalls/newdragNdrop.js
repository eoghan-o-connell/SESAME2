window.onload = setup();

var dz;
var progressbar;

var fname;
var sname;
var date;
var tag;

var previousFname="";
var previousLname="";
var previous;
var element;
// var fnamePrevBool;

function setup(){
    Dropzone.autoDiscover = false;
    progressbar = document.getElementById('progress');
    fname = document.getElementById('fname');
    sname = document.getElementById('sname');
    date = document.getElementById('date');
    tag = document.getElementById('tag');
    var csrftoken = Cookies.get('csrftoken');
    console.log(csrftoken);

    fname.addEventListener("input",checkValidName,false);
    sname.addEventListener("input",checkValidName,false);

    var uploadButton = document.getElementById("btn");
    uploadButton.addEventListener("click",uploadFiles,false);
    if (document.getElementById("dropbox")){
        dz = new Dropzone("div#dropbox", {
        uploadMultiple: true,
        paramName: "file",
        maxFilesize: 5,
        maxFiles: 3,
        parallelUploads: 3,
        autoProcessQueue: false,
        acceptedFiles: "application/pdf" ,
        headers: { "X-CSRFToken": csrftoken   // < here
            // state:"inactive"
          },
        // url: "../python/fileReceiver.py",
         url: "/publish/",
        init: function() {
            this.on("totaluploadprogress",uploadInformation);
            this.on("addedfile", fileAdded);
            this.on("success",success);
            this.on("sendingmultiple",sndMul);
            // this.on("complete",function(file){
            //     dz.removeFile(file);
            // })
        }
    });
  }
}

function checkValidName(e){
    let fname_bool = e.srcElement.id == "fname";
    let val = e.srcElement.value;

    if (fname_bool){
        console.log(1);
        previous = previousFname;
        element = fname;
    }else{
        console.log(2);
        previous = previousLname;
        console.log(previous + "~");
        element = sname;
    }

    if (val == ""){
        element.classList.remove('is-valid');
        element.classList.add('is-invalid');
    }else if (val!="" && previous==""){
        element.classList.remove('is-invalid');
        element.classList.add('is-valid');
    }

    if (fname_bool){
      previousFname = val;
    }else {
      previousLname = val;
    }

    fnamePrevBool = fname_bool;
    previous = val;

}

function sndMul(file,xhr,formData){
    // console.log("Grabbing form data..");
    // console.log("Fname: " + fname.value + " Sname: " + sname.value);
    // console.log("date: " + date.value);
    // console.log("Tag chosen  = " + tag.value);
    // console.log("sending multiple files and adding additional dom uploadInformation");
    formData.append("fname",fname.value);
    formData.append("sname",sname.value);
    formData.append("date",date.value);
    formData.append("tag",tag.value);
}

function success(ev){
    console.log("success!");
    // progressbar.style.width= 0 + "%";

}

function uploadInformation(progress,totalBytes,bytesSent){//, progress, bytesSent){
    // console.log("updating upload info!: " + totalBytes + " bytes sent: " + bytesSent + " prog " + progress);
    // console.log(bytesSent + "    " + progress);
    if (bytesSent > 0){
        progressbar.style.width= progress + "%";
        progressbar.innerHTML = progress + "%";
    }
}

function fileAdded(file){
    file.previewElement.addEventListener("click",function(){
        // console.log("Before removal:" + dz.getQueuedFiles());
        dz.removeFile(file);
        // console.log("After removal:" + dz.getQueuedFiles());
    });
}

function uploadFiles(ev){
    // console.log("dz.getQueuedFiles()")
    if (dz.getQueuedFiles().length > 0){
        dz.processQueue();
        //dz.removeAllFiles() ;
    }
}
