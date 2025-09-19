import pathway as pw
from stream import read_stream

# Define schema
class MessageSchema(pw.Schema):
    user: str
    text: str
    ts: str

# Custom Subject to push messages from read_stream()
class MessageSubject(pw.io.python.ConnectorSubject):
    def run(self):
        for msg in read_stream():
            self.next(user=msg["user"], text=msg["text"], ts=msg["ts"])

# Read messages into Pathway table
table = pw.io.python.read(MessageSubject(), schema=MessageSchema)

# Filter invalid messages using Pathway expressions
valid_messages = table.filter((table.text != "") & (table.user != ""))

# Print valid messages using compute_and_print
pw.debug.compute_and_print(valid_messages)

# Run the pipeline
pw.run()
