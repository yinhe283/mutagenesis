from autoprotocol.protocol import Protocol
from internal.xpipette import xtransfer, xdistribute, dispense_target, distribute_target, aspirate_source, depth
from autoprotocol.instruction import *
import json

# write a python script for site-directed mutagenesis
# protocol based on the Agilent Quikchange method
# should think about tooling to design QuikChange/mutagenesis oligos on our website

# step 1: order mutant oligos, dilute to 100 uM


# step 2: dilute mutant oligos to working stock 20 uM

# step 3: Mutagenesis master mix containing 10X buffer, dNTPs, primers, QuikChange Multi enzyme blend
# step 4: Distribute mutagenesis MM to 96 well PCR plate
# step 5: Bravo LiHa DNA to 96 well PCR plate
# step 6: Move 96 well plate to PCR machine
# step 7: Thermocycle: 95 C for 1 min, 30 cycles of 95C for 1 min, 55C for 1 min, 65C for 2 min/kb, hold 12C
# step 8: unseal and move 96 well PCR plate to liha
# step 9: move enzyme plate from -20 to liha
# step 10: transfer 1 ul enzyme DpnI from enzyme plate to 96 well PCR plate
# step 11: return enzyme plate to -20
# step 12: seal and move 96-well PCR plate to 37C tiso
# step 13: unseal 96-well plate 
# step 14: transformation and plating
# step 15: colony picking
# step 16: miniprep
# step 17: sequencing

p = Protocol()

mutagenesis_plate = p.ref("mutagenesis_plate", None, "96-pcr", storage="cold_20")
mutagenesis_mm = p.ref("mutagenesis_mm", None, "micro-1.5", discard=True)
dna_plate = p.ref("dna_plate", None, "96-pcr", storage="cold_20")
enzyme_mm = p.ref("enzyme_mm", None, "micro-1.5", discard=True)


p.distribute(mutagenesis_mm, mutagenesis_plate.all_wells(), "23:microliter", one_tip=True)
p.stamp(dna_plate, mutagenesis_plate, "2:microliter")

p.seal(mutagenesis_plate)

p.thermocycle(mutagenesis_plate,
		[{"cycles": 1, "steps": [
			{"temperature": "95:celsius", "duration": "1:minute"}
			]},
		{"cycles": 30, "steps": [
			{"temperature": "95:celsius", "duration": "1:minute"},
			{"temperature": "55:celsius", "duration": "1:minute"},
			{"temperature": "65:celsius", "duration": "6:minute"}
			]},  #2 min/kb of plasmid
		{"cycles": 1, "steps": [
			{"temperature": "12: celsius", "duration": "10:minute"}
		]}
	])


p.unseal(mutagenesis_plate)

p.distribute(enzyme_mm, mutagenesis_plate.all_wells(), "2:microliter", one_tip=False)

p.seal(mutagenesis_plate)

p.incubate(mutagenesis_plate, "warm_37", "2:hour", shaking=False)

p.unseal(mutagenesis_plate)

print json.dumps(p.as_dict(), indent=2)

# def site_directed_mutagenesis(protocol, params):
# 	params = make_dottable_dict(params)

# 	#Step 1 - Make mutagenesis MM
# 	mutagenesis_plate = protocol.ref("mutagenesis_plate", None, "96-pcr", storage="cold_20")
# 	wells_to_mutagenize = mutagenesis_plate.wells_from("A1", len(params.source_plasmid))
# 	# mutagenesis_reagent_plate = protocol.ref("mutagesnsis_reagent_plate", None, "96-pcr", storage="cold_20")
# 	mutagenesis_mm = []
# 	for i in range(0, 1+len(params.source_plasmid)/40):
# 		mutagenesis_mm.append(protocol.ref("mutagenesis_mm%s"%(i), None, "micro-1.5", discard=True).well(0).set_volume("1500:microliter"))
	
# 	# mutagenesis_buffer10x = protocol.ref("mutagenesis_buffer10x", None, "micro-1.5", discard=True).well(0).set_volume("500:microliter")
# 	# quikchange_enzyme = protocol.ref("quikchange_enzyme", None, "micro-1.5", discard=True).well(0).set_volume("100:microliter")
# 	# dNTPs = protocol.ref("dNTPs", None, "micro-1.5", discard=True).well(0).set_volume("100:microliter")
# 	# oligo_forward = protocol.ref("oligo_forward", None, "micro-1.5", discard=True).well(0).set_volume("100:microliter")
# 	# oligo_reverse = protocol.ref("oligo_reverse", None, "micro-1.5", discard=True).well(0).set_volume("100:microliter")
	

# 	protocol.distribute(mutagenesis_mm, wells_to_mutagenize, "20:microliter", allow_carryover=True)
# 	for i, source_plasmid in enumerate(params.source_plasmid): protocol.transfer(source_plasmid, 
# 			wells_to_mutagenize[i], "2:microliter", mix_after=False)
	
# 	protocol.seal(mutagenesis_plate)

	# p.thermocycle(mutagenesis_plate,
	# 	[{"cycles": 1, "steps": [
	# 		{"temperature": "95:celsius", "duration": "1:minute"},
	# 		]},
	# 	{"cycles": 30, "steps": [
	# 		{"temperature": "95:celsius", "duration": "1:minute"},
	# 		{"temperature": "55:celsius", "duration": "1:minute"},
	# 		{"temperature": "65:celsius", "duration": "6:minute"},  #2 min/kb of plasmid
	# 	{"cycles": 1, "steps": [
	# 		{"temperature": "12: celsius", "duration": "10:minute"},
	# 	]},
	# ], 
# 		# volume = "25:microliter")

# 	protocol.unseal(mutagenesis_plate)




# if __name__ == '__main__':
# 	from autoprotocol.harness import run
# 	run(site_directed_mutagenesis)

