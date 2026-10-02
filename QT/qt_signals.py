from PySide6.QtCore import QObject, Signal



class OBSBridge(QObject):

    status_changed = Signal(bool, bool)


obs_bridge = OBSBridge()
