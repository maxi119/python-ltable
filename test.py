from ltable.sstable import *
from pprint import pprint
## import spdb ; spdb.start(0)

def testListStorage():
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
    _TestSimpleTable()

def testDictStorage():
    def GenRow( row, tag ):
        row.clear()
        tag = str(tag)
        row["col1"] = tag +"-1";
        row["col2"] = tag +"-2";
        row["col3"] = tag +"-3";
        row["col4"] = tag +"-4";
        row["col5"] = tag +"-5";
        row["col6"] = tag +"-6";



    def _TestSimpleTable():
        theTable = SSTable()
        pIndex = theTable.addIndex( 'col1', 'idx1' );
        vCol = [ "col1", "col2" ]
        pIndex3 = theTable.addIndex( vCol, 'idx2' );

        vRow = {}
        GenRow( vRow, 0 );
        theTable.addRow( vRow );
        GenRow( vRow, 1 );
        theTable.addRow( vRow );
        theTable.addRow( vRow );
        GenRow( vRow, 2 );
        theTable.addRow( vRow );

        print("all")
        pprint( theTable.all().to_list() )
        resultRow=[]
        theKey = ["1-1"]
        resultRow = theTable.findRow( "idx1", "1-1")
        pprint( resultRow.to_list() )

        theKey = ["1-1"]
        print( "find 1-1" )
        rs = theTable.findRow( pIndex3, theKey );
        pprint( rs.to_list() )

        print( "\nfind 0-1" )
        rs = theTable.findRow( "idx1", "0-1" );
        pprint( rs.to_list() )

        print( "\nfind 2-1" )
        rs = theTable.findRow( "idx1", "2-1" );
        pprint( rs.to_list() )

        print( "\nfind 3-1" )
        rs = theTable.findRow( "idx1", "3-1");
        pprint( rs.to_list() )

        rs = theTable.all()
        print( "\nsorted" )
        rs1 = rs.sort( [("col1",cmp), ("col2,cmp") ] )        
        pprint( rs1.to_list() )

        print( "\nsorted 2" )
        rs1 = rs.sort( [("col1",cmp)], reverse = True )        
        pprint( rs1.to_list() )

        print( "\nremove 2-1" )
        theTable.removeRow( "idx1", ("2-1") )
        rs = theTable.findRow( "idx1", "2-1" );
        pprint( rs.to_list() )

        print("\n Group")
        rs = theTable.findRow( "idx1", ("1-1") ).group("col1").head(0)
        pprint( rs.to_list() )

    _TestSimpleTable()
 
if __name__ == '__main__':
    testDictStorage()
    #testListStorage()
