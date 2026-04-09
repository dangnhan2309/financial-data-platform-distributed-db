BEGIN EXECUTE IMMEDIATE 'DROP TABLE export_document_set CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE sale_order CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE contract_item CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE contract CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE proforma_invoice CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE quotation_item CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE quotation CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE incoterm CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE payment_term CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE product CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE customer CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE staff CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/



-- STAFF
CREATE TABLE staff (
    staff_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    role VARCHAR2(50),
    email VARCHAR2(100),
    phone VARCHAR2(20),
    department VARCHAR2(50),
    status VARCHAR2(20)
);

-- CUSTOMER
CREATE TABLE customer (
    customer_id NUMBER PRIMARY KEY,
    customer_type VARCHAR2(50),
    customer_code VARCHAR2(50),
    company_name VARCHAR2(100),
    short_name VARCHAR2(50),
    tax_id VARCHAR2(50),
    country VARCHAR2(50),
    city VARCHAR2(50),
    address VARCHAR2(200),
    phone VARCHAR2(20),
    email VARCHAR2(100),
    website VARCHAR2(100),
    industry VARCHAR2(50),
    status VARCHAR2(20),
    preferred_currency VARCHAR2(10),
    created_at DATE
);

-- PRODUCT
CREATE TABLE product (
    product_id NUMBER PRIMARY KEY,
    product_type VARCHAR2(50),
    name VARCHAR2(100),
    description VARCHAR2(200),
    price NUMBER,
    application VARCHAR2(100),
    brix NUMBER,
    product_size VARCHAR2(50),
    solid NUMBER,
    ph NUMBER,
    is_active NUMBER,
    created_at DATE,
    updated_at DATE
);

-- PAYMENT TERM
CREATE TABLE payment_term (
    payment_term_id NUMBER PRIMARY KEY,
    description VARCHAR2(100),
    number_of_days NUMBER,
    status VARCHAR2(20)
);

-- INCOTERM
CREATE TABLE incoterm (
    incoterm_id NUMBER PRIMARY KEY,
    name VARCHAR2(10),
    description VARCHAR2(100),
    version VARCHAR2(10),
    status VARCHAR2(20)
);

-- QUOTATION
CREATE TABLE quotation (
    quotation_id NUMBER PRIMARY KEY,
    customer_id NUMBER,
    staff_id NUMBER,
    quotation_date DATE,
    expiry_date DATE,
    total_amount NUMBER,
    currency VARCHAR2(10),
    status VARCHAR2(20),
    created_at DATE
);

-- QUOTATION ITEM
CREATE TABLE quotation_item (
    quotation_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    quantity NUMBER,
    unit_price NUMBER,
    discount NUMBER,
    tax_rate NUMBER,
    total_price NUMBER,
    created_at DATE,
    PRIMARY KEY (quotation_id, product_id)
);

-- PROFORMA
CREATE TABLE proforma_invoice (
    proforma_invoice_id NUMBER PRIMARY KEY,
    quotation_id NUMBER,
    payment_term_id NUMBER,
    staff_id NUMBER,
    total_contract_value NUMBER,
    currency VARCHAR2(10),
    port_of_loading VARCHAR2(100),
    port_of_discharge VARCHAR2(100),
    delivery_time DATE,
    status VARCHAR2(20),
    file_path VARCHAR2(200),
    created_at DATE,
    updated_at DATE
);

-- CONTRACT
CREATE TABLE contract (
    contract_id NUMBER PRIMARY KEY,
    customer_id NUMBER,
    contract_type VARCHAR2(50),
    incoterm_id NUMBER,
    proforma_invoice_id NUMBER,
    contract_date DATE,
    effective_date DATE,
    expiry_date DATE,
    total_contract_value NUMBER,
    total_quantity NUMBER,
    currency VARCHAR2(10),
    loading_port VARCHAR2(100),
    destination_port VARCHAR2(100),
    status VARCHAR2(20),
    signed_date DATE,
    created_at DATE,
    updated_at DATE
);

-- CONTRACT ITEM
CREATE TABLE contract_item (
    contract_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    quantity NUMBER,
    unit_price NUMBER,
    discount NUMBER,
    tax_rate NUMBER,
    total_price NUMBER,
    created_at DATE,
    PRIMARY KEY (contract_id, product_id)
);

-- SALE ORDER
CREATE TABLE sale_order (
    sale_order_id NUMBER PRIMARY KEY,
    contract_id NUMBER,
    order_date DATE,
    delivery_date DATE,
    total_amount NUMBER,
    currency VARCHAR2(10),
    status VARCHAR2(20),
    created_at DATE,
    updated_at DATE
);

-- EXPORT DOC
CREATE TABLE export_document_set (
    document_set_id NUMBER PRIMARY KEY,
    sale_order_id NUMBER,
    issue_date DATE,
    document_type VARCHAR2(50),
    file_path VARCHAR2(200),
    status VARCHAR2(20),
    created_at DATE,
    updated_at DATE
);



-- QUOTATION
ALTER TABLE quotation ADD CONSTRAINT fk_quotation_customer
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id);

ALTER TABLE quotation ADD CONSTRAINT fk_quotation_staff
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id);

-- QUOTATION_ITEM
ALTER TABLE quotation_item ADD CONSTRAINT fk_quotation_item_quotation
    FOREIGN KEY (quotation_id) REFERENCES quotation(quotation_id);

ALTER TABLE quotation_item ADD CONSTRAINT fk_quotation_item_product
    FOREIGN KEY (product_id) REFERENCES product(product_id);

-- PROFORMA_INVOICE
ALTER TABLE proforma_invoice ADD CONSTRAINT fk_proforma_quotation
    FOREIGN KEY (quotation_id) REFERENCES quotation(quotation_id);

ALTER TABLE proforma_invoice ADD CONSTRAINT fk_proforma_payment_term
    FOREIGN KEY (payment_term_id) REFERENCES payment_term(payment_term_id);

ALTER TABLE proforma_invoice ADD CONSTRAINT fk_proforma_staff
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id);

-- CONTRACT
ALTER TABLE contract ADD CONSTRAINT fk_contract_customer
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id);

ALTER TABLE contract ADD CONSTRAINT fk_contract_incoterm
    FOREIGN KEY (incoterm_id) REFERENCES incoterm(incoterm_id);

ALTER TABLE contract ADD CONSTRAINT fk_contract_proforma
    FOREIGN KEY (proforma_invoice_id) REFERENCES proforma_invoice(proforma_invoice_id);

-- CONTRACT_ITEM
ALTER TABLE contract_item ADD CONSTRAINT fk_contract_item_contract
    FOREIGN KEY (contract_id) REFERENCES contract(contract_id);

ALTER TABLE contract_item ADD CONSTRAINT fk_contract_item_product
    FOREIGN KEY (product_id) REFERENCES product(product_id);

-- SALE_ORDER
ALTER TABLE sale_order ADD CONSTRAINT fk_sale_order_contract
    FOREIGN KEY (contract_id) REFERENCES contract(contract_id);

-- EXPORT_DOCUMENT_SET
ALTER TABLE export_document_set ADD CONSTRAINT fk_export_doc_sale_order
    FOREIGN KEY (sale_order_id) REFERENCES sale_order(sale_order_id);