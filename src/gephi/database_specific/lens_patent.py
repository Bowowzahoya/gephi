# -*- coding: utf-8 -*-

from ..document_export_mixins import NodeGetterMixin, EdgeGetterMixin
from ..constants import LENS_ID_COL, TITLE_COL

class NodeGetter(NodeGetterMixin):
    MAX_EXPORT_LENGTH = 50_000
    MARGIN = 10
    CONTENT_COL = TITLE_COL
    
    def __init__(self, *args, **kwargs):
        super(NodeGetter, self).__init__(*args, **kwargs)
    
class EdgeGetter(EdgeGetterMixin):
    ID_COL = LENS_ID_COL
    
    def __init__(self, *args, **kwargs):
        super(EdgeGetter, self).__init__(*args, **kwargs)




    
    

