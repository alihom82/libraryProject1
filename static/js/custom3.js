function fillPage(page) {
    let url = new URL(window.location.href);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}

// document.addEventListener("DOMContentLoaded", function () {
//     const form = document.getElementById("borrowForm");
//     form.addEventListener("submit", function(e) {
//         e.preventDefault();
//
//         fetch(form.action, {
//             method: "POST",
//             headers: {
//                 "X-CSRFToken": form.querySelector('[name=csrfmiddlewaretoken]').value,
//                 "Content-Type": "application/x-www-form-urlencoded"
//             },
//             body: new URLSearchParams(new FormData(form))
//         })
//         .then(response => response.json())
//         .then(data => {
//             document.getElementById("resultMessage").innerText = data.message;
//         })
//         .catch(error => {
//             document.getElementById("resultMessage").innerText = "خطایی رخ داد.";
//             console.error("Fetch error:", error);
//         });
//     });
// });
