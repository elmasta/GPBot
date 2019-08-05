# What is this?

Don't you like it when your grandpa tell you incoherent and boring stories?
Well, you're in luck, This program act just like him! Just ask for a the story of some place and he'll kindly give you the adresse and tell you some story. He can even give you a summary of that place if it's in his encyclopedia.

# But how does it works?

Once the user make a request, the server calls the methods in qparser.py one by one to parse and then get the wanted infos online using Google Geocoder and Wikimedia API.
Once that's done, the server send a json with all the infos to the client and java do the rest. I used the Leaflet API to show the map.

# Can I try it?
You can try it directly here: https://el-gpbot.herokuapp.com/