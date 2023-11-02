from py2neo import Graph, Node, Relationship, apoc


class Game:
    def init(self):
        self.graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))


    def create_player(self, name):
        player = Node("Player", id=self.player_id, name=name)
        self.graph.create(player)
        self.id = apoc.create.uuid()

    def update_player(self, id, new_name):
        query = "MATCH (p:Player {id: $id}) SET p.name = $new_name"
        self.graph.run(query, id=id, new_name=new_name)

    def delete_player(self, id):
        query = "MATCH (p:Player {id: $id}) DELETE p"
        self.graph.run(query, id=id)

    def create_match(self, players, results):
        match = Node("Match", id=self.match_id)
        self.graph.create(match)
        self.id = apoc.create.uuid()

        for player, result in zip(players, results):
            player_node = Node("Player", id=player["id"])
            relationship = Relationship(player_node, "PARTICIPATED_IN", match, result=result)
            self.graph.create(relationship)

    def get_players(self):
        query = "MATCH (p:Player) RETURN p.name"
        result = self.graph.run(query)
        return [record["p.name"] for record in result]

    def get_match(self, match_id):
        query = "MATCH (m:Match {id: $match_id}) RETURN m"
        result = self.graph.run(query, match_id=match_id).single()
        return dict(result["m"])

    def get_player_history(self, player_id):
        query = "MATCH (p:Player {id: $player_id})-[:PARTICIPATED_IN]->(m:Match) RETURN m"
        result = self.graph.run(query, player_id=player_id)
        return [dict(record["m"]) for record in result]

# Populando e usando a classe

game = Game()

# Criar jogadores
game.create_player("Player 1")
game.create_player("Player 2")

# Atualizar jogador
game.update_player("Player 1", "New Player 1")

# Excluir jogador
game.delete_player("Player 2")

# Criar partida
game.create_match(["New Player 1", "Player 3"], [10, 5])

# Obter lista de jogadores
players = game.get_players()
print(players)

# Obter informações sobre uma partida
match = game.get_match(1)
print(match)

# Obter histórico de partidas de um jogador
player_history = game.get_player_history("New Player 1")
print(player_history)
