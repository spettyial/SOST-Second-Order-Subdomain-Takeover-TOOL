<h1> What is Second-Order Subdomain Takeover?</h1>

Second-Order Subdomain Takeover refers to a security issue where a subdomain is not directly vulnerable, but it is indirectly referenced by other applications or websites in a way that allows exploitation after an attacker takes control of it.
<h2> How is it different from regular subdomain takeover?</h2>

  <b>Regular Subdomain Takeover:</b> The vulnerable subdomain is actively pointing (via CNAME or A record) to a third-party service (e.g., GitHub, Heroku) that is not claimed. Anyone can claim it and host content.

  <b>Second-Order Subdomain Takeover:</b> The vulnerable subdomain might not even appear in a browser or website, but it’s referenced in places like:

        script-src, iframe, img, style, or API calls (XHR/fetch) inside HTML/JS

        DNS-based settings (e.g., SPF, DKIM)

        CORS headers, CSP headers

        External services (e.g., ads, analytics, CDNs)




<h4>REQUIREMENTS:</h4>
1-python3<br>
2-pip install requests beautifulsoup4 urllib3


<h4>USAGE:</h4>
1-Enter the domain you want to scan in the domain section at the bottom of the code.<br>
2-Use this command "python3 SOST.py" or "python SOST.py"



