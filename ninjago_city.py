from mine import *
import math
import random


# Tower dimentions
TOWER_SIZE = 10
INNER_SIZE = TOWER_SIZE - 4
GAP = (TOWER_SIZE - INNER_SIZE - 2) / 2
MAX_HEIGHT_INNER = 10
MAX_HEIGHT_OUTER = 3

# Block dimentions
TOWERS_PER_BLOCK_X = 2
TOWERS_PER_BLOCK_Z = 2
TOWER_BORDER = 2
BLOCK_LENGTH_X = (TOWERS_PER_BLOCK_X * TOWER_SIZE) + (TOWERS_PER_BLOCK_X * (2 * TOWER_BORDER))
BLOCK_LENGTH_Z = (TOWERS_PER_BLOCK_Z * TOWER_SIZE) + (TOWERS_PER_BLOCK_Z * (2 * TOWER_BORDER))

# City dimentions
BLOCKS_X = 15
BLOCKS_Z = 15
BLOCK_GAP = 7
OUTER_BLOCKS = 5


def horizontal_square(minecraft, x, y, z, blk, size):
    for i in range(0, size):
        minecraft.setBlock(x + i, y, z, blk)
        minecraft.setBlock(x + i, y, z + size - 1, blk)
    for i in range(0, size - 2):
        minecraft.setBlock(x, y, z + 1 + i, blk)
        minecraft.setBlock(x + size - 1, y, z + 1 + i, blk)


def vertical_square_fixed_x(minecraft, x, y, z, blk, size):
    for i in range(0, size):
        minecraft.setBlock(x, y + i, z, blk)
        minecraft.setBlock(x, y + i, z + size - 1, blk)
    for i in range(0, size - 2):
        minecraft.setBlock(x, y, z + 1 + i, blk)
        minecraft.setBlock(x, y + size - 1, z + 1 + i, blk)


def vertical_square_fixed_z(minecraft, x, y, z, blk, size):
    for i in range(0, size):
        minecraft.setBlock(x, y + i, z, blk)
        minecraft.setBlock(x + size - 1, y + i, z, blk)
    for i in range(0, size - 2):
        minecraft.setBlock(x + 1 + i, y, z, blk)
        minecraft.setBlock(x + 1 + i, y + size - 1, z, blk)


def vertical_struts(minecraft, x, y, z, blk, size):
    for i in range(0, size - 2):
        minecraft.setBlock(x, y + 1 + i, z, blk)
        minecraft.setBlock(x + size - 1, y + 1 + i, z, blk)
        minecraft.setBlock(x, y + 1 + i, z + size - 1, blk)
        minecraft.setBlock(x + size - 1, y + 1 + i, z + size - 1, blk)


def fill_glass_horizontal(minecraft, x, y, z, size, gap):
    blk = block.STAINED_GLASS_WHITE
    for i in range(0, gap):
        horizontal_square(minecraft, x + 1 + i, y, z + 1 + i, blk, size - 2 - i)


def fill_glass_vertical_fixed_x(minecraft, x, y, z, size, gap):
    blk = block.STAINED_GLASS_WHITE
    for i in range(0, gap):
        vertical_square_fixed_x(minecraft, x, y + 1 + i, z + 1 + i, blk, size - 2 - i)


def fill_glass_vertical_fixed_z(minecraft, x, y, z, size, gap):
    blk = block.STAINED_GLASS_WHITE
    for i in range(0, gap):
        vertical_square_fixed_z(minecraft, x + 1 + i, y + 1 + i, z, blk, size - 2 - i)


def build_tower(minecraft, x, y, z, height, size, inner_size, gap):
    outer_blk = block.NETHERRACK
    inner_blk = block.PRISMARINE
    for i in range(0, height):
        # Outer base square
        horizontal_square(minecraft, x, y + (i * (size - 1)), z, outer_blk, size)
        # Innner base square
        horizontal_square(minecraft, x + 2, y + (i * (size - 1)), z + 2, inner_blk, inner_size)
        # Uprights
        vertical_struts(minecraft, x, y + (i * (size - 1)), z, outer_blk, size)
        # The 4 side inner squares
        vertical_square_fixed_z(minecraft, x + 2, y + (i * (size - 1)) + 2, z, inner_blk, inner_size)
        vertical_square_fixed_z(minecraft, x + 2, y + (i * (size - 1)) + 2, z + size - 1, inner_blk, inner_size)
        vertical_square_fixed_x(minecraft, x, y + (i * (size - 1)) + 2, z + 2, inner_blk, inner_size)
        vertical_square_fixed_x(minecraft, x + size - 1, y + (i * (size - 1)) + 2, z + 2, inner_blk, inner_size)
        # Fill glass in the base square
        fill_glass_horizontal(minecraft, x, y, z, size, gap)
        # Fill glass sides
        fill_glass_vertical_fixed_x(minecraft, x, y + (i * (size - 1)), z, size, gap)
        fill_glass_vertical_fixed_x(minecraft, x + size - 1, y + (i * (size - 1)), z, size, gap)
        fill_glass_vertical_fixed_z(minecraft, x, y + (i * (size - 1)), z, size, gap)
        fill_glass_vertical_fixed_z(minecraft, x, y + (i * (size - 1)), z + size - 1, size, gap)

    if height > 0:
        horizontal_square(minecraft, x, y + (height * (size - 1)), z, outer_blk, size)
        horizontal_square(minecraft, x + 2, y + (height * (size - 1)), z + 2, inner_blk, inner_size)
        fill_glass_horizontal(minecraft, x, y + (height * (size - 1)), z, size, gap)


def get_tower_height(block_x, block_z):
    inner_city_x = block_x >= OUTER_BLOCKS and block_x <= (BLOCKS_X - OUTER_BLOCKS)
    inner_city_z = block_z >= OUTER_BLOCKS and block_z <= (BLOCKS_Z - OUTER_BLOCKS)
    if inner_city_x and inner_city_z:
        return random.randint(0, MAX_HEIGHT_INNER)
    else:
        return random.randint(0, MAX_HEIGHT_OUTER)


def _generate_city():
    random.seed(0)
    city = []
    # Generate random heights for each tower block
    for block_x in range(0, BLOCKS_X):
        for block_z in range(0, BLOCKS_Z):
            blocks = []
            for x in range(0, TOWERS_PER_BLOCK_X):
                for z in range(0, TOWERS_PER_BLOCK_Z):
                    blocks.append({"x": x, "z": z, "height": get_tower_height(block_x, block_z)})
            city.append({"x": block_x, "z": block_z, "block": blocks})
    return city


def get_tower_coords(start_x, start_z, block_x, block_z, tower_x, tower_z, tower_length, tower_border):
    x = start_x + (BLOCK_LENGTH_X * block_x) + (BLOCK_GAP * block_x) + \
        (tower_x * (tower_length + (2 * tower_border))) + tower_border
    z = start_z + (BLOCK_LENGTH_Z * block_z) + (BLOCK_GAP * block_z) + \
        (tower_z * (tower_length + (2 * tower_border))) + tower_border
    return (x, z)


def _generate_towers(minecraft, start_x, start_y, start_z):
    city = _generate_city()
    for block in city:
        for tower in block["block"]:
            (x, z) = get_tower_coords(start_x, start_z,
                         block["x"], block["z"],
                         tower["x"], tower["z"],
                         TOWER_SIZE, TOWER_BORDER)
            build_tower(minecraft, x, start_y, z, tower["height"], TOWER_SIZE, INNER_SIZE, GAP)


def _generate_roads(minecraft, start_x, start_y, start_z):
    gray_blk = block.HARDENED_CLAY_STAINED_LIGHT_GRAY
    white_blk = block.HARDENED_CLAY_STAINED_WHITE

    # Generate the roads heading in the z direction (keeping x constant).
    for b in range(1, BLOCKS_X):
        road_x = start_x + (BLOCK_LENGTH_X * b) + (BLOCK_GAP * (b - 1))
        road_width = BLOCK_GAP
        road_length = (BLOCK_LENGTH_Z * BLOCKS_Z) + (BLOCK_GAP * (BLOCKS_Z - 1))
        for z in range(0, road_length):
            for x in range(0, road_width):
                minecraft.setBlock(road_x + x, start_y - 1, start_z + z, gray_blk)

        # Generates the white line.
        middle_x = road_x + int(BLOCK_GAP / 2.0)
        for z in range(0, road_length):
            blk = white_blk if (z % 3) != 0 else gray_blk
            minecraft.setBlock(middle_x, start_y - 1, start_z + z, blk)

    # Generate the roads heading in the x direction (keeping z constant).
    for b in range(1, BLOCKS_Z):
        road_z = start_z + (BLOCK_LENGTH_Z * b) + (BLOCK_GAP * (b - 1))
        road_width = BLOCK_GAP
        road_length = (BLOCK_LENGTH_X * BLOCKS_X) + (BLOCK_GAP * (BLOCKS_X - 1))
        for x in range(0, road_length):
            for z in range(0, road_width):
                minecraft.setBlock(start_x + x, start_y - 1, road_z + z, gray_blk)

        # Generates the white line.
        middle_z = road_z + int(BLOCK_GAP / 2.0)
        for x in range(0, road_length):
            blk = white_blk if (x % 3) != 0 else gray_blk
            minecraft.setBlock(start_x + x, start_y - 1, middle_z, blk)


def _main():
    minecraft = Minecraft()
    minecraft.postToChat("Building city")

    pos = minecraft.player.getPos()
    start_x = int(pos.x + 1)
    start_y = 0
    start_z = int(pos.z + 1)

    _generate_towers(minecraft, start_x, start_y, start_z)
    _generate_roads(minecraft, start_x, start_y, start_z)

    minecraft.postToChat("Building complete")


_main()
