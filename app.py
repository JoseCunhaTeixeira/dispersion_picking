from dash import Dash

from callbacks import register_callbacks
from layout import create_layout

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = create_layout()

register_callbacks(app)

if __name__ == "__main__":
    app.run(port=8052)
