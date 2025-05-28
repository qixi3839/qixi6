import random

class BlackjackGame:
    def __init__(self):
        self.players = {}
        self.deck = []

    def add_player(self, user_id, username):
        if user_id not in self.players:
            self.players[user_id] = {"username": username, "cards": [], "stand": False}

    def start_game(self):
        self.deck = self._generate_deck()
        for player in self.players.values():
            player["cards"] = [self.deck.pop(), self.deck.pop()]
            player["stand"] = False

    def get_player_initial_cards(self, user_id):
        cards = self.players[user_id]["cards"]
        return f"初始牌：{self._format_cards(cards)} 点数：{self._calculate_points(cards)}"

    def player_hit(self, user_id):
        if self.players[user_id]["stand"]:
            return "你已经选择停牌，不能再要牌了。"
        card = self.deck.pop()
        self.players[user_id]["cards"].append(card)
        score = self._calculate_points(self.players[user_id]["cards"])
        if score > 21:
            return f"你抽到了 {card}，当前点数 {score}，爆了！"
        return f"你抽到了 {card}，当前点数 {score}。"

    def player_stand(self, user_id):
        self.players[user_id]["stand"] = True
        score = self._calculate_points(self.players[user_id]["cards"])
        return f"你选择停牌，最终点数：{score}。等待其他玩家操作..."

    def _calculate_points(self, cards):
        total = 0
        aces = 0
        for card in cards:
            if card in ["J", "Q", "K"]:
                total += 10
            elif card == "A":
                aces += 1
                total += 11
            else:
                total += int(card)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def _format_cards(self, cards):
        return "、".join(cards)

    def _generate_deck(self):
        base = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]
        return base * 4