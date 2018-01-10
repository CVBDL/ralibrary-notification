import sys
import os

# Add project top level directory to search path.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..'))

from ralibrarynotification.main import main


if __name__ == '__main__':
    main()
