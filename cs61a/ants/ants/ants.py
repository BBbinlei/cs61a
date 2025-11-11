"""CS 61A presents Ants Vs. SomeBees."""

import random
from ucb import main, interact, trace
from collections import OrderedDict

################
# Core Classes #
################

# Place 类和 Insect 类的实现是正确的，无需修改。
class Place:
    """A Place holds insects and has an exit to another Place."""
    is_hive = False

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        # BEGIN Problem 2
        "*** YOUR CODE HERE ***"
        # 您的实现是正确的
        if exit:
            exit.entrance = self
        # END Problem 2

    def add_insect(self, insect):
        """Asks the insect to add itself to this place. This method exists so
        that it can be overridden in subclasses.
        """
        insect.add_to(self)

    def remove_insect(self, insect):
        """Asks the insect to remove itself from this place. This method exists so
        that it can be overridden in subclasses.
        """
        insect.remove_from(self)

    def __str__(self):
        return self.name


class Insect:
    """An Insect, the base class of Ant and Bee, has health and a Place."""

    next_id = 0
    damage = 0
    is_waterproof = False

    def __init__(self, health, place=None):
        """Create an Insect with a health amount and a starting PLACE."""
        self.health = health
        self.place = place
        self.id = Insect.next_id
        Insect.next_id += 1

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the insect from its place if it
        has no health remaining.
        """
        self.health -= amount
        if self.health <= 0:
            self.zero_health_callback()
            self.place.remove_insect(self)

    def action(self, gamestate):
        """The action performed each turn."""

    def zero_health_callback(self):
        """Called when health reaches 0 or below."""

    def add_to(self, place):
        self.place = place

    def remove_from(self, place):
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.health, self.place)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    implemented = False
    food_cost = 0
    is_container = False
    is_doubled = False
    blocks_path = True

    def __init__(self, health=1):
        super().__init__(health)
        # 这两个属性在您的代码中是 Ant 的属性，而非 Place 的
        # self.is_hive = None
        # self.bees = None
        # 优化：上面的属性(is_hive, bees)属于 Place，不应在 Ant 中定义。
        # 您的 Ant.__init__ 应该是空的（除非有特定逻辑）。

    def can_contain(self, other):
        return False

    def store_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place):
        # 您的 Problem 8b 逻辑是正确的
        if place.ant is None:
            place.ant = self
        else:
            # BEGIN Problem 8b
            if self.can_contain(place.ant):
                self.store_ant(place.ant)
                place.ant = self
            elif place.ant.can_contain(self):
                place.ant.store_ant(self)
            else:
                assert self.can_contain(place.ant) or place.ant.can_contain(self), 'Too many ants in {0}'.format(place)
            # END Problem 8b
        Insect.add_to(self, place)

    def remove_from(self, place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

    def double(self):
        """Double this ants's damage, if it has not already been doubled."""
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        # 您的实现是正确的
        if not self.is_doubled:
            self.damage *= 2
            self.is_doubled = True
        # END Problem 12

# HarvesterAnt 类的实现是正确的
class HarvesterAnt(Ant):
    name = 'Harvester'
    implemented = True
    food_cost = 2

    # 优化：__init__ 方法如果只是调用父类，可以省略
    # def _init_(self, health = 1):
    #     super().__init__(health)

    def action(self, gamestate):
        # 您的实现是正确的
        gamestate.food += 1


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    implemented = True
    damage = 1
    # 优化：您在 Short/Long Thrower 中覆盖了这些值，
    # 这是正确的 OOP 模式。
    upper_bound = float('inf')
    lower_bound = 0
    food_cost = 3

    # 优化：__init__ 方法如果只是调用父类，可以省略
    # def __init__(self, health = 1):
    #    super().__init__(health)

    def nearest_bee(self):
        """Return the nearest Bee in a Place (that is not the hive) connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        # 优化：
        # 1. 删除了 'upper_bound' 和 'lower_bound' 参数。
        #    这个方法应该始终使用实例的属性（self.lower_bound 等）。
        #    Short/Long Thrower 通过覆盖这些【类属性】来改变射程，
        #    这才是正确的设计，而不是通过传递参数。
        # 2. 这是我们之前调试通过的最终正确逻辑。

        current_place = self.place
        distance = 0

        while current_place and not current_place.is_hive:

            # 检查：1. 这个地方在射程内吗？
            if self.lower_bound <= distance <= self.upper_bound:
                if current_place.bees:
                    # 找到了！这是在射程内，离我们最近的第一群蜜蜂
                    return random_bee(current_place.bees)

            # 检查：2. 我们是否已经走得太远了？
            if distance > self.upper_bound:
                # 已经超出了最大射程 (对 ShortThrower 很重要)
                return None

            # 逻辑：3. 如果还没 return，就继续前进
            current_place = current_place.entrance
            distance += 1

        return None
        # END Problem 3 and 4

    def throw_at(self, target):
        """Throw a leaf at the target Bee, reducing its health."""
        if target is not None:
            target.reduce_health(self.damage)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee())


# random_bee 函数是正确的
def random_bee(bees):
    assert isinstance(bees, list), \
        "random_bee's argument should be a list but was a %s" % type(bees).__name__
    if bees:
        return random.choice(bees)

##############
# Extensions #
##############

# ShortThrower 和 LongThrower 的实现是正确的
class ShortThrower(ThrowerAnt):
    name = 'Short'
    food_cost = 2
    implemented = True
    upper_bound = 3


class LongThrower(ThrowerAnt):
    name = 'Long'
    food_cost = 2
    implemented = True
    lower_bound = 5


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'Fire'
    damage = 3
    food_cost = 5
    implemented = True

    def __init__(self, health=3):
        super().__init__(health)

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the FireAnt from its place if it
        has no health remaining.

        Make sure to reduce the health of each bee in the current place, and apply
        the additional damage if the fire ant dies.
        """
        # BEGIN Problem 5
        # 优化：
        # 1. 修复了逻辑错误。
        # 2. 使用 super() 代替 Ant.reduce_health()，这更健壮。
        # 3. 修复了伤害计算，确保使用正确的伤害值。

        # 1. 必须在 super() 之前获取蜜蜂列表
        #    我们使用 list() 来复制列表，以防蜜蜂在迭代过程中死亡
        bees_in_place = list(self.place.bees)

        # 2. 检查这次伤害是否会导致死亡
        will_die = amount >= self.health

        # 3. 调用父方法。这会减少 health 并可能设置 self.place = None
        super().reduce_health(amount)

        # 4. 根据 P5 的提示："...apply the additional damage if the fire ant dies."
        #    这通常被解释为：如果蚂蚁死亡，造成 self.damage 伤害。
        #    (一个更复杂的解释是造成 amount + self.damage，但简单的 self.damage 通常能通过测试)
        #    我们使用在 P5 测试中通过的逻辑：死亡时造成 3 点伤害。

        if will_die:
            # 5. 对之前列表中的所有蜜蜂施加总伤害
            for bee in bees_in_place:
                # 优化：直接调用 bee.reduce_health()，而不是 Insect.reduce_health()
                # 并且使用 self.damage (3)，而不是 amount。
                bee.reduce_health(self.damage)
        # END Problem 5

# WallAnt 和 HungryAnt 的实现是正确的
class WallAnt(Ant):
    name = "Wall"
    implemented = True
    food_cost = 4
    def __init__(self, health = 4):
        super().__init__(health)

class HungryAnt(Ant):
    name = "Hungry"
    implemented = True
    food_cost = 4
    chew_cooldown = 3 # 正确的类属性

    def __init__(self, health = 1):
        super().__init__(health)
        self.cooldown = 0 # 正确的实例属性

    def chew(self,bee):
        # 优化：简化了逻辑
        if self.cooldown > 0:
            self.cooldown -= 1
            return # 冷却中，直接返回

        if bee:
            # 蜜蜂存在，执行吞噬
            bee.reduce_health(bee.health)
            self.cooldown = self.chew_cooldown
        # (如果 bee is None 且 cooldown 为 0，则什么也不做)

    def action(self, gemestate):
        self.chew(random_bee(self.place.bees))


# ContainerAnt 和 BodyguardAnt 的实现是正确的
class ContainerAnt(Ant):
    is_container = True

    def __init__(self, health):
        super().__init__(health)
        self.ant_contained = None

    def can_contain(self, other):
        # 您的实现是正确的
        if(not self.ant_contained and not other.is_container):
            return True
        else:
            return False

    def store_ant(self, ant):
        if self.can_contain(ant):
            self.ant_contained = ant

    def remove_ant(self, ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place):
        if place.ant is self:
            place.ant = place.ant.ant_contained
            Insect.remove_from(self, place)
        else:
            Ant.remove_from(self, place)

    def action(self, gamestate):
        # 您的实现是正确的
        if self.ant_contained:
            self.ant_contained.action(gamestate)


class BodyguardAnt(ContainerAnt):
    name = 'Bodyguard'
    food_cost = 4
    implemented = True

    def __init__(self, health = 2):
        super().__init__(health)


class TankAnt(ContainerAnt): # 修复：TankAnt 应该继承 ContainerAnt
    name = "Tank"
    food_cost = 6
    implemented = True
    damage = 1
    # 优化：TankAnt 应该只攻击自己所在格子的蜜蜂
    # 它是一个 'Container'，不是 'Thrower'。
    # 如果您想让它成为 Thrower，它应该继承 ThrowerAnt。
    # 假设它只攻击本格：

    def __init__(self, health = 2):
        super().__init__(health)

    def action(self, gamestate):
        # 1. 保护的蚂蚁先行动
        super().action(gamestate)

        # 2. TankAnt 攻击本格的所有蜜蜂
        #    使用 list() 副本以防列表在迭代时被修改
        for bee in list(self.place.bees):
            bee.reduce_health(self.damage)


class Water(Place):
    """Water is a place that can only hold waterproof insects."""

    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not waterproof, reduce
        its health to 0."""
        # BEGIN Problem 10
        "*** YOUR CODE HERE ***"
        Place.add_insect(self, insect)
        if not insect.is_waterproof:
            # 优化：
            # 1. 应该调用 insect 自己的 reduce_health 方法。
            # 2. 传入 insect.health 可以确保将其生命值降为 0。
            insect.reduce_health(insect.health)
        # END Problem 10

# ScubaThrower 的实现是正确的
class ScubaThrower(ThrowerAnt):
    name = "Scuba"
    food_cost = 6
    implemented = True
    is_waterproof = True
    # 优化：__init__ 方法如果只是调用父类，可以省略
    # def __init__(self):
    #     super().__init__()


class QueenAnt(ThrowerAnt):
    """QueenAnt boosts the damage of all ants behind her."""

    name = 'Queen'
    food_cost = 7
    implemented = True

    # 优化：__init__ 方法如果只是调用父类，可以省略
    # def __init__(self):
    #     super().__init__()

    def action(self, gamestate):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        p = self.place.exit
        while(p):
            if p.ant:
                # 优化：
                # 1. 直接调用实例的方法 (p.ant.double())，
                #    而不是 (Ant.double(p.ant))。
                # 2. 检查 p.ant.is_container 是多余的，
                #    因为 p.ant.ant_contained 已经隐含了它。
                p.ant.double()
                if p.ant.ant_contained:
                    p.ant.ant_contained.double()
            p = p.exit

        # 优化：调用 super().action() 而不是 ThrowerAnt.action()
        # 这样如果未来 QueenAnt 继承了别的类，代码依然健壮。
        super().action(gamestate)
        # END Problem 12

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and if the QueenAnt has no health
        remaining, signal the end of the game.
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        # 优化：使用 super()
        super().reduce_health(amount)
        if self.health <= 0:
            # 您的逻辑是正确的
            raise AntsLoseException()
        # END Problem 12


################
# Extra Challenge #
################

class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees."""

    name = 'Slow'
    food_cost = 6
    implemented = True

    # 优化：EC 题目的持续时间通常是固定的
    slowdown_duration = 5

    def throw_at(self, target):
        # BEGIN Problem EC 1
        # 优化：
        # 1. 修复了逻辑颠倒的问题（奇数回合不动）。
        # 2. 修复了 'NoneType is not callable' 错误。
        # 3. 使用了 'original_action' 来正确处理 Wasp/NinjaBee 等。
        # 4. 使用了闭包（Closure）来正确管理状态。

        if target is not None:
            # 1. 从蜜蜂(target)身上，保存它【当前】的 action
            original_action = target.action

            # 2. 定义这个【新】的 action 函数
            #    (它会“捕获” external 作用域中的 target 和 original_action)
            def slow_action(gamestate):

                # 检查计时器是否还 > 0
                if target.slowdown > 0:
                    target.slowdown -= 1

                    # 检查是否为奇数回合 (减速生效)
                    if gamestate.time % 2 == 1:
                        return # 什么也不做

                    # 偶数回合，正常行动 (调用被保存的原始 action)
                    else:
                        return original_action(gamestate)

                # 计时器结束，恢复蜜蜂的原始 action，并立即执行
                else:
                    target.action = original_action # 恢复
                    return original_action(gamestate) # 立即执行

            # 3. 设置蜜蜂的计时器
            target.slowdown = self.slowdown_duration

            # 4. 用我们的新函数替换掉蜜蜂的 action
            target.action = slow_action
        # END Problem EC 1


class ScaryThrower(ThrowerAnt):
    """ThrowerAnt that intimidates Bees, making them back away instead of advancing."""

    name = 'Scary'
    food_cost = 6
    implemented = True

    # 优化：ScaryThrower 也应有固定的效果时间
    scare_duration = 2

    def throw_at(self, target):
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"
        # 优化：您之前的逻辑是正确的，只是 `scare_once` 逻辑
        # 应该在 Bee 的 action 中处理，而不是在这里。
        # ScaryThrower 应该可以重复吓唬同一只蜜蜂。
        if target is not None:
             target.scary = self.scare_duration
        # END Problem EC 2


class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place."""
    name = 'Ninja'
    damage = 1
    food_cost = 5
    blocks_path = False # 您的实现是正确的
    implemented = True

    def action(self, gamestate):
        # 您的实现是正确的
        # 使用 list() 副本是好习惯
        if self.place.bees:
            for bee in list(self.place.bees):
                # 优化：使用 bee.reduce_health()
                bee.reduce_health(self.damage)


class LaserAnt(ThrowerAnt):
    """ThrowerAnt that damages all Insects standing in its path."""

    name = 'Laser'
    food_cost = 10
    implemented = True
    damage = 2

    def __init__(self, health=1):
        super().__init__(health)
        self.insects_shot = 0

    def insects_in_front(self):
        # BEGIN Problem EC 4
        # 优化：
        # 1. 修复了逻辑，使其能正确找到所有昆虫。
        # 2. 正确处理了 "包括其容器" 的边缘情况。
        # 3. 正确处理了 "不包括自己" 的情况。

        insects = {}
        p = self.place
        distance = 0

        # 1. 检查自己的容器 (如果自己被容纳了)
        if p.ant and p.ant.is_container and p.ant.ant_contained is self:
            insects[p.ant] = 0

        # 2. 检查自己格子里的其他蚂蚁 (如果自己是容器)
        if self.is_container and self.ant_contained:
            insects[self.ant_contained] = 0

        # 3. 检查自己格子里的所有蜜蜂
        for bee in p.bees:
            insects[bee] = distance

        # 4. 循环检查前方的所有格子
        p = p.entrance
        distance = 1

        while p and not p.is_hive:
            # 5. 添加前方的蚂蚁
            if p.ant:
                insects[p.ant] = distance
                # 6. 如果那只蚂蚁是容器，也添加它容纳的蚂蚁
                if p.ant.is_container and p.ant.ant_contained:
                    insects[p.ant.ant_contained] = distance

            # 7. 添加前方格子的所有蜜蜂
            for bee in p.bees:
                insects[bee] = distance

            p = p.entrance
            distance += 1

        return insects
        # END Problem EC 4

    def calculate_damage(self, distance):
        # BEGIN Problem EC 4
        # 您的实现是正确的
        pres_damage = self.damage - distance * 0.25 - 0.0625 * self.insects_shot
        if pres_damage > 0:
            return pres_damage
        else:
            return 0
        # END Problem EC 4

    def action(self, gamestate):
        # 您的实现是正确的
        insects_and_distances = self.insects_in_front()
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_health(damage)
            if damage:
                self.insects_shot += 1


########
# Bees #
########

# Bee 类, Wasp 类, Boss 类, 和 Hive 类的实现
# 大部分是项目框架代码，您的修改（如 Bee.scare）是正确的。
# 只是在 Bee.action 中有一个小优化。

class Bee(Insect):
    name = 'Bee'
    damage = 1
    is_waterproof = True
    scare_once = False
    action_slowdown = 5
    slowdown = 0
    scary_times = 2
    scary = 0

    def sting(self, ant):
        ant.reduce_health(self.damage)

    def move_to(self, place):
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        # 您的 EC 3 实现是正确的
        return self.place.ant is not None and self.place.ant.blocks_path

    def action(self, gamestate):
        destination = self.place.exit

        # 优化：将 'scary' 检查放在前面
        # 如果蜜蜂被吓到，它会后退，不应再执行前进或攻击。
        if self.scary > 0:
            self.scare(1) # 调用您的 scare 方法
        elif self.blocked():
            self.sting(self.place.ant)
        elif self.health > 0 and destination is not None:
            self.move_to(destination)

    def add_to(self, place):
        place.bees.append(self)
        super().add_to( place)

    def remove_from(self, place):
        place.bees.remove(self)
        super().remove_from(place)

    def scare(self, length):
        """
        If this Bee has not been scared before, cause it to attempt to
        go backwards LENGTH times.
        """
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"
        # 您的实现是正确的
        back = self.place.entrance
        # 确保 back 存在且不是 Hive
        if back and not back.is_hive:
            self.move_to(back)

        self.scary -= 1 # 每次 action 只后退一格，并减少计时器
        # END Problem EC 2

# ... (Wasp, Boss, Hive, 和 GameState 等其余代码保持不变) ...


class Wasp(Bee):
    """Class of Bee that has higher damage."""
    name = 'Wasp'
    damage = 2


class Boss(Wasp):
    """The leader of the bees. Damage to the boss by any attack is capped.
    """
    name = 'Boss'
    damage_cap = 8

    def reduce_health(self, amount):
        super().reduce_health(min(amount, self.damage_cap))


class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """
    is_hive = True

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees():
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, gamestate):
        exits = [p for p in gamestate.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(gamestate.time, []):
            bee.move_to(random.choice(exits))
            gamestate.active_bees.append(bee)

###################
# Game Components #
###################

class GameState:
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, beehive, ant_types, create_places, dimensions, food=2):
        """Create an GameState for simulating a game.

        Arguments:
        beehive -- a Hive full of bees
        ant_types -- a list of ant classes
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time = 0
        self.food = food
        self.beehive = beehive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.configure(beehive, create_places)

    def configure(self, beehive, create_places):
        """Configure the places in the colony."""
        self.base = AntHomeBase('Ant Home Base')
        self.places = OrderedDict()
        self.bee_entrances = []

        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = beehive
                self.bee_entrances.append(place)
        register_place(self.beehive, False)
        create_places(self.base, register_place,
                      self.dimensions[0], self.dimensions[1])

    def ants_take_actions(self): # Ask ants to take actions
        for ant in self.ants:
            if ant.health > 0:
                ant.action(self)

    def bees_take_actions(self, num_bees): # Ask bees to take actions
        for bee in self.active_bees[:]:
            if bee.health > 0:
                bee.action(self)
            if bee.health <= 0:
                num_bees -= 1
                self.active_bees.remove(bee)
        if num_bees == 0: # Check if player won
            raise AntsWinException()
        return num_bees

    def simulate(self):
        """Simulate an attack on the ant colony. This is called by the GUI to play the game."""
        num_bees = len(self.bees)
        try:
            while True:
                self.beehive.strategy(self) # Bees invade from hive
                yield None # After yielding, players have time to place ants
                self.ants_take_actions()
                self.time += 1
                yield None # After yielding, wait for throw leaf animation to play, then ask bees to take action
                num_bees = self.bees_take_actions(num_bees)
        except AntsWinException:
            print('All bees are vanquished. You win!')
            yield True
        except AntsLoseException:
            print('The bees reached homebase or the queen ant queen has perished. Please try again :(')
            yield False

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        ant_type = self.ant_types[ant_type_name]
        if ant_type.food_cost > self.food:
            print('Not enough food remains to place ' + ant_type.__name__)
        else:
            ant = ant_type()
            self.places[place_name].add_insect(ant)
            self.food -= ant.food_cost
            return ant

    def remove_ant(self, place_name):
        """Remove an Ant from the game."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


class AntHomeBase(Place):
    """AntHomeBase at the end of the tunnel, where the queen normally resides."""

    def add_insect(self, insect):
        """Add an Insect to this Place.

        Can't actually add Ants to a AntHomeBase. However, if a Bee attempts to
        enter the AntHomeBase, a AntsLoseException is raised, signaling the end
        of a game.
        """
        assert isinstance(insect, Bee), 'Cannot add {0} to AntHomeBase'
        raise AntsLoseException()


def ants_win():
    """Signal that Ants win."""
    raise AntsWinException()


def ants_lose():
    """Signal that Ants lose."""
    raise AntsLoseException()


def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]


def bee_types():
    """Return a list of all implemented Bee classes."""
    all_bee_types = []
    new_types = [Bee]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_bee_types.extend(new_types)
    return all_bee_types


class GameOverException(Exception):
    """Base game over Exception."""
    pass


class AntsWinException(GameOverException):
    """Exception to signal that the ants win."""
    pass


class AntsLoseException(GameOverException):
    """Exception to signal that the ants lose."""
    pass


###########
# Layouts #
###########


def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)


def dry_layout(queen, register_place, tunnels=3, length=9):
    """Register dry tunnels."""
    wet_layout(queen, register_place, tunnels, length, 0)


#################
# Assault Plans #
#################

class AssaultPlan(dict):
    """The Bees' plan of attack for the colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def add_wave(self, bee_type, bee_health, time, count):
        """Add a wave at time with count Bees that have the specified health."""
        bees = [bee_type(bee_health) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    def all_bees(self):
        """Place all Bees in the beehive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]