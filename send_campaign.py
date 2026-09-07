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
TO         = ["edward.demoor@mpact.be", "veronika.usova@mpact.be"]            # recipients (test on yourself first)
SUBJECT    = "Oproep: Wij willen jouw cijfers"

HTML_BODY = """\
<!doctype html>
<html>
  <body style="font-family: Arial, sans-serif; color:#222;">
    <p>Beste partnerorganisatie,</p>
    <p>In het kader van de duurzame mobiliteit in Brussel verzamelen we cijfers rond het gebruik van verschillende vervoersmiddelen.</p>
    <p>Daarvoor kan je onze technische omschrijving van onze standaard raadplegen: <a href="https://www.traject.brussels/aanbesteding">hier</a>.</p>
    <p>Hopelijk horen we snel iets van jullie.</p>

    <table cellpadding="0" cellspacing="0" border="0" role="presentation"
       style="font-family: Arial, Helvetica, sans-serif; color:#1F2124; font-size:13px; line-height:1.4;">
  <tr>
    <!-- Logo column -->
    <td valign="top" style="padding-right:18px;">
      <table cellpadding="0" cellspacing="0" border="0" role="presentation">
        <tr>
          <td align="center" valign="middle">
            <!-- Email clients strip inline SVG. Host a PNG on your domain and
                 reference it here. Width/height set so Outlook reserves the box. -->
            <img src="https://www.traject.brussels/logo.png"
                 alt="Traject" width="150" height="31"
                 style="display:block; border:0; outline:none; text-decoration:none;">
          </td>
        </tr>
      </table>
    </td>

    <!-- Red divider -->
    <td style="width:2px; background:#B0182B; font-size:1px; line-height:1px;">&nbsp;</td>

    <!-- Details column -->
    <td valign="top" style="padding-left:18px;">
      <div style="font-size:15px; font-weight:bold; color:#1F2124;">
        Pierre Bertin
      </div>
      <div style="font-size:12px; color:#B0182B; font-weight:bold; padding:1px 0 6px;">
        Project Manager Sustainable Mobility
      </div>

      <div style="font-size:12px; color:#1F2124;">
        <strong>Traject</strong> &ndash; Duurzame Mobiliteit
      </div>
      <div style="font-size:12px; color:#555555; padding-top:4px;">
        T&nbsp;+32 (0)2 321 12 14
      </div>
      <div style="font-size:12px; padding-top:2px;">
        <a href="mailto:info@traject.brussels" style="color:#1F2124; text-decoration:none;">info@traject.brussels</a>
        &nbsp;&bull;&nbsp;
        <a href="https://www.traject.brussels" style="color:#B0182B; text-decoration:none; font-weight:bold;">www.traject.brussels</a>
      </div>
      <div style="font-size:11px; color:#8A8A8A; padding-top:6px;">
        Kantersteen 47, 1000 Brussel
      </div>
    </td>
  </tr>
</table>

  </body>
</html>
"""

# Plain-text fallback improves deliverability (and looks less suspicious to filters).
TEXT_BODY = "Om onze werking in Brussel verder uit te bouwen, hebben we door de complexiteit van onze hoofdstad nood aan een ondersteunden tool blabla bla."


def build_message(to_addr: str) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = formataddr((FROM_NAME, FROM_EMAIL))
    msg["To"] = to_addr
    msg["Subject"] = SUBJECT
    msg["Message-ID"] = make_msgid(domain=FROM_EMAIL.split("@")[1])
    msg.set_content(TEXT_BODY)
    msg.add_alternative(HTML_BODY.format(tracking_id="test123"), subtype="html")
    return msg


def main():
    username = input(f"SMTP username (full email, e.g. {FROM_EMAIL}): ").strip()
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
