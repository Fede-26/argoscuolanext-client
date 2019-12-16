#!/usr/bin/env python3
import pickle
import pprint
pp = pprint.PrettyPrinter(indent=4)
import sys
sys.path.append("../modules")
import gestdati as gsd

pp.pprint(gsd.get_credentials())
