import flask

app = flask.Flask(__name__)

ZWS = flask.Markup('<span class="highlight zero-width-char">zw</span>')

def replace_zero_width(text):
  text = text.replace(u'\u200B', ZWS).replace(u'\u200C', ZWS)
  return text.replace(u'\u200D', ZWS).replace(u'\uFEFF', ZWS)

def highlight_content(text):
  escaped = flask.Markup.escape(text)
  without_zwc = replace_zero_width(escaped)
  with_breaks = without_zwc.replace('\n', flask.Markup('<br>'))
  bytestring = with_breaks.encode('utf-8')
  print repr(bytestring)
  output = []

  in_high_bytes = False
  for byte in bytestring:
    if ord(byte) > 127:
      if not in_high_bytes:
        in_high_bytes = True
        output.extend(list(b'<span class="highlight">'))
    elif in_high_bytes:
      output.extend(list(b'</span>'))
      in_high_bytes = False
    output.append(byte)

  if in_high_bytes:
    output.extend(list(b'</span>'))

  return ''.join(output).decode('utf-8')

@app.route('/')
def hello():
  return flask.render_template('index.html')

@app.route('/highlight', methods=['POST'])
def highlight():
  content = highlight_content(flask.request.form['content'])
  return flask.render_template('highlight.html', content=flask.Markup(content))

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
