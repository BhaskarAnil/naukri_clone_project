function toggleCompanyField() {
  var checkbox = document.getElementById('is_employer');
  var companyField = document.getElementById('company_name_field');
  if (checkbox && companyField) {
    companyField.style.display = checkbox.checked ? 'block' : 'none';
  }
}

document.addEventListener('DOMContentLoaded', function() {
  var checkbox = document.getElementById('is_employer');
  if (checkbox) {
    checkbox.addEventListener('change', toggleCompanyField);
    toggleCompanyField();
  }
});
