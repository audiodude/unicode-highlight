import re
import unicodedata
import urllib
import flask

app = flask.Flask(__name__)

character_names = { "\n": "\\n", "\r": "\\r", "\t": "\\t" }

# Load some Unicode data remotely.
unicode_blocks = []
for line in urllib.urlopen("http://www.unicode.org/Public/UNIDATA/Blocks.txt").read().split("\n"):
  if line.strip() != "" and line[0] != "#":
    m = re.match("([0-9A-F]+)\.\.([0-9A-F]+); (.*)", line)
    unicode_blocks.append({
      "start": int(m.group(1), 16),
      "end": int(m.group(2), 16),
      "name": m.group(3),
    })

def lookup_block(c):
  c = ord(c)
  for block in unicode_blocks:
    if block["start"] <= c <= block["end"]:
      return block["name"]
  return None

def highlight_content(text):
  ret = []
  for character in unicode(text):
    suspicious = False

    # How to display this character?
    if unicodedata.category(character)[0] in ("L", "N", "P", "S"):
      # letters, numbers, punctuation, and symbols -- things that should be displayable
      display = character
    elif character == " ":
      # show the space as a space
      display = " "
    elif character in character_names:
      # use some names that we preset
      display = character_names[character]
    else:
      # show the character as its name ("?" as fallback if character has no name)
      display = unicodedata.name(character, "?")
      suspicious = True

    if lookup_block(character) != "Basic Latin":
      suspicious = True

    ret.append({
      "codepoint": hex(ord(character)),
      "block": lookup_block(character),
      "character": character,
      "display": display,
      "eol": character in ("\n", "\r"),
      "suspicious": suspicious,
    })
  return ret

@app.route('/')
def hello():
  return flask.render_template('index.html')

@app.route('/highlight', methods=['POST'])
def highlight():
  content = highlight_content(flask.request.form['content'])
  return flask.render_template('highlight.html', content=content)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
