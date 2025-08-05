// Limit contact number length to 10
function limitContactLength(input) {
  if (input.value.length > 10) {
    input.value = input.value.slice(0, 10);
  }
}

//----------------------------------------------------------------------------------------------
//Validating records before updating
//----------------------------------------------------------------------------------------------

function validateUserUpdateForm() {
  var isupdateNameValid = nameValidation("updateName", "nameUpdateErr");
  var isupdateEmailValid = emailValidation("updateEmail", "emailUpdateErr");
  var isupdateAddressValid = addressValidation(
    "updateAddress",
    "addressUpdateErr"
  );
  var isupdateContactValid = contactValidation(
    "updateContact",
    "contactUpdateErr"
  );

  if (
    isupdateNameValid &&
    isupdateEmailValid &&
    isupdateAddressValid &&
    isupdateContactValid
  ) {
    return true;
  } else {
    return false;
  }
}


function validateForm() {
  const validName = nameValidation('fullName', 'nameErr');
  const validEmail = emailValidation('email', 'emailErr');
  const validPhone = contactValidation('phone', 'phoneErr');
  const validAddress = addressValidation('address', 'adddressErr');
  const validPassword = passwordValidation('newPassword', 'newPassErr');
  const validConfirm = checkPass('confirmPassword', 'newPassword', 'confirmPassErr');

  return validName && validEmail && validPhone && validAddress && validPassword && validConfirm;
}

function validateEditForm() {
  const validName = nameValidation('fullName', 'nameErr');
  const validEmail = emailValidation('email', 'emailErr');
  const validPhone = contactValidation('phone', 'phoneErr');
  const validAddress = addressValidation('address', 'addressErr');

  return validName && validEmail && validPhone && validAddress;
}


//----------------------------------------------------------------------------------------------
// functions to validate input fields
//----------------------------------------------------------------------------------------------

function nameValidation(inputId, errorId) {
  var name = document.getElementById(inputId).value;
  var errorElem = document.getElementById(errorId);
  errorElem.innerHTML = "";
  const nameRegex = /^[a-zA-Z ]{4,}$/;
  if (!nameRegex.test(name)) {
    errorElem.innerHTML = name.length < 4 ? "Name is too short" : "Invalid name";
    return false;
  }
  return true;
}

function emailValidation(inputId, errorId) {
  var email = document.getElementById(inputId).value;
  var errorId = document.getElementById(errorId);
  errorId.innerHTML = "";
  const emailRegex =
    /(?:[a-z0-9!#$%&'+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
  if (!emailRegex.test(email)) {
    errorId.innerHTML = "Invalid email";
    return false;
  }
  return true;
}

function addressValidation(inputId, errorId) {
  var address = document.getElementById(inputId).value;
  var errorId = document.getElementById(errorId);
  errorId.innerHTML = "";
  const addressRegex = /^(?=.*[a-zA-Z])[a-zA-Z0-9\s,'-]{4,}$/;
  if (!addressRegex.test(address)) {
    errorId.innerHTML = "Invalid address";
    return false;
  }
  return true;
}

function contactValidation(inputId, errorId) {
  var contact = document.getElementById(inputId).value;
  var errorId = document.getElementById(errorId);
  errorId.innerHTML = "";
  const contactRegex = /^(98|97)\d{8}$/;
  if (!contactRegex.test(contact)) {
    errorId.innerHTML = "Invalid contact no.";
    return false;
  }
  return true;
}

function passwordValidation(inputId, errorId) {
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*[^A-Za-z0-9]).{8,25}$/;
  var password = document.getElementById(inputId).value;
  var errorId = document.getElementById(errorId);
  errorId.innerHTML = "";
  if (!passwordRegex.test(password)) {
    if (password.length < 8) {
      errorId.innerHTML = "Password must be at least 8 characters long";
    } else {
      errorId.innerHTML =
        "Password must contain at least one letter and one special character";
    }
    return false;
  }
  return true;
}

function checkPass(inputId1, inputId2, errorId) {
  // for admin and teacher pages
  var cpass = document.getElementById(inputId1).value;
  var pass = document.getElementById(inputId2).value;
  var errorId = document.getElementById(errorId);
  errorId.innerHTML = "";
  if (pass != cpass) {
    errorId.innerHTML = "Password does not match";
    return false;
  }
  return true;
}

function confirmPasswordValidation(passId, confirmId, errId) {
  const pass = document.getElementById(passId).value;
  const confirm = document.getElementById(confirmId).value;
  const errorElem = document.getElementById(errId);
  const matchText = document.getElementById("passwordMatch");

  if (pass !== confirm) {
    errorElem.textContent = "Passwords do not match.";
    matchText.textContent = "Passwords do not match";
    return false;
  }

  errorElem.textContent = "";
  matchText.textContent = "Passwords matched";
  return true;
}

function validatePasswordForm() {
  const validNew = passwordValidation('newPassword', 'newPassErr');
  const validConfirm = confirmPasswordValidation('newPassword', 'confirmPassword', 'confirmPassErr');

  return validNew && validConfirm;
}
