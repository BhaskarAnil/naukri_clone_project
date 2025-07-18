// Live job search filter
document.addEventListener('DOMContentLoaded', function() {
  var searchInput = document.getElementById('job-search-input');
  var jobsList = document.getElementById('jobs-list');
  if (searchInput && jobsList) {
    searchInput.addEventListener('input', function() {
      var val = searchInput.value.trim().toLowerCase();
      var cards = jobsList.querySelectorAll('.job-card');
      cards.forEach(function(card) {
        var title = card.getAttribute('data-title') || '';
        var desc = card.getAttribute('data-description') || '';
        var loc = card.getAttribute('data-location') || '';
        var comp = card.getAttribute('data-company') || '';
        if (
          val === '' ||
          title.includes(val) ||
          desc.includes(val) ||
          loc.includes(val) ||
          comp.includes(val)
        ) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }
});
document.addEventListener('DOMContentLoaded', function() {
  var navToggle = document.getElementById('navToggle');
  var mainNav = document.querySelector('.main-nav');
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function() {
      mainNav.classList.toggle('open');
    });
  }
  document.addEventListener('click', function(event) {
  if (
    mainNav.classList.contains('open') &&
    !mainNav.contains(event.target) &&
    !navToggle.contains(event.target)
  ) {
    mainNav.classList.remove('open');
  }
});
    const addJobForm = document.querySelector('.add-job-form');
    if (addJobForm) {
        const submitBtn = addJobForm.querySelector('.submit-job-btn');
        addJobForm.addEventListener('submit', function(e) {
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Adding...';
            }
        });
        const fieldErrors = document.querySelectorAll('.field-error');
        if (fieldErrors.length > 0 && submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Add Job';
        }
    }
    document.querySelectorAll('.delete-job-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (btn.getAttribute('data-job-id')) {
                if (!confirm('Are you sure you want to delete this job?')) {
                    e.preventDefault();
                    return false;
                }
                btn.disabled = true;
                btn.textContent = 'Deleting...';
                window.location.href = '/employer/jobs/' + btn.getAttribute('data-job-id') + '/delete/';
            }
        });
    });
});
