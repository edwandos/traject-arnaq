<?php
/**
 * results.php — simple protected viewer for the click log.
 * Open:  https://arnaq.traject.brussels/results.php?key=CHANGE-ME
 * Change the secret below before deploying.
 */
$SECRET = 'CHANGE-ME';   // <-- set your own long random string

if (($_GET['key'] ?? '') !== $SECRET) {
    http_response_code(403);
    exit('Forbidden');
}

$logfile = __DIR__ . '/clicks.tsv';
$rows = file_exists($logfile) ? array_filter(array_map('trim', file($logfile))) : [];

header('Content-Type: text/html; charset=utf-8');
echo "<!doctype html><meta charset='utf-8'>";
echo "<title>Click results</title>";
echo "<style>body{font-family:Arial,Helvetica,sans-serif;margin:24px;color:#1F2124}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border:1px solid #ddd;padding:6px 10px;text-align:left}
th{background:#f4f5f7}tr:nth-child(even){background:#fafafa}
h1{font-size:18px}.muted{color:#777}</style>";

$total = max(0, count($rows) - 1); // minus header line
echo "<h1>Phishing-test kliks <span class='muted'>(" . $total . " geregistreerd)</span></h1>";

if (!$rows) { echo "<p class='muted'>Nog geen kliks geregistreerd.</p>"; exit; }

echo "<table>";
foreach ($rows as $i => $line) {
    $cells = explode("\t", $line);
    $tag = $i === 0 ? 'th' : 'td';
    echo '<tr>';
    foreach ($cells as $c) echo "<$tag>" . htmlspecialchars($c) . "</$tag>";
    echo '</tr>';
}
echo "</table>";
