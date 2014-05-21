from ltable import *


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