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
 * Each click appends: timestamp, id (campaign label), user-agent, likely.
 * "likely" is a coarse bot/human guess from the user-agent, to help filter out
 * mail security scanners (Safe Links, Mimecast, ...) from real clicks.
 * Google does not expose the visitor's IP to Apps Script, so IP is not logged.
 */
function doGet(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('clicks') || ss.insertSheet('clicks');
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['timestamp', 'id', 'user_agent', 'likely']);
    }
    var p = (e && e.parameter) ? e.parameter : {};
    var ua = p.ua || '';
    sheet.appendRow([new Date(), p.u || 'unknown', ua, classify(ua)]);
  } finally {
    lock.releaseLock();
  }
  // Apps Script can only return text. The click is already logged above;
  // the browser ignores this response, which is fine for tracking.
  return ContentService.createTextOutput('ok');
}

/**
 * Coarse "bot" vs "human" guess from the user-agent.
 * Scanners/bots often have empty, non-browser, or headless UAs; real people
 * come through with a normal Mozilla/... browser string.
 */
function classify(ua) {
  if (!ua) return 'bot';                       // no UA = almost certainly a scanner
  var s = ua.toLowerCase();
  var botHints = ['bot', 'crawl', 'spider', 'scan', 'preview', 'headless',
                  'python', 'curl', 'wget', 'go-http', 'java', 'okhttp',
                  'httpclient', 'safelinks', 'mimecast', 'proofpoint',
                  'barracuda', 'microsoft', 'slackbot', 'facebookexternalhit'];
  for (var i = 0; i < botHints.length; i++) {
    if (s.indexOf(botHints[i]) !== -1) return 'bot';
  }
  // Real browsers virtually always contain "mozilla"; absence is suspicious.
  return s.indexOf('mozilla') !== -1 ? 'human' : 'bot';
}
