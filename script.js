document.addEventListener("DOMContentLoaded", function() {
    // Your script here
    document.getElementById("plannerForm").addEventListener("submit", async function(event) {
        event.preventDefault();
        
        let dueDateInput = document.getElementById("dueDate").value;
        let localDate = new Date(dueDateInput);
        
        // Adjust for UTC
        let adjustedDate = new Date(localDate.getTime() - localDate.getTimezoneOffset() * 60000);
        
        // Format to remove milliseconds
        let dueDateISO = adjustedDate.toISOString().split(".")[0] + "Z";
        
        let formData = {
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            title: document.getElementById("title").value,
            details: document.getElementById("details").value,
            dueDate: dueDateISO,  // Now formatted correctly
            additionalNotes: document.getElementById("additionalNotes").value
        };
        
        const apiUrl = "https://q7ey10hfki.execute-api.af-south-1.amazonaws.com/Dev/submitPlan";  // Replace with your API Gateway URL
        console.log("Form Data:", formData);
        alert(JSON.stringify(formData, null, 2));
    

        try {
            let response = await fetch(apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            });
    
            let data = await response.json();
            document.getElementById("responseMessage").innerText = data.message || "Plan submitted successfully! Kindly Check your Mail to Confirm the Subscription";
        } catch (error) {
            document.getElementById("responseMessage").innerText = "Error submitting plan.";
        }
    });
});



