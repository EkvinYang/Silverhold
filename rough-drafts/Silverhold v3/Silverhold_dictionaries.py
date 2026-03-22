# ==========
# TOWERS
# ==========

towerDict = {
    "central": {
        "resolution": (100, 100),
        "Size": 5,
        "level1": {
            # STATS
            "Health": 500, "Cost": 0,
            # ATTACK
            "Damage": 10, "Range": 375, "attackSpeed": 5, "attackType": "arrow",
            # MISC
            "Value": 250, "imageFile": "tower_archer1.png", "turretSprite": "tower_archerturret1.png"
        },
        "level2": {
                # STATS
                "Health": 250, "Cost": 250,
                # ATTACK
                "Damage": 10, "Range": 375, "attackSpeed": 5, "attackType": "arrow",
                # MISC
                "Value": 250, "imageFile": "tower_archer1.png", "turretSprite": "tower_archerturret1.png"
        },
        "level3": {
                # STATS
                "Health": 250, "Cost": 250,
                # ATTACK
                "Damage": 10, "Range": 375, "attackSpeed": 5, "attackType": "arrow",
                # MISC
                "Value": 250, "imageFile": "tower_archer1.png", "turretSprite": "tower_archerturret1.png"
        }
    },
    "archer": {
        "resolution": (60, 60),
        "Size": 3, 
        "level1": {
            # STATS
            "Health": 250, "Cost": 250,
            # ATTACK
            "Damage": 10, "Range": 375, "attackSpeed": 5, "attackType": "arrow",
            # MISC
            "Value": 250, "imageFile": "tower_archer1.png", "turretSprite": "tower_archerturret1.png"},
        
        "level2": {
            # STATS
            "Health": 350, "upgradeCost": 250,
            # ATTACK
            "Damage": 20, "Range": 425, "attackSpeed": 4, "attackType": "arrow",
            # MISC
            "Value": 500, "imageFile": "tower_archer2.png", "turretSprite": "tower_archerturret2.png"},

        "level3": {
            # STATS
            "Health": 600, "upgradeCost": 500,
            # ATTACK
            "Damage": 50, "Range": 475, "attackSpeed": 3, "attackType": "arrow2",
            # MISC
            "Value": 1000, "imageFile": "tower_archer3.png", "turretSprite": "tower_archerturret3.png"},
        },
    
    "cannon": {
        "resolution": (80, 80),
        "Size": 4, 
        "level1": {
            # STATS
            "Health": 500, "Cost": 500,
            # ATTACK
            "Damage": 50, "Range": 400, "attackSpeed": 20, "attackType": "cannonball",
            # MISC
            "Value": 500, "imageFile": "tower_cannon1.png", "turretSprite": "tower_cannonturret1.png"},

        "level2": {
            # STATS
            "Health": 750, "upgradeCost": 750,
            # ATTACK
            "Damage": 75, "Range": 500, "attackSpeed": 20, "attackType": "cannonball",
            # MISC
            "Value": 1250, "imageFile": "tower_cannon2.png", "turretSprite": "tower_cannonturret2.png"},

        "level3": {
            # STATS
            "Health": 1100, "upgradeCost": 1500,
            # ATTACK
            "Damage": 150, "Range": 600, "attackSpeed": 15, "attackType": "explosive",
            # MISC
            "Value": 2750, "imageFile": "tower_cannon3.png", "turretSprite": "tower_cannonturret3.png"},
        },

    "wizard": {
        "resolution": (60, 60),
        "Size": 3, 
        "level1": {
            # STATS
            "Health": 300, "Cost": 1250,
            # ATTACK
            "Damage": 10, "Range": 350, "attackSpeed": 20, "attackType": "magic_swarm",
            # MISC
            "Value": 1250, "imageFile": "tower_wizard1.png"},

        "level2": {
            # STATS
            "Health": 400, "upgradeCost": 1750,
            # ATTACK
            "Damage": 25, "Range": 375, "attackSpeed": 20, "attackType": "magic_swarm",
            # MISC
            "Value": 3000, "imageFile": "tower_wizard2.png"},

        "level3": {
            # STATS
            "Health": 650, "upgradeCost": 5000,
            # ATTACK
            "Damage": 75, "Range": 400, "attackSpeed": 15, "attackType": "magic2_swarm",
            # MISC
            "Value": 8000, "imageFile": "tower_wizard3.png"},
        },
    }

# ==========
# ENEMIES
# ==========

enemyDict = {
    "sailboat": {
        # STATS
        "Size": 5, "Health": 250, "Speed": 3, 
        # ATTACK
        "Damage": 10, "attackSpeed": 20, "attackType": "cannonball",
        # MISC
        "Value": 250, "imageFile": "enemy_sailboat.png"},

    "caravel": {
        # STATS
        "Size": 10, "Health": 1000, "Speed": 2, 
        # ATTACK
        "Damage": 25, "attackSpeed": 50, "attackType": "cannonball",
        # MISC
        "Value": 500, "imageFile": "enemy_caravel.png"},

    "brigantine": {
        # STATS
        "Size": 25, "Health": 5000, "Speed": 1, 
        # ATTACK
        "Damage": 100, "attackSpeed": 250, "attackType": "explosive",
        # MISC
        "Value": 1500, "imageFile": "enemy_brigantine.png"},
    }

# ==========
# PROJECTILES
# ==========

projectileDict = {
    "arrow": {
        "imageFile": "projectile_arrow.png"
    },
    "arrow2": {
        "imageFile": "projectile_arrow2.png"
    },
    "cannonball": {
        "imageFile": "projectile_cannonball.png"
    },
    "explosive": {
        "imageFile": "projectile_explosive.png"
    },
    "magic_swarm": {
        "imageFile": "projectile_magic.png"
    },
    "magic2_swarm": {
        "imageFile": "projectile_magic.png"
    },
}
