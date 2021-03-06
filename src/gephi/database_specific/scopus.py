# -*- coding: utf-8 -*-

from ..document_export_mixins import NodeGetterMixin, EdgeGetterMixin
from ..constants import EID_COL, TITLE_COL

class NodeGetter(NodeGetterMixin):
    MAX_EXPORT_LENGTH = 20_000
    MARGIN = 10
    CONTENT_COL = TITLE_COL
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
class EdgeGetter(EdgeGetterMixin):
    ID_COL = EID_COL
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

