from discord import ui


class VoteView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)


class YesNoVoteView(VoteView):
    def __init__(self):
        super().__init__()
        self.add_item(YesVoteButton())
        self.add_item(NoVoteButton())


class VoteButton(ui.Button):  # type: ignore
    def __init__(self):
        pass


class YesVoteButton(VoteButton):
    pass


class NoVoteButton(VoteButton):
    pass
