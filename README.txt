Will update README for EVE Combat Interaction Tool (ECIT) at a later time.

Re: random_state_svc 
The service runs as a Flask app; before beginning, change the host and port to whatever desired on line 28. Start the service. 

To REQUEST: Once the service is running, use HTTP GET requests to the endpoint found at 'http://yourhost:yourport/random-state'; no payload in the request is needed

To RECEIVE: JSON packages containing a single US State abbreviation as a string. Use json.loads to unpack and utilize the contents of the JSON package.

Example: requests.get('http://localhost:5000/random-state') --->  will receive a JSON object = { "AL" }, use json.loads(object) to retreive the string "AL" for use elsewhere.
