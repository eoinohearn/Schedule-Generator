let classEl = document.getElementsByClassName('class');
let i;

const validBtn = document.querySelector('.userBtn')

document.addEventListener('dragstart', (event)=>{
    semesterEls = document.querySelectorAll('.semester')
    semesterEls.forEach(semester => {
        semester.classList.add('dropzone')
    });
    }
)

document.addEventListener('dragend', (event)=>{
    semesterEls = document.querySelectorAll('.semester')
    semesterEls.forEach(semester => {
        semester.classList.remove('dropzone')
    });
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






function validScheduleCheck(){
    const createdSchedule = {};
    const semesterList = document.querySelectorAll('.semester');

    semesterList.forEach(semester => {
        let courseList = semester.children;
        const courseNameList = [];
        //starts at 1 because the 'semester i' is a div within the semester div and so starting at one skips this
        for (let course = 1; course < courseList.length; course++){
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
    if (!ev.target.classList.contains('semester')){return}
    ev.preventDefault();
    // ev.target.classList.add('dropzone')
}

function drag(ev){
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev){
    ev.preventDefault();
    let data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}