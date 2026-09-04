/* CaliforniaMTG contact forms — success UI only after backend acceptance. */
(function () {
  "use strict";

  function validate(form) {
    var ok = true;
    form.querySelectorAll("[required]").forEach(function (el) {
      if (el.type === "radio" || el.type === "checkbox") return;
      var bad = !String(el.value || "").trim();
      var field = el.closest(".field");
      var err = field && field.querySelector(".field-error");
      if (err) err.textContent = bad ? "This field is required." : "";
      if (bad) ok = false;
    });

    var row = form.querySelector(".radio-row");
    if (row) {
      var checked = form.querySelector('input[name="contactMethod"]:checked');
      var field = row.closest(".field");
      var err = field && field.querySelector(".field-error");
      if (err) err.textContent = checked ? "" : "Please choose a contact method.";
      if (!checked) ok = false;
    }
    return ok;
  }

  function showSuccess(form) {
    var card = document.getElementById("contactCard") || form.parentNode;
    if (!card) return;
    card.innerHTML =
      '<div class="thankyou">' +
        '<div class="ty-mark" aria-hidden="true">&#10003;</div>' +
        '<h3>Thank you.</h3>' +
        '<p class="ty-lead">Your scenario has been received. A licensed mortgage professional ' +
        'can review your situation and contact you about the next step.</p>' +
        '<p class="ty-compliance">This is not a loan approval, loan commitment, or rate quote. ' +
        'Final loan options are subject to review by a licensed mortgage professional.</p>' +
      '</div>';
    card.classList.add("is-thankyou");
  }

  function showError(form) {
    var existing = form.querySelector("[data-cm-submit-error]");
    if (!existing) {
      existing = document.createElement("div");
      existing.setAttribute("data-cm-submit-error", "");
      existing.setAttribute("role", "alert");
      existing.style.cssText = "margin:0 0 16px;padding:12px 14px;border:1px solid #b85c4a;border-radius:8px;background:#fff7f4;color:#6b2e23;line-height:1.5";
      form.insertBefore(existing, form.firstChild);
    }
    existing.textContent = "We couldn't send your request right now. Your information is still on this page. Please try again, or call (310) 654-1577.";
  }

  /* Capture phase runs before the legacy script.js submit handler. */
  document.addEventListener("submit", function (event) {
    var form = event.target;
    if (!form || !form.matches || !form.matches("form.cm-form")) return;

    event.preventDefault();
    event.stopImmediatePropagation();
    if (!validate(form)) return;

    var button = form.querySelector('button[type="submit"], input[type="submit"]');
    var oldText = button && button.tagName === "BUTTON" ? button.textContent : "";
    if (button) {
      button.disabled = true;
      if (button.tagName === "BUTTON") button.textContent = "Sending…";
    }

    var saver = window.CMLeads && window.CMLeads.saveContactForm;
    var promise = saver
      ? saver(form)
      : Promise.reject(new Error("Lead service unavailable"));

    Promise.resolve(promise)
      .then(function (result) {
        if (!result || !result.stored || result.stored === "local") throw new Error("No backend confirmation");
        showSuccess(form);
      })
      .catch(function (err) {
        console.warn("[California Mortgage] contact submission failed:", err);
        showError(form);
        if (button) {
          button.disabled = false;
          if (button.tagName === "BUTTON") button.textContent = oldText || "Submit";
        }
      });
  }, true);
})();
