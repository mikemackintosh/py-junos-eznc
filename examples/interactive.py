import pdb
from pprint import pprint as pp 
from lxml.builder import E 
from lxml import etree

# junos "ez" module
from jnpr.eznc import Netconf
from jnpr.eznc.exception import *

jdev = Netconf(user='jeremy', host='vsrx_cyan', password='jeremy1')
jdev.open()

## now play around with jdev object ...






