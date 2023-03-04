from dash import dcc, html

def render(id):
    # #clients = list(load_data()['camera_id'].unique())
    # clients = ['one-space-11', 'vumacam-14', 'itrack-21', 'navic-5', '-20', '-9', 'alpha-security-group-12', '-7', '-10', 'watcher-22', '-17', 'nimbus-24', 'cloudsell-25', '-8', 'maxi-security-18' ]
    
    # missing_urls = {'x': [], 'y': [], 'type': 'bar', 'name': 'Proportion missing image_url'}
    # missing_locations = {'x': [], 'y': [], 'type': 'bar', 'name': 'Proportion missing locations'}

    # tickvals = []
    # ticktext = []

    # client_ids = [i[-2:].replace('-', '') for i in clients]
    # for i, client_id in enumerate(client_ids):
    #     tickvals.append(i)
    #     ticktext.append(client_id)

    #     counts_missing, counts_whole  = load_missing_url_count(client_id)
    #     perc = counts_missing/(counts_whole + counts_missing)
    #     missing_urls['x'].append(i)
    #     missing_urls['y'].append(perc)

    #     counts_missing, counts_whole  = load_missing_location_count(client_id)
    #     perc = counts_missing/(counts_whole + counts_missing)
    #     missing_locations['x'].append(i)
    #     missing_locations['y'].append(perc)


    return html.Div(
        [
            dcc.Graph(id = id,
            figure={
                'data': [
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }),
        html.Div(id=id + '-initial-loader')
    ])
