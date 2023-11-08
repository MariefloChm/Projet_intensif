let today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();
let dateElements = document.getElementById("dates");
let monthYearElement = document.getElementById("monthYear");

document.addEventListener("DOMContentLoaded", function() {
    showCalendar(currentMonth, currentYear);
});

document.getElementById("saveDatesBtn").addEventListener("click", function() {
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    var selectedDates = document.querySelectorAll(".selected");
    var datesToSave = [];
    var datesToDelete = [];
    for (var i = 0; i < selectedDates.length; i++) {
        // datesToSave.push(selectedDates[i].textContent);
        datesToSave.push(selectedDates[i].querySelector("span").textContent);
    }

    // Afficher les données avant l'envoi
    console.log({
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'dates': datesToSave,
        'delete_dates': datesToDelete
    });
    console.log(selectedDates);


    // Envoi des dates à l'application Django via AJAX
    $.ajax({
        url: saveURL,
        type: "POST",
        data: JSON.stringify({
            'csrfmiddlewaretoken': csrfToken,
            'dates': datesToSave
        }),
        success: function(response) {
            if(response.success) {
                alert(response.message);
            } else {
                alert("Erreur: " + response.message);
            }
        },
        error: function(error) {
            console.error("Erreur AJAX:", error);
        }
    });
});


function showCalendar(month, year) {
    let firstDay = (new Date(year, month)).getDay();
    let daysInMonth = 32 - new Date(year, month, 32).getDate();

    dateElements.innerHTML = "";
    monthYearElement.innerHTML = monthNames[month] + " " + year;

    for (let i = 0; i < 6; i++) {
        for (let j = 0; j < 7; j++) {
            let cell = document.createElement("div");

            if (i === 0 && j < firstDay || (i * 7) + j - firstDay + 1 > daysInMonth) {
                dateElements.appendChild(cell);
            } else {
                let cellDate = (i * 7) + j - firstDay + 1;
                cell.innerText = cellDate;
                cell.classList.add("date-cell");
                dateElements.appendChild(cell);

                cell.addEventListener('click', function() {
                    // Logic pour définir les disponibilités
                    this.classList.toggle("available");
                    let selectedDate = new Date(year, month, parseInt(this.innerText));

                    if (selectedDate >= today) {
                        fetch(disponibiliteURL, {
                            method: 'POST',
                            body: JSON.stringify({
                                date: selectedDate.toISOString().split('T')[0]
                            }),
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCookie('csrftoken')
                            }
                        })
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Erreur réseau ou côté serveur');
                                }
                                return response.json();
                            })
                            .then(data => {
                                if (data.status === "created") {
                                    this.style.backgroundColor = "green";
                                } else if (data.status === "deleted") {
                                    this.style.backgroundColor = "red";
                                }
                                console.log(data.status);
                            })
                            .catch(error => {
                                console.error("There was an error:", error);
                            });
                    }
                });
            }
        }
    }
}

function nextMonth() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear);
}

function prevMonth() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear);
}

function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

let monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
