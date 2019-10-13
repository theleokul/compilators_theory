# Syntax driven translator

## Installation
Requirements: python 3.\*, pandas. I guess, you have python 3.* with command `python`.

1. Clone repository and move to it

### With virtual environment
2. Create environment `python -m virtualenv venv` (If you haven't virtualenv module, install it with `pip install virtualenv`)
3. Activate environment `. venv/bin/activate`      
3. Download all dependencies `pip install -r requirements.txt`
4. Run program `./sdt.py -s 'a+b*c'`

### Without virtual environment (Be sure you have pandas installed in global python)
2. Run program `./sdt.py -s 'a+b*c'`

## Info
You can change grammatics in `grammatics.py`