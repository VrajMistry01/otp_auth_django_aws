/* static/js/script.js */

// Example of handling error messages for login and OTP
document.addEventListener("DOMContentLoaded", function () {
  // If there's an error message for the login form
  const errorMessage = document.getElementById("error-message");
  if (errorMessage) {
    setTimeout(function () {
      errorMessage.textContent = ""; // Clear the error after 5 seconds
    }, 5000);
  }

  // OTP error message for OTP form
  const otpErrorMessage = document.getElementById("otp-error-message");
  if (otpErrorMessage) {
    setTimeout(function () {
      otpErrorMessage.textContent = ""; // Clear the error after 5 seconds
    }, 5000);
  }
});
