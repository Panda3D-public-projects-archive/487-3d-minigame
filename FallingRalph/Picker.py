from pandac.PandaModules import *

class Picker:
    def __init__(self, parent=None, fromMask=BitMask32(0), collideWithGeom=False, intoMask=BitMask32(0)):
        if (parent==None):
            parent = camera
        self.cRay = CollisionRay()
        self.cNode = CollisionNode('PickRay')
        self.cNode.addSolid(self.cRay)
        self.cNode.setIntoCollideMask(intoMask)
        if collideWithGeom:
            fromMask = fromMask | GeomNode.getDefaultCollideMask()
        self.cNode.setFromCollideMask(fromMask)
        self.cNodePath = parent.attachNewNode(self.cNode)
#        self.cNodePath.show()
        self.cHandler = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(self.cNodePath,self.cHandler)
    
    def pick(self,traverseRoot=None):
        return self.pickFromScreen(base.mouseWatcherNode.getMouseX(),base.mouseWatcherNode.getMouseY(),traverseRoot)
    
    def pickFromScreen(self, screenX, screenY, traverseRoot=None):
       self.cRay.setFromLens(base.camNode,screenX,screenY)
       dir = self.cRay.getDirection()
       self.cRay.setDirection(dir)
       return self.__doPick(traverseRoot)

    def __doPick(self,traverseRoot=None):
        if (not traverseRoot):
            traverseRoot=render
            
        self.cTrav.traverse(traverseRoot)
        self.cHandler.sortEntries()
        for i in range(self.cHandler.getNumEntries()):
            entry = self.cHandler.getEntry(i)
            if (not (isinstance(entry.getIntoNode(),GeomNode) and entry.getIntoNodePath().isHidden()) and entry.hasSurfacePoint()):
                return entry

        return None
