from checker import build_url, is_https, scan_sites, show_response, check_site, scan_sites, check_headers, retry_check
# Partea 1: apeluri pentru build_url și is_https
build_url("example.com", "login")
build_url("example.com", "/login")
is_https("https://example.com/login")
# Partea 2: apeluri pentru show_response
show_response("https://httpbin.org/html")
# Partea 3: apeluri pentru check_site
check_site("https://httpbin.org/json")
# Partea 4: apelul scan_sites()
scan_sites()
# Partea 5: apeluri pentru check_headers
print(check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
# Partea 6: apeluri pentru retry_check
