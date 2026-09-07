# Phishing-awareness landing page — GitHub Pages setup

A static "you've been phished" debrief page with click tracking via Google
Apps Script (no server needed).

## Files

| File | Keep on GitHub Pages? |
|------|-----------------------|
| `index.html`     | ✅ the landing page |
| `apps-script.gs` | ➖ reference only — its code lives in Google, not the repo |
| `track.php`      | ❌ delete (PHP does not run on Pages) |
| `results.php`    | ❌ delete (PHP does not run on Pages) |
| `.htaccess`      | ❌ delete (Pages ignores it) |

---

## 1. Set up click tracking (Google Apps Script)

1. Create a new **Google Sheet** (any Google account). This is your results log.
2. **Extensions → Apps Script**. Delete the sample code, paste in the contents
   of `apps-script.gs`, and **Save**.
3. **Deploy → New deployment → Web app**:
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Authorise when prompted, then **copy the Web app URL** (ends in `/exec`).
5. Open `index.html` and paste that URL into **both** places marked
   `PASTE_YOUR_ID` (the `TRACK_URL` in the script, and the `<noscript>` image).

Each click adds a row to the sheet: **timestamp · id · user-agent**.
(No IP — Google doesn't expose it to Apps Script.)

> Want IP addresses too? Ask me for the Cloudflare Worker version instead.

---

## 2. Publish on GitHub Pages

1. Create a GitHub repo (e.g. `arnaq`) and add **`index.html`** (delete the
   `.php` files and `.htaccess`).
2. Repo **Settings → Pages**:
   - Source: **Deploy from a branch**
   - Branch: **main** / **/ (root)** → Save.
3. Your site goes live at `https://<username>.github.io/arnaq/` within a minute.
   Test it there first (click it, confirm a row appears in your Sheet).

---

## 3. Use your own domain (custom subdomain)

Serving it from `traject.brussels` looks far more trustworthy than
`github.io`. Use a **subdomain** (not the apex), e.g. `info.traject.brussels` —
pick a name that reads as legitimate to your colleagues.

### 3a. Tell GitHub the domain
- **Settings → Pages → Custom domain**: enter `info.traject.brussels`, Save.
  (This commits a `CNAME` file to the repo — leave it there.)

### 3b. Combell DNS
1. Log in to **my.combell.com** → **Domains** → select **traject.brussels**.
2. Open **DNS settings** (Advanced DNS / DNS records).
3. Add a record:
   | Field | Value |
   |-------|-------|
   | Type  | **CNAME** |
   | Name / host | **info** (just the subdomain part) |
   | Value / target | **`<username>.github.io.`** (your GitHub username, trailing dot) |
   | TTL   | default (e.g. 1 hour) |
4. Save. Propagation is usually minutes, up to a few hours.

> Do **not** point the apex `traject.brussels` at GitHub — keep the subdomain
> so your mail (`info@traject.brussels`) and website are unaffected.

### 3c. Enforce HTTPS
- Back in **Settings → Pages**, once DNS resolves, tick **Enforce HTTPS**.
  GitHub issues a free certificate automatically (can take up to ~1 hour).

---

## 4. Point the email at the page

In `send_campaign.py`, make the link target this page with a **unique id per
recipient** so you know who clicked:

```
https://info.traject.brussels/?u=jan.peeters
```

The page reads `?u=` and logs it. Give each recipient a distinct `u` value.

---

## Note on GitHub's terms

This page is a **debrief/education** page (it states up front that it was a
simulation and collects no credentials), which is low-risk. Do **not** turn it
into a fake login / credential-capture page on GitHub Pages — that violates
their Acceptable Use Policy and can get the repo taken down.
