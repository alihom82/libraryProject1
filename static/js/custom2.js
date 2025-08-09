function fillPage(page) {
    console.log("Change");
    $('#page').val(page);
    $('#filter_form').submit();
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("borrowForm");
    form.addEventListener("submit", function(e) {
        e.preventDefault();

        fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": form.querySelector('[name=csrfmiddlewaretoken]').value,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams(new FormData(form))
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("resultMessage").innerText = data.message;
        })
        .catch(error => {
            document.getElementById("resultMessage").innerText = "خطایی رخ داد.";
            console.error("Fetch error:", error);
        });
    });
});
console.log("test")
