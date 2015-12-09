#!/usr/bin/env python3
# coding: utf-8
import rpg


def get_clauses(merchant, level):
    # Append all clauses needed to find the correct equipment in the 'clauses' list.
    #
    # Minisat variables are represented with integers. As such you should use
    # the index attribute of classes Ability and Equipment from the rpg.py module
    #
    # The equipments and abilities they provide read from the merchant file you passed
    # as argument are contained in the variable 'merchant'.
    # The enemies and abilities they require to be defeated read from the level file you
    # passed as argument are contained in the variable 'level'
    #
    # For example if you want to add the clauses equ1 or equ2 or ... or equN (i.e. a
    # disjunction of all the equipment pieces the merchant proposes), you should write:
    #
    # clauses.append(tuple(equ.index for equ in merchant.equipments))
    clauses = []
    inventaire = []
    # Pour toute habilité
    for ability_needed_name in level.ability_names:
        ability_equips = []
        for equip in merchant.equipments:
            # Pour tout item achetable
            if merchant.abi_map[ability_needed_name] in equip.provides:
                # if item provides l'ability
                ability_equips.append(equip)
                # if item ne fait pas encore partie de l'equipement
                if equip not in inventaire:
                    inventaire.append(equip)
                    # Insertion des conflits
                    clauses.append(
                        tuple([-equip.index, -equip.conflicts.index]))
        # disjonction des items necessaires à satisfaire une habilité
        clauses.append(tuple(e.index for e in ability_equips))
    return clauses



def get_nb_vars(merchant, level):
    # nb_vars should be the number of different variables present in your list 'clauses'
    #
    # For example, if your clauses contain all the equipments proposed by merchant and
    # all the abilities provided by these equipment, you would have:
    # nb_vars = len(merchant.abilities) + len(merchant.equipments)
    indexes = []
    for ability_needed_name in level.ability_names:
        for equip in merchant.equipments:
            if merchant.abi_map[ability_needed_name] in equip.provides:
                indexes.append(equip.index)
                indexes.append(equip.conflicts.index)
    return max(indexes)
