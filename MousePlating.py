metadata = {
    'protocolName': 'Mouse Study Plating and Dilution',
    'author': 'Lachlan <lajamu@biosustain.dtu.dk',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}

def run(protocol):

	#Load Tips1
    tips20= [protocol.load_labware('opentrons_96_tiprack_20ul', '9')]
    tips1000 = [protocol.load_labware('opentrons_96_tiprack_1000ul', '1')]

    p20Multi = protocol.load_instrument("p20_multi_gen2", "left", tip_racks=tips20)
    p1000Single = protocol.load_instrument("p1000_single", "right", tip_racks=tips1000)

    temp_block = protocol.load_module("tempdeck", 4)
    temp_block.set_temperature(4)

    pooTubes = temp_block.load_labware("opentrons_24_aluminumblock_nest_2ml_screwcap")

    plate_type = "corning_96_wellplate_360ul_flat"
    locs = [10, 11, 5, 6]

    dilutionPlates = [protocol.load_labware(plate_type, slot)
    				for slot in locs]



    agar_plate_type = "biorad_96_wellplate_200ul_pcr" #can be any 96 that isn't the same as dil plate
    agar_locs = [7, 8, 2, 3]
    agar_plates = [protocol.load_labware(agar_plate_type, slot)
    				for slot in agar_locs]

    print(dilutionPlates[1])
    print(pooTubes)

    for p in range(16):
    	p1000Single.distribute(200, pooTubes.wells()[p], [dilutionPlates[0].wells()[p], 
    		dilutionPlates[1].wells()[p]] if p < 8 
    		else [dilutionPlates[2].wells()[p], dilutionPlates[3].wells()[p]])


    

