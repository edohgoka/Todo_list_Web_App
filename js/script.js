function validateForm() {
    var input = document.getElementById("myInput").value;
    if (input === "") {
      alert("Input should not be empty");
      return false; // Prevent form submission
    }
    return true; // Allow form submission
  }