-- Oracle Schema Generation
-- Auto-generated matches FastAPI SQLAlchemy Models

-- DROP TABLES (Safely)
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE transport_ticket CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE qc_record CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE weighing_ticket CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE purchase_ticket CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE sensor_data CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE cultivation_log CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE inventory CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE production_lot CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE purchase_batch CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE iot_sensor CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE farm_bed CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE purchase_contract CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE farm_plot CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE product CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE ingredient CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE supplier CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE warehouse CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE farm CASCADE CONSTRAINTS';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

-- CREATE TABLES
-- Table: farm
CREATE TABLE farm (
    farm_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    farm_name VARCHAR2(255),
    location VARCHAR2(255),
    region VARCHAR2(50),
    site_id VARCHAR2(50)
);

-- Table: warehouse
CREATE TABLE warehouse (
    warehouse_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    warehouse_name VARCHAR2(255),
    location VARCHAR2(255),
    capacity_ton NUMBER,
    region VARCHAR2(50),
    site_id VARCHAR2(50)
);

-- Table: supplier
CREATE TABLE supplier (
    supplier_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    supplier_name VARCHAR2(255),
    supplier_type VARCHAR2(100),
    phone VARCHAR2(50),
    address VARCHAR2(255),
    region VARCHAR2(50),
    site_id VARCHAR2(50)
);

-- Table: ingredient
CREATE TABLE ingredient (
    ingredient_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    name VARCHAR2(255),
    region VARCHAR2(50),
    site_id VARCHAR2(50)
);

-- Table: product
CREATE TABLE product (
    product_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    product_name VARCHAR2(255),
    ingredient_id VARCHAR2(50),
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_prod_ing FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
);

-- Table: farm_plot
CREATE TABLE farm_plot (
    plot_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    farm_id VARCHAR2(50),
    plot_name VARCHAR2(255),
    crop_type VARCHAR2(100),
    area_m2 NUMBER,
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_plot_farm FOREIGN KEY (farm_id) REFERENCES farm(farm_id)
);

-- Table: purchase_contract
CREATE TABLE purchase_contract (
    contract_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    supplier_id VARCHAR2(50),
    ingredient_id VARCHAR2(50),
    committed_quantity NUMBER,
    contract_price NUMBER,
    quality_commitment VARCHAR2(255),
    start_date DATE,
    end_date DATE,
    status VARCHAR2(50),
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_cont_sup FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id),
    CONSTRAINT fk_cont_ing FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
);

-- Table: farm_bed
CREATE TABLE farm_bed (
    bed_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    plot_id VARCHAR2(50),
    bed_number NUMBER,
    planting_date DATE,
    status VARCHAR2(50),
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_bed_plot FOREIGN KEY (plot_id) REFERENCES farm_plot(plot_id)
);

-- Table: iot_sensor
CREATE TABLE iot_sensor (
    sensor_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    plot_id VARCHAR2(50),
    sensor_type VARCHAR2(100),
    manufacturer VARCHAR2(100),
    status VARCHAR2(50),
    installed_at TIMESTAMP,
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_sens_plot FOREIGN KEY (plot_id) REFERENCES farm_plot(plot_id)
);

-- Table: purchase_batch
CREATE TABLE purchase_batch (
    batch_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    contract_id VARCHAR2(50),
    purchase_date DATE,
    expected_quantity NUMBER,
    unit_price NUMBER,
    status VARCHAR2(50),
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_batch_cont FOREIGN KEY (contract_id) REFERENCES purchase_contract(contract_id)
);

-- Table: production_lot
CREATE TABLE production_lot (
    lot_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    product_id VARCHAR2(50),
    mfg_date TIMESTAMP,
    exp_date TIMESTAMP,
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_lot_prod FOREIGN KEY (product_id) REFERENCES product(product_id)
);

-- Table: inventory
CREATE TABLE inventory (
    inventory_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    warehouse_id VARCHAR2(50),
    inventory_type VARCHAR2(20),
    item_id VARCHAR2(50),
    lot_number VARCHAR2(50),
    origin_source VARCHAR2(50),
    origin_ref_id VARCHAR2(50),
    quantity_kg NUMBER,
    updated_at TIMESTAMP,
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_inv_wh FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id)
);

-- Table: cultivation_log
CREATE TABLE cultivation_log (
    log_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    bed_id VARCHAR2(50),
    action VARCHAR2(100),
    performed_by VARCHAR2(100),
    notes VARCHAR2(4000),
    timestamp TIMESTAMP,
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_log_bed FOREIGN KEY (bed_id) REFERENCES farm_bed(bed_id)
);

-- Table: sensor_data
CREATE TABLE sensor_data (
    data_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    sensor_id VARCHAR2(50),
    temperature NUMBER,
    humidity NUMBER,
    soil_moisture NUMBER,
    light_intensity NUMBER,
    recorded_at TIMESTAMP,
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_data_sens FOREIGN KEY (sensor_id) REFERENCES iot_sensor(sensor_id)
);

-- Table: purchase_ticket
CREATE TABLE purchase_ticket (
    ticket_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    batch_id VARCHAR2(50),
    supplier_id VARCHAR2(50),
    ingredient_id VARCHAR2(50),
    raw_weight NUMBER,
    received_at TIMESTAMP,
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_ptick_batch FOREIGN KEY (batch_id) REFERENCES purchase_batch(batch_id),
    CONSTRAINT fk_ptick_sup FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id),
    CONSTRAINT fk_ptick_ing FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
);

-- Table: weighing_ticket
CREATE TABLE weighing_ticket (
    ticket_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    bed_id VARCHAR2(50),
    ingredient_id VARCHAR2(50),
    raw_weight NUMBER,
    harvested_by VARCHAR2(100),
    timestamp TIMESTAMP,
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_wtick_bed FOREIGN KEY (bed_id) REFERENCES farm_bed(bed_id),
    CONSTRAINT fk_wtick_ing FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id)
);

-- Table: qc_record
CREATE TABLE qc_record (
    qc_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    source_type VARCHAR2(50),
    reference_id VARCHAR2(50),
    inspector_name VARCHAR2(100),
    pass_status VARCHAR2(20),
    checked_at TIMESTAMP,
    notes VARCHAR2(4000),
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    sample_size NUMBER,
    defects_found NUMBER,
    quality_score NUMBER,
    appearance_grade VARCHAR2(50),
    brix_level NUMBER,
    ph_level NUMBER,
    pesticide_residue_check VARCHAR2(20),
    final_grade VARCHAR2(20)
);

-- Table: transport_ticket
CREATE TABLE transport_ticket (
    transport_id VARCHAR2(50) NOT NULL PRIMARY KEY,
    source_type VARCHAR2(50),
    source_ticket_id VARCHAR2(50),
    destination_warehouse_id VARCHAR2(50),
    driver VARCHAR2(100),
    vehicle VARCHAR2(100),
    depart_time TIMESTAMP,
    arrive_time TIMESTAMP,
    status VARCHAR2(50),
    region VARCHAR2(50),
    site_id VARCHAR2(50),
    CONSTRAINT fk_trans_wh FOREIGN KEY (destination_warehouse_id) REFERENCES warehouse(warehouse_id)
);



