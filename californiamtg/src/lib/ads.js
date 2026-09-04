/* CaliforniaMTG — consent-gated Google Ads conversion tracking */
const ADS_ID = "AW-18417657219";
const LEAD_DESTINATION = "AW-18417657219/LiA7CPWd4eocEIPLnM5E";

function hasAdsConsent() {
  try { return window.localStorage.getItem("cookie_consent_status") === "accepted"; }
  catch (_) { return false; }
}

function uid() {
  if (window.crypto && window.crypto.randomUUID) return "cmtg_" + window.crypto.randomUUID();
  return "cmtg_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 10);
}

export function initGoogleAds() {
  if (typeof window === "undefined" || typeof document === "undefined" || !hasAdsConsent()) return false;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

  if (!window.__cmtgAdsConfigured) {
    window.__cmtgAdsConfigured = true;
    window.gtag("js", new Date());
    window.gtag("config", ADS_ID);
  }

  if (!document.querySelector("script[data-cmtg-google-ads]")) {
    const script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(ADS_ID);
    script.setAttribute("data-cmtg-google-ads", "");
    document.head.appendChild(script);
  }
  return true;
}

export function fireLeadConversion(meta) {
  if (!initGoogleAds()) return null;
  const id = uid();
  const data = Object.assign({
    event: "californiamtg_lead_submit",
    lead_event_id: id,
    page_location: window.location.href
  }, meta || {});
  window.dataLayer.push(data);
  window.gtag("event", "conversion", {
    send_to: LEAD_DESTINATION,
    value: 1.0,
    currency: "USD",
    transaction_id: id
  });
  return id;
}
