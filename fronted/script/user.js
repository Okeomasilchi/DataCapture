document.addEventListener("DOMContentLoaded", function() {
    // Functionality for Upload Image button
    document.querySelector('.upload-btn').addEventListener('click', function() {
      alert("Upload image functionality will be implemented here.");
    });
  
    // Functionality for Delete Account button
    document.querySelector('.delete').addEventListener('click', function() {
      if (confirm("Are you sure you want to delete your account?")) {
        alert("Account deleted successfully.");
      }
    });
  
    // Functionality for Change Password button
    document.querySelector('.change-password-btn').addEventListener('click', function() {
      alert("Change password functionality will be implemented here.");
    });
  
    // Functionality for Save button
    document.querySelector('.save-btn').addEventListener('click', function() {
      alert("User information saved successfully.");
    });
  });
  