#!/usr/bin/env python3
"""
Send an HTML email through a Combell-hosted mailbox (authenticated SMTP).
For authorized phishing-awareness / security-training campaigns only.
"""
import smtplib
import ssl
import getpass
from email.message import EmailMessage
from email.utils import make_msgid, formataddr

# --- Combell SMTP settings ---------------------------------------------------
# Confirm the exact host in your Combell control panel (Mail > settings).
# Combell mailboxes usually use one of:
#   smtp.combell.com            (generic)
#   smtpout.combell.com
#   serverXX.combell.com        (server-specific, shown in your hosting panel)
SMTP_HOST = "smtp-auth.mailprotect.be"
SMTP_PORT = 465          # 587 = STARTTLS (recommended). Use 465 for implicit SSL.
USE_SSL   = True         # True = connect with SSL on 465; False = STARTTLS on 587

# --- Message -----------------------------------------------------------------
FROM_NAME  = "Traject - Duurzame Mobiliteit"
FROM_EMAIL = "info@traject.brussels"   # a real mailbox on your domain
TO         = ["edward.demoor@mpact.be"]            # recipients (test on yourself first)
SUBJECT    = "Fwd: Oproep: Wij willen jouw cijfers"

HTML_BODY = """\
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: Arial, sans-serif; color:#222; line-height: 1.5; }

    .email-chain { background:#fff; margin:16px 0; }
    .chain-header {
      background:#e8e8e8; padding:10px 12px; border-bottom:1px solid #ccc;
      font-size:12px; color:#333;
    }
    .chain-content { padding:12px; font-size:13px; }
    .chain-content p { margin:6px 0; }
    table { border-collapse: collapse; }
    .signature-table { margin-top:12px; }
    .signature-table td { padding:0; }
    .sig-divider { width:2px; background:#B0182B; height:80px; }
    .sig-content { padding-left:12px; }
    .sig-name { font-weight:bold; color:#1F2124; font-size:14px; }
    .sig-title { color:#B0182B; font-weight:bold; font-size:11px; margin:2px 0; }
    .sig-company { font-size:12px; color:#1F2124; margin:4px 0; }
    .sig-contact { font-size:12px; color:#555; margin:2px 0; }
    .sig-address { font-size:11px; color:#888; margin-top:4px; }
  </style>
</head>
<body>

<p>Beste,</p>

<p>We hoorden van Luc dat we beter jullie hiervoor contacteren (zie hieronder).</p>

<p>In het kader van de duurzame mobiliteit in Brussel verzamelen we cijfers rond het gebruik van verschillende vervoersmiddelen.</p>

<p>Omdat jullie met verschillende projecten betrokken zijn bij duurzame mobiliteit, willen we graag jullie cijfers ontvangen.</p>

<p>Om alle informatie te vinden rond de standaarden die we gebruiken en welke data we verwachten, kunnen jullie <a href="https://data.traject.brussels/">hier</a> onze technische omschrijving van onze standaard raadplegen.</p>

<p>Hopelijk horen we snel iets van jullie.</p>

<p>Met vriendelijke groeten,</p>

<table cellpadding="0" cellspacing="0" border="0" role="presentation" style="font-family: Arial, sans-serif; color:#1F2124;">
  <tr>
    <td valign="top" style="padding-right:12px;">
      <img src="https://data.traject.brussels/logo.jpg" alt="Traject" width="50" height="50" style="display:block; border:0; outline:none;">
    </td>
    <td class="sig-divider">&nbsp;</td>
    <td class="sig-content" valign="top">
      <div class="sig-name">Pierre Bertin</div>
      <div class="sig-title">Project Manager Sustainable Mobility</div>
      <div class="sig-company"><strong>Traject</strong> – Duurzame Mobiliteit</div>
      <div class="sig-contact">T +32 (0)2 321 12 14</div>
      <div class="sig-contact"><a href="mailto:info@traject.brussels" style="color:#1F2124; text-decoration:none;">info@traject.brussels</a> • <a href="https://traject.be" style="color:#B0182B; text-decoration:none; font-weight:bold;">data.traject.brussels</a></div>
      <div class="sig-address">Kantersteen 47, 1000 Brussel</div>
    </td>
  </tr>
</table>
<br><br><br>

<!-- Forwarded email chain -->
<div class="forwarding-header">
  ------ Forwarded Message ------<br>
  Van: Pierre Bertin (info@traject.brussels)<br>
  Date: dinsdag 13 oktober 2026 - 10:42<br>
  Subject: Oproep: Wij willen jouw cijfers<br>
  To: Luc Botten (luc.botten@mpact.be)<br>
</div>

<div class="email-chain">
  <div class="chain-content">
    <p>Beste Pierre,</p>
    <p>Bedankt voor je e-mail. We werken graag hieraan mee, kan je dit doorsturen naar it@mpact.be?</p>
    <p style="margin-top:12px;">Mvg,<br>
    Luc Botten<br>
    Directeur<br>
    Mpact</p>
  </div>
</div>

</body>
</html>

"""

# Plain-text fallback improves deliverability (and looks less suspicious to filters).
TEXT_BODY = "Beste,We hoorden van Luc dat we beter jullie hiervoor contacteren (zie hieronder).In het kader van de duurzame mobiliteit in Brussel verzamelen we cijfers rond het gebruik van verschillende vervoersmiddelen.Omdat jullie met verschillende projecten betrokken zijn bij duurzame mobiliteit, willen we graag jullie cijfers ontvangen. Om alle informatie te vinden rond de standaarden die we gebruiken en welke data we verwachten, kunnen jullie hier onze technische omschrijving van onze standaard raadplegen. Hopelijk horen we snel iets van jullie. Met vriendelijke groeten, Pierre Bertin Traject"


def build_message(to_addr: str) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = formataddr((FROM_NAME, FROM_EMAIL))
    msg["To"] = to_addr
    msg["Subject"] = SUBJECT
    msg["Message-ID"] = make_msgid(domain=FROM_EMAIL.split("@")[1])
    msg.set_content(TEXT_BODY)
    msg.add_alternative(HTML_BODY, subtype="html")
    return msg


def main():
    username = FROM_EMAIL
    password = getpass.getpass("SMTP password: ")
    ctx = ssl.create_default_context()

    try:
        if USE_SSL:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx, timeout=15)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
            server.starttls(context=ctx)
    except (TimeoutError, OSError) as e:
        print(f"\nCould not reach {SMTP_HOST}:{SMTP_PORT} -> {e}")
        print("This is almost always a firewall blocking outbound SMTP.")
        print("Try port 587 (STARTTLS), or run from a non-corporate network.")
        return

    with server:
        server.login(username, password)
        for to_addr in TO:
            msg = build_message(to_addr)
            server.send_message(msg)
            print(f"Sent to {to_addr}")


if __name__ == "__main__":
    main()
