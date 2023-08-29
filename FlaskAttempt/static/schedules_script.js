const btn = document.querySelector('.save_Schedule');

function saveSchedules(){

    var radios = document.querySelectorAll("input[type=radio]");
    var favScheduleIndex = null;
    for (let i = 0; i< radios.length; i++){
        if(radios[i].checked){
            favScheduleIndex = i
        }
    }

    var tableListEl = document.querySelector('.all-tables');
    var childList = tableListEl.children;
    var favScheduleList = childList[favScheduleIndex].children; // this contains both the table and the radio input
    var favSchedule = favScheduleList[0].outerHTML

    return favSchedule
}


btn.addEventListener('click', ()=>{

        let favSchedule = saveSchedules();

        fetch('/favSchedule', {
            headers : {
                'Content-Type' : 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(favSchedule)
        })
        .then(function(response){
            if(response.ok){
                response.json()
                .then(function(response){
                    console.log(response);
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
);
