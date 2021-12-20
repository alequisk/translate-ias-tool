import sys
from src.decoder import Decoder

try:
  file = open(sys.argv[1], 'r')
  decoder = Decoder(file)
  if len(sys.argv) == 3:
    output_file = open(sys.argv[2], "w")
    decoder.handle(output_file)
  else:
    decoder.handle()
except IndexError:
  print("You must to pass the input file to use translate IAS tool.")
except FileNotFoundError:
  print(f"File '{sys.argv[1]}' don't exists.")
