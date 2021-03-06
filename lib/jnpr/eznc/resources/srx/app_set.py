
import pdb

# 3rd-party
from lxml.builder import E 

# module packages
from ..resource import Resource
from ... import jxml as JXML

class ApplicationSet( Resource ):
  """
  [edit applications application-set <name>]
  """

  PROPERTIES = [
    'description',
    'app_list',     'app_list_adds',    'app_list_dels',
    'appset_list',  'appset_list_adds', 'appset_list_dels'
  ]

  def _xml_at_top(self):
    return E.applications(E('application-set', (E.name( self._name ))))

  def _xml_at_res(self, xml):
    return xml.find('.//application-set')

  def _xml_to_py(self, has_xml, has_py ):
    Resource._r_has_xml_status( has_xml, has_py )    
    Resource.copyifexists( has_xml, 'description', has_py )
    has_py['app_list'] = []
    has_py['appset_list'] = []

    # each of the <application> elements
    for this in has_xml.xpath('application'):
      has_py['app_list'].append(this.find('name').text)

    # sets can contain other sets too ...
    for this in has_xml.xpath('application-set'):
      has_py['appset_list'].append(this.find('name').text)

  ##### -----------------------------------------------------------------------
  ##### XML property writers
  ##### -----------------------------------------------------------------------

  ### -------------------------------------------------------------------------
  ### application list
  ### -------------------------------------------------------------------------

  def _xml_change_app_list( self, xml ):
    self._xml_list_property_add_del_names( xml,
      prop_name='app_list',element_name='application')
    return True

  def _xml_change_app_list_adds( self, xml ):
    for this in self.should['app_list_adds']:
      xml.append(E.application(E.name(this)))
    return True

  def _xml_change_app_list_dels( self, xml ):
    for this in self.should['app_list_dels']:
      xml.append(E.application(JXML.DEL, E.name(this)))
    return True

  ### -------------------------------------------------------------------------
  ### application-set list
  ### -------------------------------------------------------------------------

  def _xml_change_appset_list( self, xml ):
    if None == self.should.get('appset_list'): self['appset_list'] = []

    (adds,dels) = Resource.diff_list( self.has.get('appset_list',[]), self.should['appset_list'])

    for this in adds: xml.append(E('application-set',E.name(this)))
    for this in dels: xml.append(E('application-set', JXML.DEL, E.name(this)))
    return True

  def _xml_change_appset_list_adds( self, xml ):
    for this in self.should['appset_list_adds']:
      xml.append(E('application-set',E.name(this)))
    return True    

  def _xml_change_appset_list_dels( self, xml ):
    for this in self.should['appset_list_dels']:
      xml.append(E('application-set', JXML.DEL, E.name(this)))
    return True    

  ##### -----------------------------------------------------------------------
  ##### Resource List, Catalog
  ##### -- only executed by 'manager' resources
  ##### -----------------------------------------------------------------------

  def _r_list(self):
    got = self._junos.rpc.get_config(
      E.applications(E('application-set', JXML.NAMES_ONLY)))

    self._rlist = [ this.text for this in got.xpath('.//name')]

  def _r_catalog(self):
    got = self._junos.rpc.get_config(
      E.applications(E('application-set')))

    for this in got.xpath('.//application-set'):
      name = this.find('name').text
      this_py = {}
      self._xml_to_py( this, this_py )
      self._rcatalog[name] = this_py
