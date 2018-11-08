

EXIT              = 0
BREAKPARENT       = 1
CONTINUEPARENT    = 2

class EXC(Exception):
    def __init__(self, blockname, action=EXIT):
        super().__init__("This exception surfaced because there was no except-clause that handled the block-name \"{}\"".format(blockname))
        self.blockname=blockname
        self.action=action
    def handleBlock(self, blockname=None):
        if not (blockname is None) and (blockname!=self.blockname):
          raise
        return self.action



"""
Usage:


# Import with whatever alias you like
import CodeblockControl as codeblock




#[[[<<BLOCKNAME>>-------------------------------------------
try:

    raise codeblock.EXC('BLOCKNAME')
    raise codeblock.EXC('BLOCKNAME', codeblock.EXIT)
    raise codeblock.EXC('BLOCKNAME', codeblock.BREAKPARENT)
    raise codeblock.EXC('BLOCKNAME', codeblock.CONTINUEPARENT)

# Put this except-clause above ordinary error-exception clauses
except codeblock.EXC as EXC:
    action= EXC.handleBlock('BLOCKNAME')
    if action==codeblock.BREAKPARENT: break         # Can be left out if not inside break-able block
    if action==codeblock.CONTINUEPARENT: continue   # Can be left out if not inside continue-able block

#]]]<<BLOCKNAME>>-------------------------------------------

"""
