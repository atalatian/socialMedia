from .models import UserJoin


class auth:
    def __init__(self):
        self.state = {
            'loggedIn': False,
            'pk': None,
        }

    def getState(self):
        return self.state

    def setState(self, loggedIn, pk):
        state = self.state.copy()
        state['loggedIn'] = loggedIn
        state['pk'] = pk
        self.state = state


if __name__ == '__main__':
    pass
else:
    authentication = auth()
