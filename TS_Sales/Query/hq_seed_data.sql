SET DEFINE OFF;
ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS';

-- =====================================================
-- CLEANUP (DELETE ALL DATA)
-- =====================================================

BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE export_document_set'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE sale_order'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE contract_item'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE contract'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE proforma_invoice'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE quotation_item'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE quotation'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE incoterm'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE payment_term'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE product'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE customer'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'TRUNCATE TABLE staff'; EXCEPTION WHEN OTHERS THEN NULL; END;
/

-- =====================================================
-- INSERT DATA IN CORRECT FK DEPENDENCY ORDER
-- =====================================================

-- 1. STAFF (No dependencies) - thêm status TERMINATED
INSERT INTO staff (staff_id, name, role, email, phone, department, status)
SELECT LEVEL,
    'Staff_'||LEVEL,
    'Sales',
    'staff'||LEVEL||'@mail.com',
    '09'||LPAD(LEVEL,2,'0'),
    'Sales Dept',
    CASE WHEN MOD(LEVEL,5)=0 THEN 'TERMINATED'
         WHEN MOD(LEVEL,5)=1 THEN 'FIRED'
         ELSE 'ACTIVE' END
FROM dual CONNECT BY LEVEL <= 100;
COMMIT;

-- 2. CUSTOMER (No dependencies) - với STATUS đa dạng
INSERT INTO customer
SELECT LEVEL, 'B2B', 'C'||LPAD(LEVEL,3,'0'),
    'Company_'||LEVEL, 'C'||LEVEL,
    'TAX'||LPAD(LEVEL,5,'0'),
    CASE WHEN MOD(LEVEL,3)=0 THEN 'Japan'
         WHEN MOD(LEVEL,3)=1 THEN 'USA'
         ELSE 'Netherlands' END,
    CASE WHEN MOD(LEVEL,3)=0 THEN 
            CASE WHEN MOD(LEVEL,5)=0 THEN 'Tokyo' WHEN MOD(LEVEL,5)=1 THEN 'Osaka' WHEN MOD(LEVEL,5)=2 THEN 'Kyoto' WHEN MOD(LEVEL,5)=3 THEN 'Yokohama' ELSE 'Kobe' END
         WHEN MOD(LEVEL,3)=1 THEN
            CASE WHEN MOD(LEVEL,5)=0 THEN 'New York' WHEN MOD(LEVEL,5)=1 THEN 'Los Angeles' WHEN MOD(LEVEL,5)=2 THEN 'Chicago' WHEN MOD(LEVEL,5)=3 THEN 'Houston' ELSE 'Phoenix' END
         ELSE 
            CASE WHEN MOD(LEVEL,5)=0 THEN 'Amsterdam' WHEN MOD(LEVEL,5)=1 THEN 'Rotterdam' WHEN MOD(LEVEL,5)=2 THEN 'The Hague' WHEN MOD(LEVEL,5)=3 THEN 'Utrecht' ELSE 'Eindhoven' END
    END AS city,
    CASE WHEN MOD(LEVEL,3)=0 THEN 
            CASE WHEN MOD(LEVEL,5)=0 THEN '1-2-1 Ginza, Chuo Ward' WHEN MOD(LEVEL,5)=1 THEN '2-3-5 Dotonbori, Chuo Ward' WHEN MOD(LEVEL,5)=2 THEN '123 Gojo, Shimogyo Ward' WHEN MOD(LEVEL,5)=3 THEN '4-5-6 Minato Mirai' ELSE '7-8-9 Port Area' END
         WHEN MOD(LEVEL,3)=1 THEN
            CASE WHEN MOD(LEVEL,5)=0 THEN '350 5th Ave, Manhattan' WHEN MOD(LEVEL,5)=1 THEN '6000 Sunset Blvd, LA' WHEN MOD(LEVEL,5)=2 THEN '233 N Michigan Ave' WHEN MOD(LEVEL,5)=3 THEN '1000 Louisiana St' ELSE '100 West Washington' END
         ELSE
            CASE WHEN MOD(LEVEL,5)=0 THEN '1 Damrak, Amsterdam' WHEN MOD(LEVEL,5)=1 THEN '123 Maas Port, Rotterdam' WHEN MOD(LEVEL,5)=2 THEN '45 Hofvijver, The Hague' WHEN MOD(LEVEL,5)=3 THEN '67 Vredenburg, Utrecht' ELSE '89 Dommelstraat, Eindhoven' END
    END AS address,
    '09'||LPAD(LEVEL,2,'0'),
    'mail'||LEVEL||'@mail.com',
    'www.c'||LEVEL||'.com',
    'Food',
    CASE WHEN MOD(LEVEL,6)=0 THEN 'ACTIVE'
         WHEN MOD(LEVEL,6)=1 THEN 'INACTIVE'
         WHEN MOD(LEVEL,6)=2 THEN 'PENDING'
         WHEN MOD(LEVEL,6)=3 THEN 'SUSPENDED'
         WHEN MOD(LEVEL,6)=4 THEN 'VERIFIED'
         ELSE 'TRIAL' END,
    CASE WHEN MOD(LEVEL,2)=0 THEN 'USD' ELSE 'EUR' END,
    DATE '2025-01-01' + LEVEL
FROM dual CONNECT BY LEVEL <= 200;
COMMIT;

-- 3. PRODUCT (No dependencies) - scale up to 500 rows
INSERT INTO product
SELECT LEVEL,
    CASE WHEN MOD(LEVEL,3)=0 THEN 'Juice'
         WHEN MOD(LEVEL,3)=1 THEN 'Puree'
         ELSE 'Concentrate' END,
    'Product_'||LEVEL,
    'Description for Product_'||LEVEL,
    ROUND(DBMS_RANDOM.VALUE(50,500),2),
    'Food Application',
    ROUND(DBMS_RANDOM.VALUE(10,20),2),
    'Size_'||LEVEL,
    ROUND(DBMS_RANDOM.VALUE(5,15),2),
    ROUND(DBMS_RANDOM.VALUE(3,5),2),
    CASE WHEN MOD(LEVEL,8)=0 THEN 0 ELSE 1 END,
    DATE '2024-06-01' + TRUNC(DBMS_RANDOM.VALUE(0,200)),
    DATE '2024-06-01' + TRUNC(DBMS_RANDOM.VALUE(100,300))
FROM dual CONNECT BY LEVEL <= 500;
COMMIT;

-- 4. PAYMENT_TERM (No dependencies)
INSERT INTO payment_term VALUES (1,'Net30',30,'ACTIVE');
INSERT INTO payment_term VALUES (2,'Net60',60,'ACTIVE');
COMMIT;

-- 5. INCOTERM (No dependencies)
INSERT INTO incoterm VALUES (1,'FOB','Free on Board','2020','ACTIVE');
INSERT INTO incoterm VALUES (2,'CIF','Cost Insurance Freight','2020','ACTIVE');
COMMIT;

-- 6. QUOTATION (deps: customer, staff) - currency khớp với customer
INSERT INTO quotation
SELECT q.quotation_id,
    MOD(q.quotation_id,200)+1,
    MOD(q.quotation_id,100)+1,
    DATE '2025-01-01' + MOD(q.quotation_id,180),
    DATE '2025-01-01' + MOD(q.quotation_id,180)+30,
    ROUND(DBMS_RANDOM.VALUE(5000,50000),2),
    c.preferred_currency,
    CASE WHEN MOD(q.quotation_id,5)=0 THEN 'DRAFT'
         WHEN MOD(q.quotation_id,5)=1 THEN 'APPROVED'
         WHEN MOD(q.quotation_id,5)=2 THEN 'REJECTED'
         WHEN MOD(q.quotation_id,5)=3 THEN 'EXPIRED'
         ELSE 'PENDING_REVIEW' END,
    DATE '2024-06-01' + TRUNC(DBMS_RANDOM.VALUE(0,250))
FROM (SELECT LEVEL AS quotation_id, MOD(LEVEL,200)+1 AS customer_id FROM dual CONNECT BY LEVEL <= 3000) q
JOIN customer c ON q.customer_id = c.customer_id;
COMMIT;

-- 7. QUOTATION_ITEM (deps: quotation, product) - PK composite (quotation_id, product_id)
INSERT INTO quotation_item
SELECT TRUNC((LEVEL-1)/2)+1,
    MOD(LEVEL-1,500)+1,
    MOD(LEVEL,10)+1,
    ROUND(DBMS_RANDOM.VALUE(100,500),2),
    CASE WHEN MOD(LEVEL,5)=0 THEN 0 WHEN MOD(LEVEL,5)=1 THEN 5 WHEN MOD(LEVEL,5)=2 THEN 10 WHEN MOD(LEVEL,5)=3 THEN 15 ELSE 20 END,
    CASE WHEN MOD(LEVEL,4)=0 THEN 5 WHEN MOD(LEVEL,4)=1 THEN 8 WHEN MOD(LEVEL,4)=2 THEN 10 ELSE 15 END,
    ROUND(DBMS_RANDOM.VALUE(1000,10000),2),
    DATE '2025-01-01' + TRUNC(DBMS_RANDOM.VALUE(0,250))
FROM dual CONNECT BY LEVEL <= 2000;
COMMIT;

-- 8. PROFORMA_INVOICE (deps: quotation, payment_term, staff) - currency khớp, thêm created_at, updated_at
INSERT INTO proforma_invoice
SELECT LEVEL,
    CASE WHEN LEVEL <= 3000 THEN MOD(LEVEL,3000)+1 ELSE MOD(LEVEL,3000)+1 END,
    MOD(LEVEL,2)+1,
    MOD(LEVEL,100)+1,
    ROUND(DBMS_RANDOM.VALUE(5000,50000),2),
    CASE WHEN MOD(LEVEL,2)=0 THEN 'USD' ELSE 'EUR' END,
    'Cat Lai Port',
    'Destination_Port_'||LEVEL,
    DATE '2025-01-01'+MOD(LEVEL,180),
    CASE WHEN MOD(LEVEL,5)=0 THEN 'DRAFT'
         WHEN MOD(LEVEL,5)=1 THEN 'ISSUED'
         WHEN MOD(LEVEL,5)=2 THEN 'ACCEPTED'
         WHEN MOD(LEVEL,5)=3 THEN 'REJECTED'
         ELSE 'CANCELLED' END,
    'file_'||LEVEL||'.pdf',
    DATE '2025-01-01' + TRUNC(DBMS_RANDOM.VALUE(0,90)) - 5,
    DATE '2025-01-01' + TRUNC(DBMS_RANDOM.VALUE(0,90))
FROM dual CONNECT BY LEVEL <= 500;
COMMIT;

-- 9. CONTRACT (deps: customer, incoterm, proforma_invoice) - scale up to 600 rows
INSERT INTO contract
SELECT c.contract_id,
    c.customer_id,
    CASE WHEN MOD(c.contract_id,4)=0 THEN 'Standard'
         WHEN MOD(c.contract_id,4)=1 THEN 'Long-term'
         WHEN MOD(c.contract_id,4)=2 THEN 'Trial'
         ELSE 'Partnership' END,
    MOD(c.contract_id,2)+1,
    MOD(c.contract_id,500)+1,
    DATE '2025-01-01' + MOD(c.contract_id,180),
    DATE '2025-01-01' + MOD(c.contract_id,180) + 1,
    CASE WHEN MOD(c.contract_id,8)<4 THEN DATE '2025-01-01' + MOD(c.contract_id,180) + 365
         ELSE DATE '2024-12-01' + MOD(c.contract_id,180) END,
    ROUND(DBMS_RANDOM.VALUE(10000,100000),2),
    ROUND(DBMS_RANDOM.VALUE(100,1000)),
    cust.preferred_currency,
    'Loading_Port_'||c.contract_id,
    'Destination_Port_'||c.contract_id,
    CASE WHEN MOD(c.contract_id,5)=0 THEN 'ACTIVE'
         WHEN MOD(c.contract_id,5)=1 THEN 'EXPIRED'
         WHEN MOD(c.contract_id,5)=2 THEN 'PENDING'
         WHEN MOD(c.contract_id,5)=3 THEN 'COMPLETED'
         ELSE 'CANCELLED' END,
    DATE '2025-01-01' + TRUNC(DBMS_RANDOM.VALUE(0,60)),
    DATE '2025-01-01' + TRUNC(DBMS_RANDOM.VALUE(0,60)) - 5,
    DATE '2025-01-01' + TRUNC(DBMS_RANDOM.VALUE(0,60))
FROM (SELECT LEVEL AS contract_id, MOD(LEVEL,200)+1 AS customer_id FROM dual CONNECT BY LEVEL <= 600) c
JOIN customer cust ON c.customer_id = cust.customer_id;
COMMIT;

-- 10. CONTRACT_ITEM (deps: contract, product) - PK composite (contract_id, product_id)
INSERT INTO contract_item
SELECT TRUNC((LEVEL-1)/2)+1,
    MOD(LEVEL-1,500)+1,
    MOD(LEVEL,10)+1,
    ROUND(DBMS_RANDOM.VALUE(100,500),2),
    CASE WHEN MOD(LEVEL,5)=0 THEN 0 WHEN MOD(LEVEL,5)=1 THEN 5 WHEN MOD(LEVEL,5)=2 THEN 10 WHEN MOD(LEVEL,5)=3 THEN 15 ELSE 20 END,
    CASE WHEN MOD(LEVEL,4)=0 THEN 5 WHEN MOD(LEVEL,4)=1 THEN 10 WHEN MOD(LEVEL,4)=2 THEN 15 ELSE 20 END,
    ROUND(DBMS_RANDOM.VALUE(1000,10000),2),
    DATE '2025-01-01' + TRUNC(DBMS_RANDOM.VALUE(0,250))
FROM dual CONNECT BY LEVEL <= 600;
COMMIT;

-- 11. SALE_ORDER (deps: contract) - currency khớp, thêm created_at, updated_at
INSERT INTO sale_order
SELECT so.sale_order_id,
    MOD(so.sale_order_id,300)+1,
    DATE '2025-01-01'+MOD(so.sale_order_id,180),
    DATE '2025-01-01'+MOD(so.sale_order_id,180)+15,
    ROUND(DBMS_RANDOM.VALUE(5000,50000),2),
    CASE WHEN MOD(so.sale_order_id,2)=0 THEN 'USD' ELSE 'EUR' END,
    CASE WHEN MOD(so.sale_order_id,6)=0 THEN 'DRAFT'
         WHEN MOD(so.sale_order_id,6)=1 THEN 'PENDING'
         WHEN MOD(so.sale_order_id,6)=2 THEN 'IN_PROGRESS'
         WHEN MOD(so.sale_order_id,6)=3 THEN 'DELIVERED'
         WHEN MOD(so.sale_order_id,6)=4 THEN 'COMPLETED'
         ELSE 'CANCELLED' END,
    DATE '2025-01-01'+MOD(so.sale_order_id,180)-3,
    DATE '2025-01-01'+MOD(so.sale_order_id,180)
FROM (SELECT LEVEL AS sale_order_id FROM dual CONNECT BY LEVEL <= 300) so;
COMMIT;

-- 12. EXPORT_DOCUMENT_SET (deps: sale_order)
INSERT INTO export_document_set
SELECT LEVEL,
    MOD(LEVEL,300)+1,
    DATE '2025-01-01'+MOD(LEVEL,180),
    CASE WHEN MOD(LEVEL,5)=0 THEN 'B/L'
         WHEN MOD(LEVEL,5)=1 THEN 'Invoice'
         WHEN MOD(LEVEL,5)=2 THEN 'Packing List'
         WHEN MOD(LEVEL,5)=3 THEN 'Certificate of Origin'
         ELSE 'Health Certificate' END,
    'doc_'||LEVEL||'.pdf',
    CASE WHEN MOD(LEVEL,3)=0 THEN 'COMPLETED' WHEN MOD(LEVEL,3)=1 THEN 'IN_PROGRESS' ELSE 'PENDING' END,
    DATE '2025-01-01'+MOD(LEVEL,180)-2,
    DATE '2025-01-01'+MOD(LEVEL,180)
FROM dual CONNECT BY LEVEL <= 300;
COMMIT;

-- Đếm số dòng từng bảng
SELECT 
  'STAFF' AS table_name, COUNT(*) AS row_count FROM staff
UNION ALL SELECT 'CUSTOMER', COUNT(*) FROM customer
UNION ALL SELECT 'PRODUCT', COUNT(*) FROM product
UNION ALL SELECT 'PAYMENT_TERM', COUNT(*) FROM payment_term
UNION ALL SELECT 'INCOTERM', COUNT(*) FROM incoterm
UNION ALL SELECT 'QUOTATION', COUNT(*) FROM quotation
UNION ALL SELECT 'QUOTATION_ITEM', COUNT(*) FROM quotation_item
UNION ALL SELECT 'PROFORMA_INVOICE', COUNT(*) FROM proforma_invoice
UNION ALL SELECT 'CONTRACT', COUNT(*) FROM contract
UNION ALL SELECT 'CONTRACT_ITEM', COUNT(*) FROM contract_item
UNION ALL SELECT 'SALE_ORDER', COUNT(*) FROM sale_order
UNION ALL SELECT 'EXPORT_DOCUMENT_SET', COUNT(*) FROM export_document_set
ORDER BY table_name;

-- Tổng cộng tất cả dòng
SELECT 
  (SELECT COUNT(*) FROM staff) +
  (SELECT COUNT(*) FROM customer) +
  (SELECT COUNT(*) FROM product) +
  (SELECT COUNT(*) FROM payment_term) +
  (SELECT COUNT(*) FROM incoterm) +
  (SELECT COUNT(*) FROM quotation) +
  (SELECT COUNT(*) FROM quotation_item) +
  (SELECT COUNT(*) FROM proforma_invoice) +
  (SELECT COUNT(*) FROM contract) +
  (SELECT COUNT(*) FROM contract_item) +
  (SELECT COUNT(*) FROM sale_order) +
  (SELECT COUNT(*) FROM export_document_set) AS total_rows
FROM dual;