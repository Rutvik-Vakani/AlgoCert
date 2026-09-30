document.getElementById("registerForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData();

    formData.append(
        "student_name",
        document.getElementById("studentName").value
    );

    formData.append(
        "course",
        document.getElementById("course").value
    );

    formData.append(
        "certificate",
        document.getElementById("certificate").files[0]
    );

    const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    document.getElementById("registerResult").innerHTML =
        `<pre>${JSON.stringify(result, null, 2)}</pre>`;
});


document.getElementById("verifyForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData();

    formData.append(
        "certificate_id",
        document.getElementById("certificateId").value
    );

    formData.append(
        "certificate",
        document.getElementById("verifyCertificate").files[0]
    );

    const response = await fetch("http://127.0.0.1:5000/verify", {
        method: "POST",
        body: formData
    });

    const result = await response.json();

    document.getElementById("verifyResult").innerHTML =
        `<pre>${JSON.stringify(result, null, 2)}</pre>`;
});