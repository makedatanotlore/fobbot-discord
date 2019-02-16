import random
from collections import namedtuple

Face = namedtuple('Face', 'name emoji pips swords skulls')
BLANK = Face('blank', '<:base_blank:545643568677519370>', 0, 0, 0)


class Die:
    faces = [BLANK]

    def __init__(self):
        self.active = BLANK

    async def roll(self):
        if await self.pushable():
            self.active = random.choice(self.faces)

    async def pushable(self):
        return self.active.swords == 0 and self.active.skulls == 0


class D6(Die):
    faces = [Face('d6_one', '<:d6_one:546326217385836565>', 1, 0, 1),
             Face('d6_two', '<:d6_two:546326217561997315>', 2, 0, 1),
             Face('d6_three', '<:d6_three:546326217633169408>', 3, 0, 1),
             Face('d6_four', '<:d6_four:546326217633300512>', 4, 0, 1),
             Face('d6_five', '<:d6_five:546326217545089024>', 5, 0, 1),
             Face('d6_six', '<:d6_six:546326217876570123>', 6, 0, 1)]


class Base(Die):
    faces = [Face('base_one', '<:base_one:545643569218584638>', 1, 0, 1),
             Face('base_two', '<:base_blank:545643568677519370>', 2, 0, 0),
             Face('base_three', '<:base_blank:545643568677519370>', 3, 0, 0),
             Face('base_four', '<:base_blank:545643568677519370>', 4, 0, 0),
             Face('base_five', '<:base_blank:545643568677519370>', 5, 0, 0),
             Face('base_six', '<:base_six:545643569298407444>', 6, 1, 0)]


class Skill(Die):
    faces = [Face('skill_one', '<:skill_blank:545643939139682314>', 1, 0, 0),
             Face('skill_two', '<:skill_blank:545643939139682314>', 2, 0, 0),
             Face('skill_three', '<:skill_blank:545643939139682314>', 3, 0, 0),
             Face('skill_four', '<:skill_blank:545643939139682314>', 4, 0, 0),
             Face('skill_five', '<:skill_blank:545643939139682314>', 5, 0, 0),
             Face('skill_six', '<:skill_six:545643939387146268>', 6, 1, 0)]


class Gear(Die):
    faces = [Face('gear_one', '<:gear_one:545646496691912704>', 1, 0, 1),
             Face('gear_two', '<:gear_blank:545646496586924035>', 2, 0, 0),
             Face('gear_three', '<:gear_blank:545646496586924035>', 3, 0, 0),
             Face('gear_four', '<:gear_blank:545646496586924035>', 4, 0, 0),
             Face('gear_five', '<:gear_blank:545646496586924035>', 5, 0, 0),
             Face('gear_six', '<:gear_six:545646496671072256>', 6, 1, 0)]


class D8(Die):
    faces = [Face('d8_one', '<:d8_blank:545646540782436365>', 1, 0, 0),
             Face('d8_two', '<:d8_blank:545646540782436365>', 2, 0, 0),
             Face('d8_three', '<:d8_blank:545646540782436365>', 3, 0, 0),
             Face('d8_four', '<:d8_blank:545646540782436365>', 4, 0, 0),
             Face('d8_five', '<:d8_blank:545646540782436365>', 5, 0, 0),
             Face('d8_six', '<:d8_six:545646541252329482>', 6, 1, 0),
             Face('d8_seven', '<:d8_six:545646541252329482>', 7, 1, 0),
             Face('d8_eight', '<:d8_eight:545646540996345866>', 8, 2, 0)]


class D10(Die):
    faces = [Face('d10_one', '<:d10_blank:545646579831275541>', 1, 0, 0),
             Face('d10_two', '<:d10_blank:545646579831275541>', 2, 0, 0),
             Face('d10_three', '<:d10_blank:545646579831275541>', 3, 0, 0),
             Face('d10_four', '<:d10_blank:545646579831275541>', 4, 0, 0),
             Face('d10_five', '<:d10_blank:545646579831275541>', 5, 0, 0),
             Face('d10_six', '<:d10_six:545646579412107265>', 6, 1, 0),
             Face('d10_seven', '<:d10_six:545646579412107265>', 7, 1, 0),
             Face('d10_eight', '<:d10_eight:545646579277627422>', 8, 2, 0),
             Face('d10_nine', '<:d10_eight:545646579277627422>', 9, 2, 0),
             Face('d10_ten', '<:d10_ten:545646579684605963>', 10, 3, 0)]


class D12(Die):
    faces = [Face('d12_one', '<:d12_blank:545646598093537282>', 1, 0, 0),
             Face('d12_two', '<:d12_blank:545646598093537282>', 2, 0, 0),
             Face('d12_three', '<:d12_blank:545646598093537282>', 3, 0, 0),
             Face('d12_four', '<:d12_blank:545646598093537282>', 4, 0, 0),
             Face('d12_five', '<:d12_blank:545646598093537282>', 5, 0, 0),
             Face('d12_six', '<:d12_six:545646598517161984>', 6, 1, 0),
             Face('d12_seven', '<:d12_six:545646598517161984>', 7, 1, 0),
             Face('d12_eight', '<:d12_eight:545646598961758208>', 8, 2, 0),
             Face('d12_nine', '<:d12_eight:545646598961758208>', 9, 2, 0),
             Face('d12_ten', '<:d12_ten:545646599141982208>', 10, 3, 0),
             Face('d12_eleven', '<:d12_ten:545646599141982208>', 11, 3, 0),
             Face('d12_twelve', '<:d12_twelve:545646600102477837>', 12, 4, 0)]
