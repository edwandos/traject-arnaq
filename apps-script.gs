/**
 * apps-script.gs — click logger for the phishing-awareness landing page.
 *
 * Setup:
 *  1. Create a new Google Sheet (this is where clicks land).
 *  2. Extensions > Apps Script. Delete the default code, paste this in, Save.
 *  3. Deploy > New deployment > type "Web app".
 *       - Description : phishing-awareness tracker
 *       - Execute as  : Me
 *       - Who has access: Anyone
 *     Deploy, authorise, and copy the Web app URL (ends in /exec).
 *  4. Paste that URL into index.html (TRACK_URL) and the <noscript> fallback.
 *
 * Each click appends: timestamp, id (the ?u= value), user-agent.
 * Google does not expose the visitor's IP to Apps Script, so IP is not logged.
 */
function doGet(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('clicks') || ss.insertSheet('clicks');
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['timestamp', 'id', 'user_agent']);
    }
    var p = (e && e.parameter) ? e.parameter : {};
    sheet.appendRow([new Date(), p.u || 'unknown', p.ua || '']);
  } finally {
    lock.releaseLock();
  }
  // Apps Script can only return text. The click is already logged above;
  // the browser ignores this response, which is fine for tracking.
  return ContentService.createTextOutput('ok');
}
