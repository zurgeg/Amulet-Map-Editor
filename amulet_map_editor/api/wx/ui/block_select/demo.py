import wx
from amulet_map_editor.api.wx.ui.block_select.block_select import (
    demo as block_select_demo,
)
from amulet_map_editor.api.wx.ui.block_select.block_define import (
    demo as block_define_demo,
)
from amulet_map_editor.api.wx.ui.block_select.multi_block_define import (
    demo as multi_block_define_demo,
)
from amulet_map_editor.api.wx.ui.block_select.properties.demo import (
    demo as properties_demo,
)


def demo():
    """
    Show a demo version of the UI.
    An app instance must be created first.
    """
    block_select_demo()
    block_define_demo()
    multi_block_define_demo()
    properties_demo()


if __name__ == "__main__":

    def main():
        app = wx.App()
        demo()
        app.MainLoop()

    main()