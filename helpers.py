import matplotlib.pyplot as plt
import io
from werkzeug.datastructures import FileStorage

def deep_copy(file):
  file.stream.seek(0)
  # Read the contents of the original file
  file_contents = file.stream.read()

  # Create a new stream for the copy
  new_stream = io.BytesIO(file_contents)

  # Rewind the original file and the new copy
  file.stream.seek(0)
  new_stream.seek(0)

  # Create a new FileStorage object with the copied stream
  copied_file_storage = FileStorage(
      stream=new_stream,
      filename=file.filename,
      name=file.name,
      content_type=file.content_type,
      content_length=file.content_length,
      headers=file.headers,
  )
  
  return copied_file_storage