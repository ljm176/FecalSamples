metadata = {
    'protocolName': 'Fecal Plating and Dilution',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'apiLevel': '2.9'
}

def run(protocol):

	#Load Tips1
    tips20= protocol.load_labware('opentrons_96_tiprack_20ul', 4)


    p20Multi = protocol.load_instrument("p20_multi_gen2", "left", tip_racks=[tips20])
    
    temp_block = protocol.load_module("tempdeck", 10)
    temp_block2 = protocol.load_module("tempdeck", 7)

    PooTubes1 = temp_block.load_labware("opentrons_24_aluminumblock_nest_2ml_screwcap", label="PooTubes")
    PooTubes2 = temp_block2.load_labware("opentrons_24_aluminumblock_nest_2ml_screwcap", label="PooTubes 2")

    reversedTips = tips20.wells()[::-1]

    plate_type = "corning_96_wellplate_360ul_flat"
    locs = [5, 6, 8, 9]

    dilutionPlates = [protocol.load_labware(plate_type, slot, label="Dilution Plates")
    				for slot in locs]

    agar_plate_type = "biorad_96_wellplate_200ul_pcr" #can be any 96 that isn't the same as dil plate
    agar_locs = [1, 2, 3, 11]
    agar_plates = [protocol.load_labware(agar_plate_type, slot, label="Agar")
    				for slot in agar_locs]

    pooWells = PooTubes1.wells() + PooTubes2.wells()

    dest_wells_r1 = [item for l in [[x for x in dilutionPlates[y].wells()[0:8]] + [x for x in dilutionPlates[y].wells()[48:56]] for y in [0, 2]] for item in l]
    dest_wells_r2 = [item for l in [[x for x in dilutionPlates[y].wells()[0:8]] + [x for x in dilutionPlates[y].wells()[48:56]] for y in [1, 3]] for item in l]


    for p in range(32):
        p20Multi.pick_up_tip(reversedTips[p].top(3), presses = 0)
        p20Multi.aspirate(20, pooWells[p])
        p20Multi.dispense(10, dest_wells_r1[p])
        p20Multi.dispense(10, dest_wells_r2[p])
        p20Multi.drop_tip()

        
    # def spot(dest, spot_vol):
    #     """Takes a diluted transformed culture and spots the defined volume onto agar 
    #     in a Nunc omnitray"""

    #     SAFE_HEIGHT = 15  
    #     spotting_dispense_rate=0.025 
    #     p20Multi.move_to(dest.top(SAFE_HEIGHT))
    #     protocol.max_speeds["Z"] = 50
    #     p20Multi.move_to(dest.top(2))
    #     p20Multi.dispense(volume=spot_vol, rate=spotting_dispense_rate)
    #     p20Multi.move_to(dest.top(0))
    #     del protocol.max_speeds["Z"]
    
    # def spot_then_dilute(sourceCol, agar_dest, destcol, spot_vol):
    #     p20Multi.aspirate(spot_vol, sourceCol)
    #     spot(agar_dest, spot_vol)
    #     p20Multi.transfer(10, sourceCol, destcol, mix_after=(5, 20), new_tip="never")

    # def spot_dilute_half_plate(plate, agar, spot_vol, startCol):
    #     p20Multi.pick_up_tip()
    #     for col in range(startCol, startCol+5):
    #         w = "A"+str(col)
    #         x = "A" + str(col+1)
    #         spot_then_dilute(plate[w], agar[w], 
    #                          plate[x], spot_vol)
    #         #Spot final dilution
    #         p20Multi.aspirate(spot_vol, plate[x])
    #         spot(agar[x], spot_vol)
    #     p20Multi.drop_tip()

    
    # def spot_dilute_plate(plate, agar, spot_vol):
    #     for c in [1, 7]: spot_dilute_half_plate(plate, agar, spot_vol, c)
        
    # for pl, ag in zip(dilutionPlates, agar_plates):
    #     spot_dilute_plate(pl, ag, 5)
        
    # protocol.comment("Run Complete!")
        
        


    

