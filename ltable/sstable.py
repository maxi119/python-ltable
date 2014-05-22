import ssindex as SIdx
from ssresult import SSResultSet

class SSTable():
    def __init__(self, columns = []):
        self._storage = {}  # data store here
        self._indexs = {}   # index by columns
        self._columns = []  # column name 
        self._next_ID = 0

    def __len__(self):
        return len(self._storage)

    @property
    def columns( self ):
        return self._solumns
    
    def addIndex( self, idx_col, name = None ):
        ''' idx_col could be index of column or list index of column
        '''
        import types
        idx = None
        if type( idx_col ) in (types.ListType, types.TupleType):
            idx = SIdx.SSIndex( idx_col, self, 0 )
        else:
            idx = SIdx.SSIndexM1( [idx_col], self, 0 )
        if name:
            self._indexs[name] = idx
        else:
            if not self._indexs.get(''):
                self._indexs[''] = []
            self._indexs[''].append( idx )
        return idx

    def onLog( self, p1, p2, p3 ):
        pass    
    
    def addRowByDict( self, row ):
        asList = [ None for i in xrange( self._columns ) ]
        for k,v in row.items():
            col = self._col_name.get( k )
            asList[col] = v
        self.addRow( row )

    def addRow( self, row ):
        import types
        rowIdx = self._next_ID
        if type( row ) == types.DictType:
            self._storage[rowIdx] = dict(row) # copy
        elif type( row ) in ( types.ListType, types.TupleType):
            self._storage[rowIdx] = list(row) # copy
        else:
            self.onLog( "addRow", "Not Support", type(row) )
            
        self._next_ID += 1

        self.onLog( rowIdx, row, "insert" )
        for k,v in self._indexs.items():
            v.registerRow( rowIdx, row )

    def findRowOne( self, idxName, keyValue, condition=None, format='dict' ):
        inRs = []
        self._findRow( idxName, keyValue, inRs )
                
        if condition:
            tempRs = list(inRs)
            del inRs[:]
            for irow in tempRs:
                row = self._storage.get( irow )
                for k, f in condition.items():
                    if f(row[k]):
                        inRs.append( irow )

        rs = SSResultSet( self, inRs )
        if format  == 'dict':
            return rs.getRowDict(0)
        return rs[0]

    def findRow( self, idxName, keyValue, filterlist = None, sortList = None, 
                                          limit = None, group = None ):
        import types
        inRs = []
        self._findRow( idxName, keyValue, inRs )
        # filter
        # sort
        if sortList:

            class _sort():
                def __init__(self, sortList, src ):
                    self._sortlist = sortList
                    self._src = src
                def _make( self, lhs, rhs ):
                    rowL = self._src._storage.get( lhs )
                    rowR = self._src._storage.get( rhs )
                    
                    pairs = self._sortlist.items()
                    last = len(pairs)-1
                    for i in xrange( pairs ):
                        k, v = pair[i]
                        col = self._scr._col_name.get( x )
                        colL = rowL[col]
                        colR = rowR[col]
                        if i == last:
                            return v( colL, colR )
                        if v( colL, colR ) < 0:
                            return -1;
                        return 1                        
                    return -1

            newList = sorted( inRs, _sort( sortList, self )._make )
            inRs = newList  # replace.

        # group
        if group:
            group_rs = {}
            for i in inRs:
                row = self._storage[i]
                if type(group) in ( types.ListType, types.TupleType):
                    g_name = []
###TY LD
                    for gcol in group:
                        g_name.append( row[ gcol ] )
                    group_rs[ tuple( g_name) ] = dict(row) # make copy
                else:
                    g_name = row[ group ] 
                    group_rs[ g_name ] = dict(row) # make copy
                    

            return group_rs
        
        rs = SSResultSet( self, inRs )
        return rs

    def removeRow( self, idxName, keyValue, condition = None):
        inRs = []
        self._findRow( idxName, keyValue, inRs )
        for i in inRs:
#            if not condition and not( condition() ):
#                continue
            row = self._storage.get( i )
            for k, v in self._indexs.items():
                v.unregisterRow(i, row )
            del self._storage[i]

    def _findRow( self, idxName, keyValue, rs ):
        import types
        idx = idxName
        if type(idx) == types.StringType:
            idx = self._indexs.get( idxName )
            if not idx :
                return None
        
        if type( keyValue ) not in (types.ListType, types.TupleType ):
            keyValue = [keyValue]
        idx.getIndexRef( keyValue, rs )


    def update( self, idxName, keyValue, newData, condition=None ):
        rs = []
        self._findRow( idxName, keyValue, rs )
        for idx in rs:
            row = self._storage.get( idx )
            if not condition or _IsMatch( condition ):
                self._update( idx, newData )

    def _update( self, irow, values ):                
        row = self._storage.get( irow )
        for k, v in values.items():
            ## TY LD
            #idxCol = self._col_name.get( k )
            row[k] = v
    
    def _rs_to_Result( self, rs ):
        import ssresult
        pkg = ssresult.SSResultSet( self, rs )    
        return pkg

    def row( self, idx ):
        return self._storage.get( idx )

    def row_dict( self, idx ):
        if len(self._columns) == 0:
            return self._storage.get(idx) 
        return dict( zip(self._columns, self._storage.get(idx) ) )

    def all( self ):
        return self._storage.values()
                

    def _getAllIndex( self, idxList ):
        for k, v in self._storage.items():
            idxList.insert( k )
        
       
