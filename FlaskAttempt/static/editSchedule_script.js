let classEl = document.getElementsByClassName('class');
let i;
let semesterElements = document.getElementsByClassName('semester');
let popup = document.querySelector('.popup-addClass');
let currSemesterId;

const validBtn = document.querySelector('.userBtn')

document.addEventListener('dragstart', (event)=>{
    semesterEls = document.querySelectorAll('.semester');
    semesterEls.forEach(semester => {
        semester.classList.add('dropzone')
    });
    let deleteBtn = document.querySelectorAll('.deleteBtn');
    deleteBtn.forEach(btn => {
        btn.style.display = 'flex';
    })
    }
)

document.addEventListener('dragend', (event)=>{
    semesterEls = document.querySelectorAll('.semester')
    semesterEls.forEach(semester => {
        semester.classList.remove('dropzone')
    });
    let deleteBtn = document.querySelectorAll('.deleteBtn');
    deleteBtn.forEach(btn => {
        btn.style.display = 'none';
    })
})

for (i=0; i< classEl.length; i++){
    classEl[i].addEventListener("click", 
    function() {
        let content = this.nextElementSibling;
        if(content.style.display == 'block'){
            content.style.display = 'none';
        } else{
            content.style.display = 'block';
        }
    });
}

function displayClassContent(elem){
    let content = elem.nextElementSibling;
    if(content.style.display == 'block'){
        content.style.display = 'none';
    } else{
        content.style.display = 'block';
    }
}






function validScheduleCheck(){
    const createdSchedule = {};
    const semesterList = document.querySelectorAll('.semester');

    semesterList.forEach(semester => {
        let courseList = semester.children;
        const courseNameList = [];
        //starts at 1 because the 'semester i' is a div within the semester div and so starting at one skips this
        //To '-1' as well because of the 'add class' button at the end
        for (let course = 1; course < courseList.length-1; course++){
            courseNameList.push(courseList[course].id);
        }
        createdSchedule[semester.id] = courseNameList;
    })

    return createdSchedule;
}



validBtn.addEventListener('click', ()=>{
    let validSchedule = validScheduleCheck();

    fetch('/validSchedule', {
        headers : {
            'Content-Type' : 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(validSchedule)
    })
    .then(function(response){
        if(response.ok){
            response.json()
            .then(function(response){
                alert(response)
            });
        }
        else{
            throw Error('Uh Oh')
        }
    })
    .catch(function(error){
        console.log(error);
    });


})


function allowDrop(ev){
    if (!ev.target.classList.contains('semester') && !ev.target.classList.contains('deleteBtn')){return}
    ev.preventDefault();
    // ev.target.classList.add('dropzone')
}

function drag(ev){
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev){
    if(ev.target.classList.contains('semester')){
        ev.preventDefault();
        let addBtn = ev.target.lastElementChild;
        let data = ev.dataTransfer.getData("text");
        ev.target.insertBefore(document.getElementById(data), addBtn)
        // ev.target.appendChild(document.getElementById(data));
    }
    if(ev.target.classList.contains('deleteBtn')){
        ev.preventDefault();
        let data = ev.dataTransfer.getData("text");
        ev.target.appendChild(document.getElementById(data));
        ev.target.removeChild(document.getElementById(data));
    }

    semesterEls = document.querySelectorAll('.semester')
    semesterEls.forEach(semester => {
        semester.classList.remove('dropzone')
    });
    let deleteBtn = document.querySelectorAll('.deleteBtn');
    deleteBtn.forEach(btn => {
        btn.style.display = 'none';
    })
}

function addNewClassPopup(el){
    currSemesterId = el.parentElement.id
    popup.classList.remove("hidden");
}

function removeNewClassPopup(){
    popup.classList.add("hidden");
}

function addNewClass(){
    let addSem = document.getElementById(currSemesterId);
    let checkboxes = document.querySelectorAll("input[type = checkbox]");
    let checkedList = [];
    for(let j = 0; j < checkboxes.length; j++){
        if(checkboxes[j].checked){
            checkedList.push(checkboxes[j].value)
        }
    }

    fetch('/addNewClassSchedule', {
        headers : {
            'Content-Type' : 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(checkedList)
    })
    .then(function(response){
        if(response.ok){
            response.json()
            .then(function(response){
                for(let j = 0; j< response.length;j++){
                    let newClass = document.createElement("div");
                    newClass.id = response[j].name;
                    newClass.draggable = 'true';
                    newClass.setAttribute("ondragstart",'drag(event)');
                    let addBtn = addSem.lastElementChild;
                    addSem.insertBefore(newClass, addBtn)

                    let newClassBtn = document.createElement("button");
                    newClassBtn.type = "button";
                    newClassBtn.classList.add("class")
                    newClassBtn.innerText = response[j].name;
                    newClassBtn.setAttribute("onclick", "displayClassContent(this)")
                    newClass.appendChild(newClassBtn);

                    let newClassContent = document.createElement("div");
                    newClassContent.classList.add("class-content");
                    newClass.appendChild(newClassContent);

                    let newCredits = document.createElement("p");
                    newCredits.innerText = "Credits: " + response[j].credits;

                    let newPre = document.createElement("p");
                    newPre.innerText = "Prerequisites: \n" + response[j].preReq;

                    let newCoreq = document.createElement("p");
                    newCoreq.innerText = "Corequisites: \n" +response[j].coReq;

                    newClassContent.appendChild(newCredits);
                    newClassContent.appendChild(newPre);
                    newClassContent.appendChild(newCoreq);

                }
                removeNewClassPopup();
                console.log("woohoo!!!!!!!!!")
            });
        }
        else{
            throw Error('Uh Oh')
        }
    })
    .catch(function(error){
        console.log(error);
    });
    

}