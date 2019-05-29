import random
from collections import namedtuple

Face = namedtuple('Face', 'name emoji pips swords skulls')
BLANK = Face('blank', '<:base_blank:545643568677519370>', 0, 0, 0)


class Die:
    faces = [BLANK]
    countable = False

    def __init__(self):
        self.active = BLANK

    async def roll(self):
        if await self.pushable():
            self.active = random.choice(self.faces)

    async def pushable(self):
        return self.active.swords == 0 and self.active.skulls == 0


class D6(Die):
    faces = [Face('d6_one', '<:d6_one:583200701761585153>', 1, 0, 1),
             Face('d6_two', '<:d6_two:583200702403444736>', 2, 0, 1),
             Face('d6_three', '<:d6_three:583200702072094730>', 3, 0, 1),
             Face('d6_four', '<:d6_four:583200701644275713>', 4, 0, 1),
             Face('d6_five', '<:d6_five:583200702004854794>', 5, 0, 1),
             Face('d6_six', '<:d6_six:583200701891477504>', 6, 0, 1)]


class Base(Die):
    countable = True
    faces = [Face('base_one', '<:base_one:545643569218584638>', 1, 0, 1),
             Face('base_two', '<:base_blank:545643568677519370>', 2, 0, 0),
             Face('base_three', '<:base_blank:545643568677519370>', 3, 0, 0),
             Face('base_four', '<:base_blank:545643568677519370>', 4, 0, 0),
             Face('base_five', '<:base_blank:545643568677519370>', 5, 0, 0),
             Face('base_six', '<:base_six:545643569298407444>', 6, 1, 0)]


class Skill(Die):
    countable = True
    faces = [Face('skill_one', '<:skill_blank:545643939139682314>', 1, 0, 0),
             Face('skill_two', '<:skill_blank:545643939139682314>', 2, 0, 0),
             Face('skill_three', '<:skill_blank:545643939139682314>', 3, 0, 0),
             Face('skill_four', '<:skill_blank:545643939139682314>', 4, 0, 0),
             Face('skill_five', '<:skill_blank:545643939139682314>', 5, 0, 0),
             Face('skill_six', '<:skill_six:545643939387146268>', 6, 1, 0)]


class Negative(Die):
    countable = True
    faces = [Face('negative_one', '<:skill_blank:545643939139682314>', 1, 0, 0),
             Face('negative_two', '<:skill_blank:545643939139682314>', 2, 0, 0),
             Face('negative_three', '<:skill_blank:545643939139682314>', 3, 0, 0),
             Face('negative_four', '<:skill_blank:545643939139682314>', 4, 0, 0),
             Face('negative_five', '<:skill_blank:545643939139682314>', 5, 0, 0),
             Face('negative_six', '<:negative_six:548433188448501776>', 6, -1, 0)]


class Gear(Die):
    countable = True
    faces = [Face('gear_one', '<:gear_one:545646496691912704>', 1, 0, 1),
             Face('gear_two', '<:gear_blank:545646496586924035>', 2, 0, 0),
             Face('gear_three', '<:gear_blank:545646496586924035>', 3, 0, 0),
             Face('gear_four', '<:gear_blank:545646496586924035>', 4, 0, 0),
             Face('gear_five', '<:gear_blank:545646496586924035>', 5, 0, 0),
             Face('gear_six', '<:gear_six:545646496671072256>', 6, 1, 0)]


class D8(Die):
    countable = True
    faces = [Face('d8_one', '<:d8_blank:545646540782436365>', 1, 0, 0),
             Face('d8_two', '<:d8_blank:545646540782436365>', 2, 0, 0),
             Face('d8_three', '<:d8_blank:545646540782436365>', 3, 0, 0),
             Face('d8_four', '<:d8_blank:545646540782436365>', 4, 0, 0),
             Face('d8_five', '<:d8_blank:545646540782436365>', 5, 0, 0),
             Face('d8_six', '<:d8_six:545646541252329482>', 6, 1, 0),
             Face('d8_seven', '<:d8_six:545646541252329482>', 7, 1, 0),
             Face('d8_eight', '<:d8_eight:545646540996345866>', 8, 2, 0)]


class D10(Die):
    countable = True
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
    countable = True
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


class ResourceD6(Die):
    faces = [Face('resource_d6_one', '<:skill_one:546398615409655830>', 1, 0, 1),
             Face('resource_d6_two', '<:skill_one:546398615409655830>', 2, 0, 1),
             Face('resource_d6_three', '<:skill_six:545643939387146268>', 3, 0, 1),
             Face('resource_d6_four', '<:skill_six:545643939387146268>', 4, 0, 1),
             Face('resource_d6_five', '<:skill_six:545643939387146268>', 5, 0, 1),
             Face('resource_d6_six', '<:skill_six:545643939387146268>', 6, 0, 1)]


class ResourceD8(Die):
    faces = [Face('resource_d8_one', '<:d8_one:546398614847619082>', 1, 0, 1),
             Face('resource_d8_two', '<:d8_one:546398614847619082>', 2, 0, 1),
             Face('resource_d8_three', '<:d8_six:545646541252329482>', 3, 0, 1),
             Face('resource_d8_four', '<:d8_six:545646541252329482>', 4, 0, 1),
             Face('resource_8_five', '<:d8_six:545646541252329482>', 5, 0, 1),
             Face('resource_d8_six', '<:d8_six:545646541252329482>', 6, 0, 1),
             Face('resource_d8_seven', '<:d8_six:545646541252329482>', 7, 0, 1),
             Face('resource_d8_eight', '<:d8_six:545646541252329482>', 8, 0, 1)]


class ResourceD10(Die):
    faces = [Face('resource_d10_one', '<:d10_one:546398614705012757>', 1, 0, 1),
             Face('resource_d10_two', '<:d10_one:546398614705012757>', 2, 0, 1),
             Face('resource_d10_three', '<:d10_six:545646579412107265>', 3, 0, 1),
             Face('resource_d10_four', '<:d10_six:545646579412107265>', 4, 0, 1),
             Face('resource_d10_five', '<:d10_six:545646579412107265>', 5, 0, 1),
             Face('resource_d10_six', '<:d10_six:545646579412107265>', 6, 0, 1),
             Face('resource_d10_seven', '<:d10_six:545646579412107265>', 7, 0, 1),
             Face('resource_d10_eight', '<:d10_six:545646579412107265>', 8, 0, 1),
             Face('resource_d10_nine', '<:d10_six:545646579412107265>', 9, 0, 1),
             Face('resource_d10_ten', '<:d10_six:545646579412107265>', 10, 0, 1)]


class ResourceD12(Die):
    faces = [Face('resource_d12_one', '<:d12_one:546398614667133006>', 1, 0, 1),
             Face('resource_d12_two', '<:d12_one:546398614667133006>', 2, 0, 1),
             Face('resource_d12_three', '<:d12_six:545646598517161984>', 3, 0, 1),
             Face('resource_d12_four', '<:d12_six:545646598517161984>', 4, 0, 1),
             Face('resource_d12_five', '<:d12_six:545646598517161984>', 5, 0, 1),
             Face('resource_d12_six', '<:d12_six:545646598517161984>', 6, 0, 1),
             Face('resource_d12_seven', '<:d12_six:545646598517161984>', 7, 0, 1),
             Face('resource_d12_eight', '<:d12_six:545646598517161984>', 8, 0, 1),
             Face('resource_d12_nine', '<:d12_six:545646598517161984>', 9, 0, 1),
             Face('resource_d12_ten', '<:d12_six:545646598517161984>', 10, 0, 1),
             Face('resource_d12_eleven', '<:d12_six:545646598517161984>', 11, 0, 1),
             Face('resource_d12_twelve', '<:d12_six:545646598517161984>', 12, 0, 1)]
