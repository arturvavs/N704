from dash import Dash


app = Dash(
    __name__,
    pages_folder='pages', 
    use_pages=True, 
    suppress_callback_exceptions=True, 
    external_stylesheets=['assets/styles.css?v=1'], 
    assets_folder='assets'
    )



if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port='8051',
        debug=True, 
        dev_tools_ui=False
        )