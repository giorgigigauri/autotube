from utils.CreateMovie import CreateMovie, GetDaySuffix
import json


post = json.loads('{"id": "62td2v", "title": "Half-naked girls get thousands of upvotes, how many for our boy in blue?", "score": 205015, "18": false, "Best_comment": "LOL OP is a mod of /r/enoughmuskspam ", "best_reply": "You could say I am trying to prove my point using a path some may find... *unnatural.*"}')
CreateMovie.CreateMP4(post)
