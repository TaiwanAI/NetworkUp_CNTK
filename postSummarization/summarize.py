import json
import sys

from textteaser import TextTeaser

# Store the title and text from the server
title = str(sys.argv[1])
text = str(sys.argv[2])

# Instantiate the TextTeaser API
tt = TextTeaser()

sentences = tt.summarize(title, text)

# Combine the text result into a single sentence
sentence = ' '.join(str(x) for x in sentences)

# Send back the summarizing result to the server
print json.dumps({'title': title, 'text': sentence})


