#!/usr/bin/python3

import json
import GameOfLife as gol

if __name__ == '__main__':	
	with open('config.json', encoding='utf-8') as config_file:
		config = json.loads(config_file.read())
	config['is_test'] = 1
	config['test_pattern'] = "Pulsar"
	gol.GameOfLife(config)
