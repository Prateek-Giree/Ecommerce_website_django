// Password show or hide

function togglePassword(fieldId) {
  const field = document.getElementById(fieldId);

  if (field.type === "password") {
    field.type = "text";
  } else {
    field.type = "password";
  }
}

// Check password strength
function checkPasswordStrength(password) {
  let strength = 0;
  let feedback = "";

  // If password is empty, reset to default state
  if (password.length === 0) {
    const strengthElement = document.getElementById("passwordStrength");
    const strengthText = strengthElement.querySelector(".strength-text");
    strengthElement.className = "password-strength";
    strengthText.textContent = "Password strength: Not entered";
    return;
  }

  // Check different criteria
  if (password.length >= 8) strength += 1;
  if (/[a-z]/.test(password)) strength += 1;
  if (/[A-Z]/.test(password)) strength += 1;
  if (/[0-9]/.test(password)) strength += 1;
  if (/[^A-Za-z0-9]/.test(password)) strength += 1;

  const strengthElement = document.getElementById("passwordStrength");
  const strengthText = strengthElement.querySelector(".strength-text");

  // Reset all classes
  strengthElement.className = "password-strength";

  // Apply appropriate strength class and feedback
  switch (strength) {
    case 0:
    case 1:
      strengthElement.classList.add("strength-weak");
      feedback = "Password strength: Weak";
      break;
    case 2:
      strengthElement.classList.add("strength-medium");
      feedback = "Password strength: Medium";
      break;
    case 3:
    case 4:
      strengthElement.classList.add("strength-strong");
      feedback = "Password strength: Strong";
      break;
    case 5:
      strengthElement.classList.add("strength-very-strong");
      feedback = "Password strength: Very Strong";
      break;
  }

  strengthText.textContent = feedback;
}

function resetForm() {
  if (
    confirm(
      "Are you sure you want to cancel? All unsaved changes will be lost."
    )
  ) {
    document.getElementById("profileForm").reset();
    location.reload();
  }
}

// Event listeners for password strength check
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("newPassword").addEventListener("input", function () {
    checkPasswordStrength(this.value);
  });
});



// CART 
document.addEventListener("DOMContentLoaded", function () {
  // Add listeners to all +/- buttons
  document.querySelectorAll(".quantity-btn").forEach(button => {
    button.addEventListener("click", function () {
      const row = button.closest("tr");
      const qtyInput = row.querySelector(".quantity-input");
      let quantity = parseInt(qtyInput.value);

      // Determine whether "+" or "-"
      if (button.textContent.trim() === "+") {
        quantity++;
      } else if (quantity > 1) {
        quantity--;
      }

      qtyInput.value = quantity;
      updateRowSubtotal(row);
      updateCartTotal();
    });
  });

  // Initial calculation on page load
  document.querySelectorAll("tbody tr").forEach(row => {
    updateRowSubtotal(row);
  });
  updateCartTotal();
});

function updateRowSubtotal(row) {
  const price = parseFloat(row.querySelector(".unit-price").textContent.replace("$", "").trim());
  const qty = parseInt(row.querySelector(".quantity-input").value);
  const subtotal = (price * qty).toFixed(2);
  row.querySelector(".subtotal").textContent = `$${subtotal}`;
}

function updateCartTotal() {
  let total = 0;
  document.querySelectorAll(".subtotal").forEach(cell => {
    total += parseFloat(cell.textContent.replace("$", ""));
  });
  total = total.toFixed(2);
  document.getElementById("cart-subtotal").textContent = `$${total}`;
  document.getElementById("cart-total").textContent = `$${total}`;
}
