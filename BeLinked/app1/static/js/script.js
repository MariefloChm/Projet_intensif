let today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();
let dateElements = document.getElementById("dates");
let monthYearElement = document.getElementById("monthYear");

document.addEventListener("DOMContentLoaded", function() {
    showCalendar(currentMonth, currentYear);
});
$(".notification-link").click(function() {
    const notificationId = $(this).data('notification-id');
    $.ajax({
        url: `/notification/read/${notificationId}/`,
        method: 'GET',
        success: function() {
            // Changer l'apparence de la notification une fois qu'elle a été lue
            $(`.notification-link[data-notification-id="${notificationId}"]`).removeClass("font-weight-bold");
        }
    });
});

$(".clear_all_notifications").click(function(e) {
    e.preventDefault();
    $.ajax({
        url: `/notification/clear_all/?timestamp=${new Date().getTime()}`,
        method: 'GET',
        success: function() {
            // Masquer toutes les notifications du menu déroulant
            $(".notification-link").remove();
            $(".dropdown-divider").remove();
            $(".clear_all_notifications").before('<a class="dropdown-item" href="#">Aucune notification</a>');
            // Mettre à jour le nombre de notifications à 0
            $(".fas.fa-bell").next().text("0");
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);
        }
    });
});

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    fetchSelectedDates();
});

function fetchSelectedDates() {
    fetch('/selected_dates') // Remplacez par le chemin correct
        .then(response => response.json())
        .then(data => {
            updateSelectedDatesUI(data.dates);
        });
}

function updateSelectedDatesUI(datesJson) {
    var dates = JSON.parse(datesJson);
    var listElement = document.getElementById('selectedDatesList');
    //listElement.innerHTML = ''; // Retirez cette ligne si vous ne voulez pas effacer les dates déjà présentes

    dates.forEach(function(dateObj) {
        var li = document.createElement('li');
        li.textContent = dateObj.fields.date; // Ajustez selon le format de votre JSON
        listElement.appendChild(li); // Ajoute à la fin de la liste
    });
}


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
