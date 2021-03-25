metadata = {
    'protocolName': '384 Dilution and Plating',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'apiLevel': '2.2'
}

def run(protocol):

	#Load Tips1
    tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]


    p20Multi = protocol.load_instrument("p20_multi_gen2", "left", tip_racks=tips20)

    agar_plate_type = "biorad_96_wellplate_200ul_pcr" #can be any 96 that isn't the same as dil plate
    agar = protocol.load_labware(agar_plate_type, 3)
    
    pl_384 = protocol.load_labware("echo_384_pp_standard", 2)      
        
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

    def mix_plate(w1, w2, p):
        p20Multi.mix(2, 20, pl_384.wells()[w1])
        p20Multi.aspirate(10, pl_384.wells()[w1])
        spot(agar.wells()[p], 5)
        p20Multi.dispense(5, pl_384.wells()[w2])



    def dilute_plate(w, a):
        """dilutes in a square and plates"""
        p20Multi.pick_up_tip()
        mix_plate(w, w + 16, a)
        mix_plate(w + 16, w + 17, a+8)
        mix_plate(w + 17, w + 1, a+16)
        p20Multi.mix(2, 20, pl_384.wells()[w+1])
        p20Multi.aspirate(5, pl_384.wells()[w+1])
        spot(agar.wells()[24], 5)
        p20Multi.drop_tip()


    wells = [0, 128, 256]
    agar_locs = [0, 32, 64]

    for well, agar_loc in zip(wells, agar_locs):
        dilute_plate(well, agar_loc)

        
    protocol.comment("Run Complete!")
        
        


    

