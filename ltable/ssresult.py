

class SSResultSet():
    def __init__(self, src, idxList ):
        self._res = idxList
        self._src = src
        self._idx = 0

    def __getitem__(self, idx):
        return self._src.row( idx )

    def clear( self ):
        self._res = []

    def __iter__(self):        
        return SSResultSet._Iter(self)

    def __len__(self):
        return len(self._res)

    def getRowDict(self, irow ):
        if irow >= len( self._res ):
            return None
        return self._src.row_dict( self._res[ irow ] )
        

    class _Iter():
        def __init__(self, rs ):
            self._rs = rs
            self._idx = 0
        def next( self ):
            if len(self._rs) <= self._idx:
                raise StopIteration
            self._idx +=1            
            return self._rs[ self._idx-1 ]

