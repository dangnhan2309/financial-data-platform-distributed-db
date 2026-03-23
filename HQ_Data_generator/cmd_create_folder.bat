mkdir data_simulator
cd data_simulator

mkdir generator
mkdir scheduler

type nul > main.py
type nul > api_client.py
type nul > config.py

type nul > generator\customer_generator.py
type nul > generator\quotation_generator.py
type nul > generator\contract_generator.py
type nul > generator\order_generator.py

type nul > scheduler\event_scheduler.py

type nul > generator\__init__.py
type nul > scheduler\__init__.py