# multicraft-api

### What it is

multicraft-api is a Python port of the [Multicraft API Interface](https://www.multicraft.org/site/docs/api).

### Installation

    pip install multicraft-api

### Usage

From example.py:

    from multicraftapi import MulticraftAPI
    

    # Arguments: (url, username, api_key)
	client = MulticraftAPI("http://example.com/multicraft/api.php",  "Example_Username",  "3X4MP134P1K3Y")

	# Arguments: (function, *args)
	response =  client("getServerStatus",  "123456")

    # Response is always JSON in form {'success': <success_status>, 'errors': [<errors>], 'data':[<returned data>]}
	print(response)

For more information, including all the functions and their args, please refer to the [wiki](https://github.com/Jakub-Wilk/MulticraftAPI.py/wiki).
