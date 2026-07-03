document.addEventListener("DOMContentLoaded", function () {
    console.log("Welcome to StudyMate AI!");
});

if (window.location.pathname.includes("index.html") ||
    window.location.pathname.endsWith("/")) {
    alert("Welcome to StudyMate AI!");
}

function welcome() {
    alert("Welcome to StudyMate AI!");
}function darkMode() {
    document.body.classList.toggle("dark");
}


function validateForm(){

    let name=document.getElementById("name").value;
    let email=document.getElementById("email").value;
    let message=document.getElementById("message").value;

    if(name=="" || email=="" || message==""){
        alert("Please fill all fields.");
        return false;
    }

    alert("Message Sent Successfully!");
    return true;
}



function searchNotes(){

    let input = document.getElementById("searchInput");
    let filter = input.value.toUpperCase();

    let table = document.querySelector(".notes table");
    let tr = table.getElementsByTagName("tr");

    for(let i=1;i<tr.length;i++){

        let td = tr[i].getElementsByTagName("td")[0];

        if(td){

            let txt = td.textContent;

            if(txt.toUpperCase().indexOf(filter)>-1){
                tr[i].style.display="";
            }
            else{
                tr[i].style.display="none";
            }

        }

    }

}

window.addEventListener("load", function () {

    let loader = document.getElementById("loader");
    let content = document.getElementById("content");

    setTimeout(function () {

        if (loader) loader.style.display = "none";
        if (content) content.style.display = "block";

    }, 1500);

});


window.onload = function () {

    
    if (
        window.location.pathname.includes("/dashboard") &&
        !sessionStorage.getItem("dashboardReminderShown")
    ) {

        let hour = new Date().getHours();
        let reminder = "";

        if (hour >= 5 && hour < 9) {
            reminder = "🌅 Good Morning!\n\nStart your day with 30 minutes of study.";
        }
        else if (hour >= 9 && hour < 12) {
            reminder = "📚 Morning Study Time!\n\nRevise yesterday's topics.";
        }
        else if (hour >= 12 && hour < 16) {
            reminder = "☀️ Afternoon Reminder!\n\nComplete today's assignments.";
        }
        else if (hour >= 16 && hour < 19) {
            reminder = "📖 Evening Study Time!\n\nPractice coding or solve quizzes.";
        }
        else if (hour >= 19 && hour < 22) {
            reminder = "🌙 Night Revision!\n\nReview your notes before sleeping.";
        }
        else {
            reminder = "😴 It's getting late!\n\nTake rest and continue tomorrow.";
        }

        setTimeout(function () {
            alert(reminder);
            sessionStorage.setItem("dashboardReminderShown", "true");
        }, 2000);
    }

};

