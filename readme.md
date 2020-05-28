# Message decoding based on standard location
## Requirements

Python 3.6 Packages

* numpy
* itertools
* pickle
* argparse

## Usage

```
python run.py [-h] {generate, encode, decode} ...
```

optional arguments: \
  ***-h, --help*** - show this help message and exit

***generate*** -  Generate linear code with given parameters \
***encode*** - Encode message with an error \
***decode*** - Find error and decode message

```
python run.py generate [-h] -r R -n N -p P -o OUT_FILE
```

optional arguments: \
  ***-h, --help*** -  show this help message and exit \
  ***-r R***  -  number of test characters \
  ***-n N*** - desired maximum length of a message block transmitted through a communication channel \
  ***-p P*** -  probability of an error in the communication channel \
  ***-o OUT_FILE*** -  output file with information for coder and decoder

```
python run.py encode [-h] -i IN_FILE -m MESSAGE [-e ERROR]
```

optional arguments: \
  ***-h, --help*** -  show this help message and exit \
  ***-i IN_FILE*** -  file with information for coder \
  ***-m MESSAGE*** -  message to encode \
  ***-e ERROR*** -   error to add to encoded message

```
python run.py decode [-h] -i IN_FILE -m MESSAGE
```

optional arguments: \
  ***-h, --help*** - show this help message and exit \
  ***-i IN_FILE*** -  file with information for decoder \
  ***-m MESSAGE***  -message to decode

