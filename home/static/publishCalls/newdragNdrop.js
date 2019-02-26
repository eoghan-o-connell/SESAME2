window.onload = setup();

var dz;
var progressbar;

//REMOVE BUTTON AND ACCEPT GET REQUEST .. spawn a link tag and re direct to same page


var fname;
var sname;
var date;
var tag;
var csrftoken;
var uploadButton;
var form;
var title;
var description;
var grant;
var captureFiles;
var toggleButton;
var summary;
var summaryHeading;

var dict = {
  "fname" : 0,
  "sname" : 1,
  "title" : 2,
  "grant" : 3
};

var elements;

var previousFname="";
var previousLname="";
var previous;
var element;
// var fnamePrevBool;

function setup(){
    Dropzone.autoDiscover = false;

    fname = document.getElementById('fname');
    sname = document.getElementById('sname');
    date = document.getElementById('date');
    tag = document.getElementById('tag');
    title = document.getElementById('title');
    description = document.getElementById('description');
    grant = document.getElementById('grant');
    toggleButton = document.getElementById('collapsingButton');
    summary = document.getElementById("summary");
    summaryHeading=document.getElementById('summaryHeading');

    progressbar = document.getElementById('progress');
    uploadButton = document.getElementById("btn");
    csrftoken = Cookies.get('csrftoken');

    fname.addEventListener("input",checkValidName,false);
    sname.addEventListener("input",checkValidName,false);
    title.addEventListener("input",checkValidName,false);
    grant.addEventListener("input",checkValidName,false);

    toggleButton.addEventListener("click",checkSummary,false);
    uploadButton.addEventListener("click",uploadFiles,false);

    toggleButton.click();

    elements = [fname,sname,title,grant];

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
        url: "/home/publish_call",
        init: function() {
            this.on("totaluploadprogress",uploadInformation);
            this.on("addedfile", fileAdded);
            this.on("successmultiple",success);
            this.on("sendingmultiple",sndMul);
            this.on("maxfilesexceeded", function(file) { this.removeFile(file); });
        }
    });
//        dz.createThumbnailFromUrl("pdf_thumbnail.webp","../pdf_thumbnail.webp");
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
    formData.append("fname",fname.value);
    formData.append("sname",sname.value);
    formData.append("date",date.value);
    formData.append("tag",tag.value);
    formData.append("title",title.value);
    formData.append("description",description.value);
    formData.append("grant",grant.value);
    console.log("**********" + tag.value);
}

function success(ev){
    console.log("success!");
    dz.removeAllFiles();
    console.log("removed all files");
    progressbar.style.width = 0 + "%";
    progressbar.innerHTML = 0 + "%";
    var s_title = document.getElementById('s_title');
    var s_desc =  document.getElementById('s_desc');
    var s_amount = document.getElementById('s_amount');
    var s_deadline  = document.getElementById('s_deadline');
    var s_call  = document.getElementById('s_call_pdf');

    s_title.innerHTML = title.value;
    s_desc.innerHTML = description.value;
    s_amount.innerHTML = grant.value;
    s_deadline.innerHTML = date.value;
    let string = "";
    console.log(captureFiles);
    for (var i=0; i<captureFiles.length; i++){
       string += captureFiles[i].name + " ";
    }
    s_call.innerHTML = string;
    summaryHeading.innerHTML="Thank you for submitting "+ fname.value  +"!";

    form.reset();
    toggleButton.click();
    summary.style.visibility="visible";
}

function uploadInformation(progress,totalBytes,bytesSent){//, progress, bytesSent){
    if (bytesSent > 0){
        progressbar.style.width= progress + "%";
        progressbar.innerHTML = progress + "%";
    }
}

function fileAdded(file){
  // file.previewElement.querySelector("img").src = newname;

    // You could of course generate another image yourself here,
    // and set it as a data url.
 }

function uploadFiles(ev){
    console.log("pressed");
    if (form.checkValidity()){
      if (dz.getQueuedFiles().length > 0){
        console.log("sending")
        captureFiles = dz.getQueuedFiles();
        summaryGeneration();
        dz.processQueue();
      }
    }
    form.reportValidity();
}

function summaryGeneration(){

}
