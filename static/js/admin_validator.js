document.addEventListener("DOMContentLoaded", function () {
  // Utility function to show an error message
  function showError(field, message) {
    clearError(field);
    field.classList.add("error-border");

    const error = document.createElement("div");
    error.className = "error-message";
    error.innerText = message;
    field.parentElement.appendChild(error);
  }

  // Utility function to clear existing error
  function clearError(field) {
    field.classList.remove("error-border");
    const existingError = field.parentElement.querySelector(".error-message");
    if (existingError) {
      existingError.remove();
    }
  }

  // Name field validation: no numbers/special characters, min 4 chars
  function validateNameField(field) {
    const nameRegex = /^[A-Za-z\s]{4,}$/; // Only letters and spaces, min 4 chars

    const isValid = () => {
      const value = field.value.trim();
      if (value === "") {
        showError(field, "Name cannot be empty.");
        return false;
      } else if (!nameRegex.test(value)) {
        showError(
          field,
          "Name must be at least 4 characters and contain only letters and spaces."
        );
        return false;
      } else {
        clearError(field);
        return true;
      }
    };

    field.addEventListener("blur", isValid);
    return isValid;
  }

  // Price > 0
  function validatePositiveFloatField(field, fieldName) {
    const isValid = () => {
      const value = parseFloat(field.value);
      if (isNaN(value) || value <= 0) {
        showError(field, `${fieldName} must be greater than 0.`);
        return false;
      } else {
        clearError(field);
        return true;
      }
    };

    field.addEventListener("blur", isValid);
    return isValid;
  }

  // Stock ≥ 0
  function validateNonNegativeIntField(field, fieldName) {
    const isValid = () => {
      const value = parseInt(field.value);
      if (isNaN(value) || value < 0) {
        showError(field, `${fieldName} cannot be negative.`);
        return false;
      } else {
        clearError(field);
        return true;
      }
    };

    field.addEventListener("blur", isValid);
    return isValid;
  }

  // Attach validators
  const nameField = document.querySelector("#id_name");
  const priceField = document.querySelector("#id_price");
  const stockField = document.querySelector("#id_stock");

  const nameValidator = nameField ? validateNameField(nameField) : null;
  const priceValidator = priceField ? validatePositiveFloatField(priceField, "Price") : null;
  const stockValidator = stockField ? validateNonNegativeIntField(stockField, "Stock") : null;

  // Prevent form submission if any validation fails
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      let isValid = true;

      if (nameField && typeof nameValidator === "function" && !nameValidator()) isValid = false;
      if (priceField && typeof priceValidator === "function" && !priceValidator()) isValid = false;
      if (stockField && typeof stockValidator === "function" && !stockValidator()) isValid = false;

      if (!isValid) {
        e.preventDefault();
        alert("Please fix the validation errors before submitting.");
      }
    });
  }
});
