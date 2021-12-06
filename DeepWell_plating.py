metadata = {
    'protocolName': 'General Plating and Dilution DeepWell',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'apiLevel': '2.8'
}

def run(protocol):

	#Load Tips1
    tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '2')]
    tips300 = [protocol.load_labware('opentrons_96_tiprack_300ul', '1')]

    p20Multi = protocol.load_instrument("p20_multi_gen2", "right", tip_racks=tips20)
    p300Multi = protocol.load_instrument("p300_multi_gen2", "left", tip_racks=tips300)



    deepWell = protocol.load_labware("usascientific_96_wellplate_2.4ml_deep", 4, label="DeepWell")
    reservoir = protocol.load_labware("agilent_1_reservoir_290ml", 10)

    plate_type = "corning_96_wellplate_360ul_flat"
    locs = [5, 6]

    dilutionPlates = [protocol.load_labware(plate_type, slot, label="Dilution Plates")
    				for slot in locs]

    agar_plate_type = "biorad_96_wellplate_200ul_pcr" #can be any 96 that isn't the same as dil plate
    agar_locs = [7, 8, 9]
    agar_plates = [protocol.load_labware(agar_plate_type, slot, label="Agar")
    				for slot in agar_locs]


    columns = [p.rows()[0] for p in dilutionPlates]
    p300Multi.transfer(90, reservoir["A1"], columns, new_tip="once")
            
        
    def spot(dest, spot_vol):
        """Takes a diluted transformed culture and spots the defined volume onto agar 
        in a Nunc omnitray"""

        SAFE_HEIGHT = 15  
        spotting_dispense_rate=0.25 
        p20Multi.move_to(dest.top(SAFE_HEIGHT))
        protocol.max_speeds["Z"] = 50
        p20Multi.move_to(dest.top(2))
        p20Multi.dispense(volume=spot_vol, rate=spotting_dispense_rate)
        p20Multi.move_to(dest.top(0))
        del protocol.max_speeds["Z"]
    
    def spot_then_dilute(sourceCol, agar_dest, destcol, spot_vol):
        p20Multi.mix(3, 20, sourceCol)
        p20Multi.aspirate(spot_vol, sourceCol)
        spot(agar_dest, spot_vol)
        p20Multi.transfer(10, sourceCol, destcol, mix_after=(3, 20), new_tip="never")
        
    for col in range(12):
    	p20Multi.pick_up_tip()
    	spot_then_dilute(deepWell.columns()[col][0], agar_plates[0].columns()[col][0], dilutionPlates[0].columns()[col][0], 5)
    	spot_then_dilute(dilutionPlates[0].columns()[col][0], agar_plates[1].columns()[col][0], dilutionPlates[1].columns()[col][0], 5)
    	p20Multi.mix(3, 20, dilutionPlates[1].columns()[col][0])
    	p20Multi.aspirate(5, dilutionPlates[1].columns()[col][0])
    	spot(agar_plates[2].columns()[col][0], 5)
    	p20Multi.drop_tip()
    
        
    protocol.comment("Run Complete!")
        
        


    

