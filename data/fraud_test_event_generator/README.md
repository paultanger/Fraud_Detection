# Happendazzler: a Simulated Access Point to Live Event Data 

The Happendazzler class and the specific pickled instance of the Happendazzler object will simulate a custom data access point created by an engineer for you to use. It's designed to be a black box so that you don't focus too much on how this portion of the larger project might work but has well defined properties that you can use to simulate live data.

Instructions for using the live data simulator is documented in the BackendEngineer.ipynb file. The object will randomly update with a new event about once a minute, so acquiring new data means using the return from the `.event()` method at least once a minute to be sure you have the most recent event listing. 

### To use the object: 

```
import pickle
import json
from Happendazzler import Happendazzler 

event_generator=pickle.load(open('ebr.p', 'rb'))

# return the most recent event -- new event roughly every minute, drawn with replacements from test database 

event_generator.event()

# if you want it formatted as a dictionary

current_event=event_generator.event()
json.loads(current_event)
```