analysis:
	python analysis.py ./data/off.txt ./data/on.txt
	python analysisdb.py ./data/off.txt ./data/on.txt
	python analysisdba.py ./data/off.txt ./data/on.txt
scan:
	sudo python speccy.py wlxc01c300da106
tooff:
	python example_offline_analysis.py ./spectral_data/*>> ./data/off.txt
toon:
	python example_offline_analysis.py ./spectral_data/*>> ./data/on.txt
