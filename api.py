# Use event-driven API
class BaseClass(object):

    def __init__(self, classtype):
        self._type = classtype

    def __repr__(self):
        return self._type

    def __hash__(self):
        return hash(str(self.__class__) + ": " + str(self.__dict__))

def ClassFactory(name, argnames,BaseClass=BaseClass):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in argnames:
                raise TypeError("argument {} not valid for {}".format(key, self.__class__.__name__))
            setattr(self, key, value)
        BaseClass.__init__(self, name)

    newclass = type(name, (BaseClass,), {"__init__": __init__})
    return newclass

class SmartBoardMessage():
    NEW_POSITION = ClassFactory(EventApi.RENDER_SCREEN, ["xmlData"])

class GameEventApi():
    PIECE_MOVED = 'EVT_PIECE_MOVED'
    
    
class GameEvent():
    PIECE_MOVED = ClassFactory(EventApi.PIECE_MOVED, ['newboardArray'])
