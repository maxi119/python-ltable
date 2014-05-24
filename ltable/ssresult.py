import types
from pprint import pprint

class SSResultSet():
    def __init__(self, src, idxList ):
        self._res = idxList
        self._src = src
        self._idx = 0

    def __getitem__(self, idx):
        return self._src.row( self._res[idx] )

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

    def to_list( self ):
        rs = []
        for r in self:
        # PT DL
            row =[]
            for k, v in r.items():
                row.append( v )
            rs.append( tuple(row) )
        return rs        

    def group( self, group_columns = () ):
        group_rs = SSResultGroup( group_columns )
        for i in self._res:
            row = self._src.row(i)
            if type(group_columns) in ( types.ListType, types.TupleType):
                g_name = []
###TY LD
                for gcol in group_columns:
                    g_name.append( row[ gcol ] )
                if not group_rs.get( g_name ):
                    group_rs[ g_name ] = []
                group_rs[ tuple( g_name) ].append( dict(row) ) # make copy
            else:
                g_name = row.get( group_columns )
                if not group_rs.get( g_name ):
                    group_rs[ g_name ] = []
                group_rs[ g_name ].append( dict(row) ) # make copy
                

        return group_rs

    def sort( self, sortList, reverse = False ):      # sort
        class _sort():
            def __init__(self, src ):
                self._sortlist = sortList
                self._src = src
            def _make( self, lhs, rhs ):
                rowL = self._src._storage.get( lhs )
                rowR = self._src._storage.get( rhs )
                
                pairs = self._sortlist
                last = len(pairs)-1
                for i in xrange( len(pairs) ):
                    k, v = pairs[i]
                    col = k
                    colL = rowL[col]
                    colR = rowR[col]
                    if i == last:
                        return v( colL, colR )
                    if v( colL, colR ) < 0:
                        return -1;
                    return 1                        
                return -1

        newList = sorted( self._res, _sort( self._src )._make, reverse=reverse )
        return SSResultSet( self._src, newList )

    class _Iter():
        def __init__(self, rs ):
            self._rs = rs
            self._idx = 0
        def next( self ):
            if len(self._rs) <= self._idx:
                raise StopIteration
            self._idx +=1            
            return self._rs[ self._idx-1 ]


class SSResultGroup(dict):
    def __init__(self, group ):
        self._group = group
        super( SSResultGroup, self).__init__()

    @property
    def group_name(self):
        return self._group

    def head( self, icount ):
        ''' flat all items into a list
        '''
        if icount<=0:
            icount = None   # all 

        rs = []
        for k, v in self.items():            
            rs.extend( v[0:icount] )
        return rs


