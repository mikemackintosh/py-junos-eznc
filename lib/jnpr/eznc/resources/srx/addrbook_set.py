# 3rd-party modules
from lxml.builder import E 

# module packages
from ... import jxml as JXML
from .. import Resource

class ZoneAddrBookSet( Resource ):
  """
  [edit security zone security-zone <zone> address-book address-set <name>]

  ~! WARNING !~
  This resource is managed only as a child of the :ZoneAddrBook:
  resource.  Do not create a manager instance of this class directly

  Notes
  -------------------------------------------------------------------
    :self._name: is the address-set name

    :self.P: is the parent ZoneAddrBook object, 
      whose _name is the security zone 
  """
  PROPERTIES = [
    'description',
    'addr_list',        # list of address items
    'set_list',         # sets can contain a list of sets
  ]

  def _xml_at_top(self):
    return E.security(E.zones(
      E('security-zone', 
        E.name(self.P._name),
        E('address-book', 
          E('address-set',E.name(self._name))
        )
      )
    ))

  ##### -----------------------------------------------------------------------
  ##### XML reading
  ##### -----------------------------------------------------------------------

  def _xml_at_res(self, xml):
    return xml.find('.//address-book/address-set')

  def _xml_to_py(self, as_xml, to_py ):
    Resource._r_has_xml_status( as_xml, to_py )
    Resource.copyifexists( as_xml, 'description', to_py )
    to_py['addr_list'] = [name.text for name in as_xml.xpath('address/name')]
    to_py['set_list'] = [name.text for name in as_xml.xpath('address-set/name')]

  ##### -----------------------------------------------------------------------
  ##### XML writing
  ##### -----------------------------------------------------------------------

  def _xml_change_addr_list( self, xml ):
    self._xml_list_property_add_del_names( xml,
      prop_name='addr_list', element_name='address')
    return True

  def _xml_change_set_list( self, xml ):
    self._xml_list_property_add_del_names( xml,
      prop_name='set_list',element_name='address-set')
    return True

  ##### -----------------------------------------------------------------------
  ##### Manager List, Catalog
  ##### -----------------------------------------------------------------------

  def _r_list(self):
    """
    list of address-book address-sets.  this list is managed by the
    parent object, so just use that, yo!
    """
    self._rlist = self.P['$sets']

  def _r_catalog(self):
    """
    catalog each of the address-sets
    """
    get = E.security(E.zones(
      E('security-zone', 
        E.name(self.P._name),
        E('address-book', 
          E('address-set')
        )
      )
    ))
    got = self.J.rpc.get_config(get)
    for adrset in got.xpath('.//address-set'):
      name = adrset.find('name').text
      self._rcatalog[name] = {}
      self._xml_to_py( adrset, self._rcatalog[name] )

