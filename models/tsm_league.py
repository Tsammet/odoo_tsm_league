from odoo import models, fields, api
from odoo.exceptions import UserError

STYLE = [
    ('AD', 'AD'),
    ('AP', 'AP'),
    ('HYBRID', 'HYBRID'),
    ('TANK', 'TANK'),
]


class TsmLeagueChamps(models.Model):
    _name = 'tsm.league.champs'
    _description = 'Campeones de League of Legends'

    name = fields.Char('Nombre del Campeón')
    lane = fields.Many2many('tsm.lane.game', string="Carril")
    style = fields.Selection(STYLE, 'Estilo Champ')
    winrate_champ = fields.Float('Winrate Campeón', compute="winrate_action")
    count_play_champ = fields.Integer('Jugabilidad', compute = "count_play_champ_fun")
    image = fields.Binary('image')

    @api.one
    def count_play_champ_fun(self):

        champions = self.env['tsm.league.champs'].search([])

        for champ in champions:
            games = self.env['tsm.game'].search([('champ', '=', champ.id)])
            total_games = len(games)

            champ.count_play_champ = total_games

                

    @api.one
    def winrate_action(self):
        champions = self.env['tsm.league.champs'].search([])

        for champion in champions:
            games = self.env['tsm.game'].search([('champ', '=', champion.id)])
            total_games = len(games)
            victories = 0

            if total_games > 0:

                for g in games:
                    if g.res_game == "VICTORY":
                        victories += 1

                champion.winrate_champ = (victories / total_games) * 100 

            else:

                champion.winrate_champ = 0

RES_GAME = [
    ('VICTORY', 'VICTORY'),
    ('DEFEAT', 'DEFEAT'),
]


class TsmGame(models.Model):
    _name = "tsm.game"
    _description = "Partida jugada"

    champ = fields.Many2one('tsm.league.champs', 'Campeón')
    enemy = fields.Many2one('tsm.league.champs', 'Campeón Enemigo' )
    duration = fields.Float('Duración de la partida')
    lane = fields.Many2one('tsm.lane.game', 'Carril Jugado')
    res_game = fields.Selection(RES_GAME, 'Resultado Partida')
    kills = fields.Integer('Asesinatos')
    death = fields.Integer('Muertes')
    assists = fields.Integer('Asistencias')
    kda = fields.Float('KDA', compute="res_kda")
    winrate = fields.Float('WinRate', compute="winrate_accion")

    @api.one
    def winrate_accion(self):
        games = self.env['tsm.game'].search([])
        total_games = len(games)
        victorias = 0

        for g in games:
            if g.res_game == "VICTORY":
                victorias += 1

        self.winrate = (victorias / total_games) * 100

    @api.one
    def res_kda(self):
        res_ka = self.kills + self.assists
        self.kda = res_ka / self.death


LANE_GAME = [
    ('TOP', 'TOP'),
    ('JG', 'JG'),
    ('MID', 'MID'),
    ('ADC', 'ADC'),
    ('SUP', 'SUP'),
]


class TsmLaneGame(models.Model):
    _name = "tsm.lane.game"
    _description = "Carril que se juega"
    _rec_name = 'lane_game'

    lane_game = fields.Selection(LANE_GAME, 'Carril')
    winrate_lane = fields.Float('Winrate Carril', compute="winrate_action")
    

    @api.one
    def winrate_action(self):

        lanes = self.env['tsm.lane.game'].search([])


        for lane in lanes:

            games = self.env['tsm.game'].search([('lane', "=", lane.id)])
            total_games = len(games)
            victorias = 0

            if total_games > 0:

                for game in games:
                    if game.res_game == "VICTORY":
                        victorias += 1

                lane.winrate_lane = (victorias / total_games) * 100 
                
            else: 
                
                lane.winrate_lane = 0
            

class TsmEstadistica(models.Model):
    _name = "tsm.estadistica"
    _description = "quienes tienen mejor Winrate de champs y peor winrate"

    estadistica_line = fields.One2many('tsm.estadistica.line', 'estadistica', 'Detalles')


    
    def winrate_champs_fun(self):
        champ_enemy = self.env['tsm.league.champs'].search([])

        champ_enemy_victories = []

        for champ in champ_enemy:
            games = self.env['tsm.game'].search([('enemy','=', champ.id)])
            victorias = 0
            for gm in games:
                if gm.res_game == 'VICTORY':
                    victorias += 1
            data = {
                'champ_enemy' : champ.id,
                'qty_victory' : victorias
            }
            champ_enemy_victories.append(data)

            self.estadistica_line = [(0,0,x) for x in champ_enemy_victories]


    def worst_winrate_champs_fun(self):
        champ_enemy = self.env['tsm.league.champs'].search([])

        champ_enemy_defeat = []

        for champ in champ_enemy:
            games = self.env['tsm.game'].search([('enemy','=', champ.id)])
            victorias = 0
            for gm in games:
                if gm.res_game == 'DEFEAT':
                    victorias += 1
            data = {
                'champ_enemy' : champ.id,
                'qty_defeat' : victorias
            }
            champ_enemy_defeat.append(data)

            self.estadistica_line = [(0,0,x) for x in champ_enemy_defeat]
                


class TsmEstadisticaLine(models.Model):
    _name = "tsm.estadistica.line"

    champ_enemy = fields.Many2one('tsm.league.champs', 'Enemigo')
    qty_victory = fields.Integer('Cantidad Victorias')
    qty_defeat = fields.Integer('Cantidad Derrotas')
    estadistica = fields.Many2one('tsm.estadistica')