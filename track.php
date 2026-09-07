<?php
/**
 * track.php — tracking pixel for the phishing-awareness campaign.
 * Logs one line per click (timestamp, recipient id, IP, user-agent),
 * then returns a 1x1 transparent GIF. Data stays on your own server.
 *
 * Email/landing link should carry a per-recipient id, e.g.
 *   https://arnaq.traject.brussels/?u=jan.peeters
 * which index.html forwards to this pixel as ?u=jan.peeters
 */

// --- collect, sanitised ------------------------------------------------------
$id  = isset($_GET['u']) ? substr(preg_replace('/[^A-Za-z0-9._@-]/', '', $_GET['u']), 0, 64) : 'unknown';
$ts  = date('c'); // ISO 8601, e.g. 2026-09-07T15:42:10+02:00
$ip  = $_SERVER['REMOTE_ADDR'] ?? '';
$ua  = str_replace(["\t", "\r", "\n"], ' ', $_SERVER['HTTP_USER_AGENT'] ?? '');

// --- append to a tab-separated log (created on first hit) --------------------
$logfile = __DIR__ . '/clicks.tsv';
if (!file_exists($logfile)) {
    @file_put_contents($logfile, "timestamp\tid\tip\tuser_agent\n", LOCK_EX);
}
$line = sprintf("%s\t%s\t%s\t%s\n", $ts, $id, $ip, $ua);
@file_put_contents($logfile, $line, FILE_APPEND | LOCK_EX);

// --- return a non-cacheable 1x1 transparent GIF ------------------------------
header('Content-Type: image/gif');
header('Content-Length: 43');
header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
header('Pragma: no-cache');
header('Expires: 0');
echo base64_decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7');
