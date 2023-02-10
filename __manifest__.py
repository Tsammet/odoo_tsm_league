# -*- coding: utf-8 -*-
{
    'name': 'League Of Legends',
    'version': '1.0',
    'website': 'https://www.driverp.com',
    'author': 'DrivErp',
    'category': 'Extra Tools',
    'sequence': 50,
    'summary': 'Modulo de League of Legends',
    'depends': ['base'],
    'description': '''
        estadisticas de las partidas
    ''',
    'data': [
        'views/tsm_league_menu.xml',
        'views/tsm_champs_view.xml',
        'views/tsm_game_view.xml',
        'views/tsm_lane_game_view.xml',
        'views/tsm_estadistica_view.xml',
        'security/ir.model.access.csv',
        
    ],
    'demo': [],
    'test': [],
    'application': True,
}
