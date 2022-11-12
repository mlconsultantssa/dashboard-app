from typing import NamedTuple

class FilterInput(NamedTuple):
    '''Named tuple for filter inputs'''
    name: str
    component_id: str
    component_property: str = 'value'
