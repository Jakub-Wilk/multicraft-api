from multicraftapi import MulticraftAPI


# Arguments: (url, username, api_key)
client = MulticraftAPI("http://example.com/multicraft/api.php",  "Example_Username",  "3X4MP134P1K3Y")

# Arguments: (function, *args)
response =  client("getServerStatus",  "123456")

# Response is always JSON in form {'success': <success_status>, 'errors': [<errors>], 'data':[<returned data>]}
print(response)