import ssindex as SIdx
from ssresult import SSResultSet

class SSTable():
    def __init__(self):
        self._storage = {}
        self._indexs = {}
        self._colomns = []
        self._col_name = {}
        self._next_ID = 0

    
    def addIndex( self, idx_col, name = None ):
        ''' idx_col could be index of column or list index of column
        '''
        import types
        idx = None
        if type( idx_col ) == types.ListType:
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

    def addIndexByName( self, lstColName, name = None ):
        idxRow = []
        for n in lstColName:
            i = self._col_name.get( n )
            if n == None:
                self.onLog( 0, n, "index not found column '%s'"%n )
            idxRow.append( i )
        return addIndex( self, idxRow, name )        

    def addRow( self, row ):
        rowIdx = self._next_ID
        self._storage[rowIdx] = list(row)
        self._next_ID += 1

        self.onLog( rowIdx, row, "insert" )
        for k,v in self._indexs.items():
            v.registerRow( rowIdx, row )

    def findRowOne( self, idxName, keyValue ):
        idx = self._indexs.get( idxName )
        if not idx :
            return None
        inRs = []
        rs = idx.getIndexRef( keyValue, inRs )
        return SSResultSet( self, inRs )

    def findRow( self, idxName, keyValue, filterlist = None, sortList = None, 
                                          limit = None, group = None ):
        import types
        idx = idxName
        if type(idx) == types.StringType:
            idx = self._indexs.get( idxName )
            if not idx :
                return None
        rs = []
        if type( keyValue ) != types.ListType:
            keyValue = [keyValue]
        idx.getIndexRef( keyValue, rs )

        # filter
        # sort
        # group
        
        return self._rs_to_Result( rs )
    
    def _rs_to_Result( self, rs ):
        import ssresult
        pkg = ssresult.SSResultSet( self, rs )    
        return pkg

    def row( self, idx ):
        return self._storage.get( idx )
        
    def _getAllIndex( self, idxList ):
        for k, v in self._storage.items():
            idxList.insert( k )
        
       

def GenRow( row, tag ):
    del row[0:len(row)]
    tag = str(tag)
    row.append( tag +"-1" );
    row.append( tag +"-2" );
    row.append( tag +"-3" );
    row.append( tag +"-4" );
    row.append( tag +"-5" );
    row.append( tag +"-6" );



def _TestSimpleTable():
    theTable = SSTable()
    pIndex = theTable.addIndex( 0, 'idx1' );
    vCol = [ 0, 1 ]
    pIndex3 = theTable.addIndex( vCol, 'idx2' );

    vRow = []
    GenRow( vRow, 0 );
    theTable.addRow( vRow );
    GenRow( vRow, 1 );
    theTable.addRow( vRow );
    theTable.addRow( vRow );
    GenRow( vRow, 2 );
    theTable.addRow( vRow );

    resultRow=[]
    resultRow = theTable.findRow( "idx1", "1-1")
    for x in resultRow:
        print x

    theKey = ["1-1"]
    #theTable.findRow( pIndex2, theKey );
    theTable.findRow( pIndex3, theKey );
    theTable.findRow( 0, "0-1" );
    resultRow=[]
    theTable.findRow( 0, "2-1" );
    resultRow=[]
    theTable.findRow( 0, "3-1");


if __name__ == '__main__':
    _TestSimpleTable()
