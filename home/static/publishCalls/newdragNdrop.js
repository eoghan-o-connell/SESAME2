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
var call_id;
var editing_mode_tag;
var editing_mode;
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

    toggleButton = document.getElementById('collapsingButton');
    fname = document.getElementById('fname');
    sname = document.getElementById('sname');
    date = document.getElementById('date');
    tag = document.getElementById('tag');
    title = document.getElementById('title');
    description = document.getElementById('description');
    grant = document.getElementById('grant');
    call_id = document.getElementById('_call_id');
    editing_mode_tag = document.getElementById('updating_call');
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

    editing_mode = editing_mode_tag.value;
    console.log("Current editing mode  -- > " + editing_mode);

    // toggleButton.click();

    elements = [fname,sname,title,grant];

    for (var i=0; i<elements.length; i++){
        if (elements[i].value!=""){
            let element = elements[i];
            element.classList.remove('is-invalid');
            element.classList.add('is-valid');
        }
    }

    form = document.getElementById('checkForm');
    form.addEventListener('submit',edit_submission,false);

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
    formData.append("editing_mode_tag",editing_mode);
    formData.append("_call_id",call_id.value);
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


function uploadFiles(ev){

    //trying to send the data without a file ( no updates ), should try and grab previous FILES
    //and repopulae the dropzone instead
    if (editing_mode == "True" && dz.getQueuedFiles().length == 0){
        console.log("WTF");
        console.log("Hmm");
        console.log(ev);
        form.submit();
        console.log("after");
    }
    else{
        if (form.checkValidity()){
          if (dz.getQueuedFiles().length > 0){
            captureFiles = dz.getQueuedFiles();
            dz.processQueue();
          }
        }
    }
  }

function edit_submission(ev){
    ev.preventDefault();
    uploadFiles(ev);
}
